"""Locally authenticated, locked, crash-tolerant metadata journals.

The local operator state directory is trusted. A journal received from a PR or
another machine is not execution proof and cannot be adopted automatically.
"""
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import fcntl


class ExecutionError(Exception):
    """Conflict or uncertain effect requiring inspection before another attempt."""


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class Journal:
    def __init__(self, path, plan, state_dir=None):
        self.path, self.plan = Path(path), plan
        base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
        self.state_dir = Path(state_dir) if state_dir else base / "ai-ascension-metadata"
        self.handle, self.events, self.previous = None, [], "0" * 64
        self.repository_locks = []

    def _lock_repositories(self):
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        for repository_id in sorted({str(x["repository_id"]) for x in self.plan.get("targets", [])}):
            identifier = hashlib.sha256(repository_id.encode()).hexdigest()
            path = self.state_dir / ("repository-" + identifier + ".lock")
            handle = os.fdopen(os.open(path, os.O_RDWR | os.O_CREAT, 0o600), "a+")
            self.repository_locks.append(handle)
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _release_repositories(self):
        for handle in reversed(self.repository_locks):
            handle.close()
        self.repository_locks.clear()

    def _key(self, existing):
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        identifier = hashlib.sha256(str(self.path.resolve()).encode()).hexdigest()
        path = self.state_dir / (identifier + ".key")
        if not path.exists():
            if existing:
                raise ExecutionError("journal has no trusted local key; manual review required")
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as stream:
                stream.write(secrets.token_bytes(32))
                stream.flush()
                os.fsync(stream.fileno())
        self.key = path.read_bytes()
        if len(self.key) != 32:
            raise ExecutionError("invalid local journal key")

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+", encoding="utf-8")
        try:
            fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._lock_repositories()
            self.handle.seek(0)
            raw = self.handle.read()
            self._key(bool(raw))
            lines = raw.splitlines(keepends=True)
            torn = lines.pop() if lines and not lines[-1].endswith("\n") else None
            for line in lines:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ExecutionError("malformed journal event")
                if (not isinstance(event.get("phase"), str)
                        or (event["phase"] in {"intent", "verified", "reconciled", "rollback-intent", "rolled-back"}
                            and (not isinstance(event.get("effect"), dict) or not isinstance(event.get("key"), str)))):
                    raise ExecutionError("malformed journal effect")
                signature = event.pop("signature", None)
                expected = hmac.new(self.key, canonical(event).encode(), hashlib.sha256).hexdigest()
                if not isinstance(signature, str) or not hmac.compare_digest(signature, expected):
                    raise ExecutionError("journal authentication failed")
                if event.get("previous") != self.previous or event.get("plan_digest") != self.plan["digest"]:
                    raise ExecutionError("journal chain or plan identity mismatch")
                self.previous = signature
                self.events.append(event)
            if torn is not None:
                # A killed writer may leave a partial final record. Retain its
                # exact bytes locally, then resume from the authenticated prefix.
                backup = self.state_dir / (hashlib.sha256(torn.encode()).hexdigest() + ".torn")
                backup.write_text(torn, encoding="utf-8")
                self.handle.seek(0)
                self.handle.truncate()
                self.handle.write("".join(lines))
                self.handle.flush()
                os.fsync(self.handle.fileno())
                self.append({"phase": "recovered-tail", "discarded_sha256": hashlib.sha256(torn.encode()).hexdigest()})
        except (OSError, ValueError, ExecutionError) as exc:
            self._release_repositories()
            self.handle.close()
            raise ExecutionError(f"journal unavailable or invalid: {exc}") from exc
        return self

    def append(self, event):
        event = {"plan_digest": self.plan["digest"], "previous": self.previous, **event}
        signature = hmac.new(self.key, canonical(event).encode(), hashlib.sha256).hexdigest()
        self.handle.write(canonical({**event, "signature": signature}) + "\n")
        self.handle.flush()
        os.fsync(self.handle.fileno())
        self.events.append(event)
        self.previous = signature

    def __exit__(self, *args):
        self.handle.close()
        self._release_repositories()

    def started(self, key):
        return any(e.get("key") == key and e.get("phase") == "intent" for e in self.events)

    def owned(self, key):
        return any(e.get("key") == key and e.get("phase") == "verified" and e.get("owned") is True for e in self.events)
