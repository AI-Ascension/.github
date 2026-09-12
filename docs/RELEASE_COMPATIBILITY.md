# Release compatibility evidence

Status: implemented local evidence-consistency tooling; release adoption and policy
approval remain owner decisions. This is not a new wire contract, cryptographic
attestation system, or permission to publish. Protocol owners retain technical
contract ownership and independent versions.

`tools/release_compatibility.py` verifies a candidate manifest against an independently
reviewed policy. The policy binds exact source commits, contract versions/digests,
producer/consumer relationships and required evidence receipt digests. A candidate
cannot drop a required native check or relabel a synthetic result as native while
retaining the approved policy digest. Every source and contract must have check
coverage, and each producer/consumer edge needs a joint check scope.

Schemas are under `metadata/schema/`: `release-compatibility.schema.json`,
`release-policy.schema.json`, and `release-receipt.schema.json`. The verifier also
enforces semantic set equality, unique IDs, source membership, exact receipt/log
hashes, safe relative non-symlink paths, completed timestamps and passing results.
Schema shape alone does not establish qualification.

## Review and verification

1. The release owner defines the intended source set, versioned contracts and
   required qualification classes. Preserve distinctions among build, synthetic,
   native-session0, operations and exact-host evidence. Missing native infrastructure
   is `unverified`, never a synthetic substitute for native evidence.
2. Run the actual required checks against those exact source revisions. Each receipt
   records check ID/class, all participating source SHAs, contract IDs, result,
   timestamp, runner identifier and a relative log path with its SHA-256. Strip
   secrets/private host paths from logs before review; changing a log changes its
   digest and requires a new receipt. Never construct a successful receipt for an
   unexecuted test. The unit-test receipts are synthetic test data only.
3. Review the receipts and logs independently. Bind the reviewed receipt digests into
   the policy, and convey the policy's SHA-256 through an independently trusted owner
   review channel. Do not obtain the "approved" policy digest from an untrusted
   candidate's own output or mutable branch. A file saying it is approved is not
   authorization. This verifier cannot authenticate the reviewer or the truth of a
   manually forged log; hosted attestation/native-run verification remains external.
4. Bundle manifest, receipts and logs. Run:

   ```sh
   python tools/release_compatibility.py --manifest candidate.json --policy reviewed-policy.json --policy-sha256 OWNER_APPROVED_POLICY_SHA256 --evidence-root evidence
   ```

5. Only `reviewed_evidence_consistent_not_published` is a successful result. Any missing
   check, mismatched source/version/hash, failed/skipped/unverified result, unsafe
   receipt path or inconsistent evidence fails with nonzero exit. Publication and
   required-check settings need separate authorization; no such operation exists in
   this tool. Keep the verified bundle immutable through any later authorized release.

Compatibility rollout is policy-specific, not an implicit demand that every repo
share one dependency revision. First review a synthetic producer/consumer pilot,
then require native/operations evidence only for the release scope that promises it.
No actual organization release is qualified by the current synthetic unit tests.

Run `python -m unittest discover -s tests -p 'test_release_compatibility.py' -v`.
Tests cover consistent evidence, policy resealing, omitted/duplicate evidence,
source and candidate-version mismatch, native substitution, unavailable results,
receipt/log tampering, unsafe paths, symlinks, duplicate JSON keys, future timestamps
and insufficient cross-repository scope. Existing metadata validation discovers the
tests; a dedicated workflow also covers tool-only changes without credentials.
