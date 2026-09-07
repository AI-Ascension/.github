use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use std::process;

type Result<T> = std::result::Result<T, String>;

const EVIDENCE_STATES: &[&str] = &[
    "confirmed",
    "source-derived",
    "proposed",
    "inferred",
    "unverified",
    "unsupported",
];

#[derive(Debug, Default)]
struct Cli {
    command: String,
    root: PathBuf,
    source_root: PathBuf,
    target_root: PathBuf,
    repository: String,
    profile_id: String,
    owner: String,
    source_commit: String,
}

#[derive(Debug, Default)]
struct Profile {
    schema_version: Option<u32>,
    profile_id: Option<String>,
    repository: Option<String>,
    owner: Option<String>,
    source_bundle: Option<String>,
    source_commit: Option<String>,
    source_digest: Option<String>,
    distribution: Option<String>,
    scopes: Option<Vec<String>>,
    checks: BTreeMap<String, Vec<String>>,
    evidence: BTreeMap<String, String>,
    exception_file: Option<String>,
    exception_status: Option<String>,
}

#[derive(Debug, Default)]
struct LockFile {
    lock_version: Option<u32>,
    repository: Option<String>,
    profile_id: Option<String>,
    source_repository: Option<String>,
    source_commit: Option<String>,
    bundle_digest: Option<String>,
    distribution: Option<String>,
    published: Option<bool>,
    files: Vec<(String, String)>,
    protected_paths: Vec<String>,
    generated_by: Option<String>,
}

#[derive(Debug, Default)]
struct RepoEntry {
    repository: String,
    repository_id: String,
    node_id: String,
    default_branch: String,
    baseline_commit: String,
    owner: String,
    profile_id: String,
    adoption: String,
    exclusion_reason: Option<String>,
}

fn main() {
    let args = match parse_cli() {
        Ok(value) => value,
        Err(error) => fail(&error),
    };

    let result = match args.command.as_str() {
        "validate" => validate_root(&args.root),
        "fixture-check" => fixture_check(&args.root),
        "sync" => sync_bundle(&args),
        "help" | "--help" | "-h" => {
            print_help();
            Ok(())
        }
        command => Err(format!("unknown command `{command}`; use `help`")),
    };

    if let Err(error) = result {
        fail(&error);
    }
}

fn fail(error: &str) -> ! {
    eprintln!("standards-sync: error: {error}");
    process::exit(1);
}

fn print_help() {
    println!(
        "standards-sync/1\n\nCommands:\n  validate [--root PATH]\n  fixture-check --root standards/conformance\n  sync --source-root PATH --target-root PATH --repository OWNER/NAME --profile-id ID --owner OWNER --source-commit COMMIT\n\nAll operations are local and dependency-free."
    );
}

fn parse_cli() -> Result<Cli> {
    let mut values = env::args().skip(1);
    let command = values.next().unwrap_or_else(|| "help".to_owned());
    let mut cli = Cli {
        command,
        root: PathBuf::from("."),
        ..Cli::default()
    };

    while let Some(flag) = values.next() {
        let mut value = || {
            values
                .next()
                .ok_or_else(|| format!("missing value for {flag}"))
        };
        match flag.as_str() {
            "--root" => cli.root = PathBuf::from(value()?),
            "--source-root" => cli.source_root = PathBuf::from(value()?),
            "--target-root" => cli.target_root = PathBuf::from(value()?),
            "--repository" => cli.repository = value()?,
            "--profile-id" => cli.profile_id = value()?,
            "--owner" => cli.owner = value()?,
            "--source-commit" => cli.source_commit = value()?,
            flag => return Err(format!("unknown option `{flag}`")),
        }
    }

    Ok(cli)
}

fn validate_root(root: &Path) -> Result<()> {
    let root = root
        .canonicalize()
        .map_err(|error| format!("cannot read root {}: {error}", root.display()))?;
    let standards = root.join("standards");
    let profile_path = root.join("standards-profile.toml");
    let lock_path = root.join("standards.lock.json");

    require_regular_file(&profile_path)?;
    require_regular_file(&lock_path)?;
    require_directory(&standards)?;

    let profile = parse_profile(&profile_path)?;
    validate_profile(&profile)?;
    let lock = parse_lock(&lock_path)?;
    validate_lock_shape(&lock, &profile)?;
    validate_lock_bytes(&root, &lock)?;
    validate_rules(&standards.join("rules.yaml"))?;
    let profile_ids = validate_profile_catalog(&standards.join("profiles.yaml"))?;
    validate_repository_map(&standards.join("repositories.yaml"), &profile_ids)?;
    validate_schemas(&standards.join("schemas"))?;
    validate_conformance(&standards.join("conformance"))?;

    println!(
        "validated profile={} repository={} source_commit={} files={} bundle_digest={}",
        profile.profile_id.as_deref().unwrap_or(""),
        profile.repository.as_deref().unwrap_or(""),
        profile.source_commit.as_deref().unwrap_or(""),
        lock.files.len(),
        lock.bundle_digest.as_deref().unwrap_or("")
    );
    Ok(())
}

fn parse_profile(path: &Path) -> Result<Profile> {
    let text = read_text(path)?;
    let mut profile = Profile::default();
    let mut section = String::new();
    let mut seen = BTreeSet::new();

    for (line_number, raw) in text.lines().enumerate() {
        let line = strip_comment(raw).trim().to_owned();
        if line.is_empty() {
            continue;
        }
        if line.starts_with('[') && line.ends_with(']') {
            section = line[1..line.len() - 1].to_owned();
            if !matches!(section.as_str(), "checks" | "evidence" | "exceptions") {
                return Err(format!(
                    "{}:{}: unknown TOML section",
                    path.display(),
                    line_number + 1
                ));
            }
            continue;
        }
        let (key, value) = line.split_once('=').ok_or_else(|| {
            format!(
                "{}:{}: expected key = value",
                path.display(),
                line_number + 1
            )
        })?;
        let key = key.trim();
        let value = value.trim();
        if !seen.insert(format!("{section}.{key}")) {
            return Err(format!(
                "{}:{}: duplicate key `{section}.{key}`",
                path.display(),
                line_number + 1
            ));
        }

        match (section.as_str(), key) {
            ("", "schema_version") => {
                profile.schema_version = Some(parse_u32(value, path, line_number)?)
            }
            ("", "profile_id") => {
                profile.profile_id = Some(parse_string(value, path, line_number)?)
            }
            ("", "repository") => {
                profile.repository = Some(parse_string(value, path, line_number)?)
            }
            ("", "owner") => profile.owner = Some(parse_string(value, path, line_number)?),
            ("", "source_bundle") => {
                profile.source_bundle = Some(parse_string(value, path, line_number)?)
            }
            ("", "source_commit") => {
                profile.source_commit = Some(parse_string(value, path, line_number)?)
            }
            ("", "source_digest") => {
                profile.source_digest = Some(parse_string(value, path, line_number)?)
            }
            ("", "distribution") => {
                profile.distribution = Some(parse_string(value, path, line_number)?)
            }
            ("", "scopes") => profile.scopes = Some(parse_array(value, path, line_number)?),
            ("checks", "fast" | "required" | "extended") => {
                profile
                    .checks
                    .insert(key.to_owned(), parse_array(value, path, line_number)?);
            }
            ("evidence", "runtime" | "deployment" | "provider") => {
                profile
                    .evidence
                    .insert(key.to_owned(), parse_string(value, path, line_number)?);
            }
            ("exceptions", "file") => {
                profile.exception_file = Some(parse_string(value, path, line_number)?);
            }
            ("exceptions", "status") => {
                profile.exception_status = Some(parse_string(value, path, line_number)?);
            }
            _ => {
                return Err(format!(
                    "{}:{}: unknown profile key `{section}.{key}`",
                    path.display(),
                    line_number + 1
                ));
            }
        }
    }
    Ok(profile)
}

fn validate_profile(profile: &Profile) -> Result<()> {
    if profile.schema_version != Some(1) {
        return Err("profile schema_version must be 1".to_owned());
    }
    let profile_id = required(&profile.profile_id, "profile_id")?;
    if !valid_profile_id(profile_id) {
        return Err(format!("invalid profile_id `{profile_id}`"));
    }
    let repository = required(&profile.repository, "repository")?;
    if !valid_repository(repository) {
        return Err(format!("invalid repository `{repository}`"));
    }
    let owner = required(&profile.owner, "owner")?;
    if !is_upper_identifier(owner) {
        return Err(format!("invalid owner `{owner}`"));
    }
    if required(&profile.source_bundle, "source_bundle")? != "AI-Ascension/.github" {
        return Err("source_bundle must be AI-Ascension/.github".to_owned());
    }
    let commit = required(&profile.source_commit, "source_commit")?;
    if !valid_commit(commit) {
        return Err("source_commit must be a 40-character lowercase commit".to_owned());
    }
    let digest = required(&profile.source_digest, "source_digest")?;
    if !valid_prefixed_digest(digest) {
        return Err("source_digest must be sha256:<64 lowercase hex>".to_owned());
    }
    if required(&profile.distribution, "distribution")? != "local" {
        return Err("distribution must be local".to_owned());
    }
    let scopes = required(&profile.scopes, "scopes")?;
    if scopes.is_empty() || !unique(scopes) || scopes.iter().any(|scope| !valid_scope(scope)) {
        return Err("scopes must be non-empty, unique lowercase identifiers".to_owned());
    }
    for name in ["fast", "required", "extended"] {
        let checks = profile
            .checks
            .get(name)
            .ok_or_else(|| format!("checks.{name} is required"))?;
        if !unique(checks) || checks.iter().any(|check| !valid_check_name(check)) {
            return Err(format!(
                "checks.{name} contains a duplicate or invalid check"
            ));
        }
    }
    for name in ["runtime", "deployment", "provider"] {
        let state = profile
            .evidence
            .get(name)
            .ok_or_else(|| format!("evidence.{name} is required"))?;
        if !EVIDENCE_STATES.contains(&state.as_str()) {
            return Err(format!("evidence.{name} has unknown state `{state}`"));
        }
    }
    let exception_file = required(&profile.exception_file, "exceptions.file")?;
    let exception_status = required(&profile.exception_status, "exceptions.status")?;
    if !matches!(exception_status.as_str(), "none" | "pending" | "approved") {
        return Err(format!("unknown exception status `{exception_status}`"));
    }
    if exception_status == "none" && !exception_file.is_empty() {
        return Err("exceptions.file must be empty when status is none".to_owned());
    }
    if exception_status != "none" && !valid_relative_path(exception_file) {
        return Err("an exception file must be a safe repository-relative path".to_owned());
    }
    Ok(())
}

fn parse_lock(path: &Path) -> Result<LockFile> {
    let text = read_text(path)?;
    if !looks_like_json(&text) {
        return Err(format!("{} is not a JSON object", path.display()));
    }
    let mut lock = LockFile::default();
    lock.lock_version = Some(json_u32(&text, "lock_version", 2)?);
    lock.repository = Some(json_string_at_indent(&text, "repository", 2)?);
    lock.profile_id = Some(json_string_at_indent(&text, "profile_id", 2)?);
    lock.source_repository = Some(json_string_at_indent(&text, "repository", 4)?);
    lock.source_commit = Some(json_string_at_indent(&text, "commit", 4)?);
    lock.bundle_digest = Some(json_string_at_indent(&text, "bundle_digest", 4)?);
    lock.distribution = Some(json_string_at_indent(&text, "distribution", 4)?);
    lock.published = Some(json_bool_at_indent(&text, "published", 4)?);
    lock.generated_by = Some(json_string_at_indent(&text, "generated_by", 2)?);
    lock.protected_paths = json_array_at_indent(&text, "protected_paths", 2)?;

    let mut pending_path: Option<String> = None;
    for line in text.lines() {
        if line.contains("\"path\"") {
            pending_path = Some(json_string_after_key(line, "path")?);
        }
        if line.contains("\"sha256\"") {
            let digest = json_string_after_key(line, "sha256")?;
            let path_value = pending_path
                .take()
                .ok_or_else(|| "lock file digest has no preceding path".to_owned())?;
            lock.files.push((path_value, digest));
        }
    }
    if lock.files.is_empty() {
        return Err("lock files must contain at least one entry".to_owned());
    }
    Ok(lock)
}

fn validate_lock_shape(lock: &LockFile, profile: &Profile) -> Result<()> {
    if lock.lock_version != Some(1) {
        return Err("lock_version must be 1".to_owned());
    }
    if lock.repository.as_deref() != profile.repository.as_deref() {
        return Err("lock repository does not match profile".to_owned());
    }
    if lock.profile_id.as_deref() != profile.profile_id.as_deref() {
        return Err("lock profile_id does not match profile".to_owned());
    }
    if lock.source_repository.as_deref() != Some("AI-Ascension/.github") {
        return Err("lock source.repository must be AI-Ascension/.github".to_owned());
    }
    if lock.source_commit.as_deref() != profile.source_commit.as_deref() {
        return Err("lock source.commit does not match profile source_commit".to_owned());
    }
    if lock.bundle_digest.as_deref() != profile.source_digest.as_deref() {
        return Err("lock bundle_digest does not match profile source_digest".to_owned());
    }
    if lock.distribution.as_deref() != Some("local") {
        return Err("lock source.distribution must be local".to_owned());
    }
    if lock.published != Some(false) {
        return Err(
            "local source must keep published=false until remote publication is verified"
                .to_owned(),
        );
    }
    if lock.generated_by.as_deref() != Some("standards-sync/1") {
        return Err("lock generated_by must be standards-sync/1".to_owned());
    }
    if lock.protected_paths.is_empty() || !unique(&lock.protected_paths) {
        return Err("protected_paths must be non-empty and unique".to_owned());
    }
    for path in &lock.protected_paths {
        if !path.starts_with("standards/") || !valid_relative_path(path) {
            return Err(format!("unsafe protected path `{path}`"));
        }
    }
    let mut previous: Option<&str> = None;
    for (path, digest) in &lock.files {
        if !path.starts_with("standards/") || !valid_relative_path(path) {
            return Err(format!("unsafe lock path `{path}`"));
        }
        if !valid_hex_digest(digest) {
            return Err(format!("invalid digest for `{path}`"));
        }
        if previous.is_some_and(|old| old >= path.as_str()) {
            return Err("lock files must be sorted and unique".to_owned());
        }
        previous = Some(path);
    }
    Ok(())
}

fn validate_lock_bytes(root: &Path, lock: &LockFile) -> Result<()> {
    let mut bundle_input = Vec::new();
    for (path, expected) in &lock.files {
        let full = safe_join(root, path)?;
        require_regular_file(&full)?;
        let bytes =
            fs::read(&full).map_err(|error| format!("cannot read {}: {error}", full.display()))?;
        let actual = sha256_hex(&bytes);
        if &actual != expected {
            return Err(format!(
                "digest mismatch for {path}: expected {expected}, got {actual}"
            ));
        }
        bundle_input.extend_from_slice(path.as_bytes());
        bundle_input.push(0);
        bundle_input.extend_from_slice(&bytes);
        bundle_input.push(0);
    }
    let actual_bundle = format!("sha256:{}", sha256_hex(&bundle_input));
    if Some(actual_bundle.as_str()) != lock.bundle_digest.as_deref() {
        return Err(format!(
            "bundle digest mismatch: expected {}, got {actual_bundle}",
            lock.bundle_digest.as_deref().unwrap_or("")
        ));
    }

    let standards = root.join("standards");
    let mut actual_files = Vec::new();
    collect_files(&standards, &standards, &mut actual_files)?;
    actual_files.sort();
    let locked: Vec<String> = lock.files.iter().map(|(path, _)| path.clone()).collect();
    if actual_files != locked {
        return Err(format!(
            "lock inventory differs from local standards files: expected {} entries, found {}",
            locked.len(),
            actual_files.len()
        ));
    }
    Ok(())
}

fn validate_rules(path: &Path) -> Result<()> {
    let text = read_text(path)?;
    if !text.lines().any(|line| line.trim() == "schema_version: 1")
        || !text.lines().any(|line| line.trim() == "rules:")
    {
        return Err(format!(
            "{} must declare schema_version 1 and rules",
            path.display()
        ));
    }
    let mut records: Vec<BTreeMap<String, String>> = Vec::new();
    for raw in text.lines() {
        let line = raw.trim();
        if let Some(value) = line.strip_prefix("- id:") {
            records.push(BTreeMap::from([("id".to_owned(), value.trim().to_owned())]));
        } else if let Some((key, value)) = line.split_once(':') {
            if let Some(record) = records.last_mut() {
                let key = key.trim();
                if matches!(
                    key,
                    "title"
                        | "purpose"
                        | "severity"
                        | "classification"
                        | "check"
                        | "command"
                        | "exception_eligible"
                        | "failure_behavior"
                ) {
                    record.insert(key.to_owned(), value.trim().to_owned());
                }
            }
        }
    }
    if records.len() < 8 {
        return Err(format!("{} has too few rules", path.display()));
    }
    let mut ids = BTreeSet::new();
    let required = [
        "X-ID-001",
        "X-VER-001",
        "X-AUTH-001",
        "X-ERR-001",
        "X-LIFE-001",
        "X-TIME-001",
        "X-PRIV-001",
        "X-OWN-001",
    ];
    for record in &records {
        let id = record
            .get("id")
            .ok_or_else(|| "rule is missing id".to_owned())?;
        if !valid_rule_id(id) || !ids.insert(id.clone()) {
            return Err(format!("invalid or duplicate rule id `{id}`"));
        }
        for key in [
            "title",
            "purpose",
            "severity",
            "classification",
            "check",
            "command",
            "exception_eligible",
            "failure_behavior",
        ] {
            if !record.contains_key(key) {
                return Err(format!("rule {id} is missing {key}"));
            }
        }
        let severity = record.get("severity").map(String::as_str).unwrap_or("");
        let classification = record
            .get("classification")
            .map(String::as_str)
            .unwrap_or("");
        let failure = record
            .get("failure_behavior")
            .map(String::as_str)
            .unwrap_or("");
        if severity == "mandatory" && (classification != "blocking" || failure != "reject") {
            return Err(format!("mandatory rule {id} is not blocking/rejecting"));
        }
        if severity != "mandatory" && severity != "advisory" {
            return Err(format!("rule {id} has unknown severity"));
        }
    }
    for id in required {
        if !ids.contains(id) {
            return Err(format!("canonical rule {id} is missing"));
        }
    }
    Ok(())
}

fn validate_profile_catalog(path: &Path) -> Result<BTreeSet<String>> {
    let text = read_text(path)?;
    if !text.lines().any(|line| line.trim() == "schema_version: 1") {
        return Err(format!("{} must declare schema_version 1", path.display()));
    }
    let mut ids = BTreeSet::new();
    let mut records: Vec<BTreeMap<String, String>> = Vec::new();
    for raw in text.lines() {
        let line = raw.trim();
        if let Some(value) = line.strip_prefix("- id:") {
            records.push(BTreeMap::from([("id".to_owned(), value.trim().to_owned())]));
        } else if let Some((key, value)) = line.split_once(':') {
            if let Some(record) = records.last_mut() {
                record.insert(key.trim().to_owned(), value.trim().to_owned());
            }
        }
    }
    if records.is_empty() {
        return Err(format!("{} contains no profiles", path.display()));
    }
    for record in records {
        let id = record
            .get("id")
            .ok_or_else(|| "profile is missing id".to_owned())?;
        if !valid_profile_id(id) || !ids.insert(id.clone()) {
            return Err(format!("invalid or duplicate catalog profile `{id}`"));
        }
    }
    Ok(ids)
}

fn validate_repository_map(path: &Path, profile_ids: &BTreeSet<String>) -> Result<()> {
    let text = read_text(path)?;
    if !text.lines().any(|line| line.trim() == "schema_version: 1") {
        return Err(format!("{} must declare schema_version 1", path.display()));
    }
    let mut records: Vec<RepoEntry> = Vec::new();
    for raw in text.lines() {
        let line = raw.trim();
        if let Some(value) = line.strip_prefix("- repository:") {
            records.push(RepoEntry {
                repository: value.trim().to_owned(),
                ..RepoEntry::default()
            });
            continue;
        }
        let Some((key, value)) = line.split_once(':') else {
            continue;
        };
        let Some(record) = records.last_mut() else {
            continue;
        };
        let value = value.trim();
        match key.trim() {
            "repository_id" | "node_id" | "default_branch" | "baseline_commit" | "owner"
            | "profile_id" | "adoption" => match key.trim() {
                "repository_id" => record.repository_id = value.to_owned(),
                "node_id" => record.node_id = value.to_owned(),
                "default_branch" => record.default_branch = value.to_owned(),
                "baseline_commit" => record.baseline_commit = value.to_owned(),
                "owner" => record.owner = value.to_owned(),
                "profile_id" => record.profile_id = value.to_owned(),
                "adoption" => record.adoption = value.to_owned(),
                _ => unreachable!(),
            },
            "exclusion_reason" => {
                record.exclusion_reason = if value == "null" {
                    None
                } else {
                    Some(value.to_owned())
                }
            }
            _ => {}
        }
    }
    if records.len() != 13 {
        return Err(format!(
            "repository map must contain exactly 13 records, found {}",
            records.len()
        ));
    }
    let expected: BTreeSet<&str> = [
        "AI-Ascension/aiascension.tech",
        "AI-Ascension/sts2-game-core",
        "AI-Ascension/sts2-game-mod",
        "AI-Ascension/sts2-gateway",
        "AI-Ascension/sts2-mcp-server",
        "AI-Ascension/sts2-harness",
        "AI-Ascension/sts2-protocol",
        "AI-Ascension/.github",
        "AI-Ascension/AI-Ascension.github.io",
        "AI-Ascension/ai-agent-observability",
        "AI-Ascension/ascension-watchdog",
        "AI-Ascension/ascension-map-visualizer",
        "AI-Ascension/ascension-brand-overhaul",
    ]
    .into_iter()
    .collect();
    let actual: BTreeSet<&str> = records
        .iter()
        .map(|record| record.repository.as_str())
        .collect();
    if actual != expected {
        return Err("repository map does not match the 13 reviewed repositories".to_owned());
    }
    for record in records {
        if record.repository_id.parse::<u64>().is_err()
            || record.node_id.is_empty()
            || record.default_branch.is_empty()
            || !valid_commit(&record.baseline_commit)
            || !is_upper_identifier(&record.owner)
            || !profile_ids.contains(&record.profile_id)
        {
            return Err(format!(
                "incomplete repository record for {}",
                record.repository
            ));
        }
        if !matches!(record.adoption.as_str(), "ready" | "prepared" | "excluded") {
            return Err(format!("unknown adoption state for {}", record.repository));
        }
        if record.adoption == "excluded"
            && record.exclusion_reason.as_deref().is_none_or(str::is_empty)
        {
            return Err(format!(
                "excluded repository {} needs a reason",
                record.repository
            ));
        }
        if record.adoption != "excluded" && record.exclusion_reason.is_some() {
            return Err(format!(
                "non-excluded repository {} has an exclusion reason",
                record.repository
            ));
        }
    }
    Ok(())
}

fn validate_schemas(directory: &Path) -> Result<()> {
    require_directory(directory)?;
    let required = [
        "rule.schema.json",
        "rules.schema.json",
        "profile.schema.json",
        "lock.schema.json",
        "repositories.schema.json",
        "profiles.schema.json",
        "exception.schema.json",
    ];
    let mut ids = BTreeSet::new();
    for name in required {
        let path = directory.join(name);
        require_regular_file(&path)?;
        let text = read_text(&path)?;
        if !looks_like_json(&text) || !text.contains("\"$schema\"") || !text.contains("\"$id\"") {
            return Err(format!(
                "{} is not a self-identifying JSON schema",
                path.display()
            ));
        }
        let id = json_string_any(&text, "$id")?;
        if !ids.insert(id) {
            return Err(format!("duplicate schema $id in {}", path.display()));
        }
    }
    Ok(())
}

fn validate_conformance(directory: &Path) -> Result<()> {
    require_directory(directory)?;
    let required = [
        "valid-profile.toml",
        "valid-lock.json",
        "valid-exception.yaml",
        "invalid-profile-floating.toml",
        "invalid-profile-missing-source.toml",
        "invalid-lock-traversal.json",
        "invalid-lock-published.json",
        "invalid-exception-pending.yaml",
        "invalid-exception-broad-path.yaml",
    ];
    for name in required {
        require_regular_file(&directory.join(name))?;
    }
    Ok(())
}

fn fixture_check(directory: &Path) -> Result<()> {
    require_directory(directory)?;
    let valid_profile = parse_profile(&directory.join("valid-profile.toml"))?;
    validate_profile(&valid_profile)?;
    let valid_lock = parse_lock(&directory.join("valid-lock.json"))?;
    validate_lock_shape(&valid_lock, &valid_profile)?;
    let valid_exception = parse_exception(&directory.join("valid-exception.yaml"))?;
    validate_exception(&valid_exception)?;

    let negative_profiles = [
        "invalid-profile-floating.toml",
        "invalid-profile-missing-source.toml",
    ];
    for name in negative_profiles {
        let result =
            parse_profile(&directory.join(name)).and_then(|profile| validate_profile(&profile));
        if result.is_ok() {
            return Err(format!("negative fixture {name} was accepted"));
        }
    }
    let negative_locks = ["invalid-lock-traversal.json", "invalid-lock-published.json"];
    for name in negative_locks {
        let result = parse_lock(&directory.join(name))
            .and_then(|lock| validate_lock_shape(&lock, &valid_profile));
        if result.is_ok() {
            return Err(format!("negative fixture {name} was accepted"));
        }
    }
    let negative_exceptions = [
        "invalid-exception-pending.yaml",
        "invalid-exception-broad-path.yaml",
    ];
    for name in negative_exceptions {
        let result = parse_exception(&directory.join(name))
            .and_then(|exception| validate_exception(&exception));
        if result.is_ok() {
            return Err(format!("negative fixture {name} was accepted"));
        }
    }
    println!("fixture-check passed: 3 valid fixtures accepted, 6 negative fixtures rejected");
    Ok(())
}

#[derive(Debug, Default)]
struct Exception {
    id: String,
    rule_ids: Vec<String>,
    paths: Vec<String>,
    owner: String,
    rationale: String,
    tests: Vec<String>,
    reviewer: String,
    record: String,
    status: String,
    reviewed_on: String,
    expires_on: String,
    removal_criteria: String,
}

fn parse_exception(path: &Path) -> Result<Exception> {
    let text = read_text(path)?;
    let mut result = Exception::default();
    let mut section = String::new();
    for raw in text.lines() {
        let indentation = raw.len() - raw.trim_start().len();
        let line = strip_comment(raw).trim().to_owned();
        if line.is_empty() {
            continue;
        }
        if indentation == 0 && line.ends_with(':') && !line.contains(' ') {
            section = line.trim_end_matches(':').to_owned();
            continue;
        }
        if indentation == 0 {
            section.clear();
        }
        let Some((key, value)) = line.split_once(':') else {
            return Err(format!("{} has malformed YAML", path.display()));
        };
        let key = key.trim();
        let value = value.trim();
        match (section.as_str(), key) {
            ("", "id") => result.id = value.to_owned(),
            ("", "rule_ids") => result.rule_ids = parse_yaml_array(value)?,
            ("", "paths") => result.paths = parse_yaml_array(value)?,
            ("", "owner") => result.owner = value.to_owned(),
            ("", "rationale") => result.rationale = value.to_owned(),
            ("", "compensating_tests") => result.tests = parse_yaml_array(value)?,
            ("", "reviewed_on") => result.reviewed_on = value.to_owned(),
            ("", "expires_on") => result.expires_on = value.to_owned(),
            ("", "removal_criteria") => result.removal_criteria = value.to_owned(),
            ("approval", "reviewer") => result.reviewer = value.to_owned(),
            ("approval", "record") => result.record = value.to_owned(),
            ("approval", "status") => result.status = value.to_owned(),
            _ => {
                return Err(format!(
                    "{} has unknown exception field {section}.{key}",
                    path.display()
                ));
            }
        }
    }
    Ok(result)
}

fn validate_exception(exception: &Exception) -> Result<()> {
    if !exception.id.starts_with("EXC-")
        || exception.rule_ids.is_empty()
        || exception.paths.is_empty()
        || exception.owner.is_empty()
        || exception.rationale.len() < 20
        || exception.tests.is_empty()
        || exception.reviewer.is_empty()
        || exception.status != "approved"
        || exception.reviewed_on.is_empty()
        || exception.expires_on.is_empty()
        || exception.removal_criteria.len() < 10
    {
        return Err("exception is missing required approval evidence".to_owned());
    }
    if exception.record == "pending"
        || exception.record == "self"
        || (!exception.record.starts_with("local-review:")
            && !exception
                .record
                .starts_with("https://github.com/AI-Ascension/"))
    {
        return Err("exception approval record is not a verifiable review reference".to_owned());
    }
    for rule in &exception.rule_ids {
        if !valid_rule_id(rule) {
            return Err(format!("invalid exception rule {rule}"));
        }
    }
    for path in &exception.paths {
        if !valid_relative_path(path) || path == "." {
            return Err(format!("exception path is not exact and relative: {path}"));
        }
    }
    Ok(())
}

fn sync_bundle(args: &Cli) -> Result<()> {
    let source_root = args.source_root.canonicalize().map_err(|error| {
        format!(
            "cannot read source root {}: {error}",
            args.source_root.display()
        )
    })?;
    let target_root = if args.target_root.as_os_str().is_empty() {
        return Err("--target-root is required for sync".to_owned());
    } else {
        args.target_root.clone()
    };
    if !valid_repository(&args.repository)
        || !valid_profile_id(&args.profile_id)
        || !is_upper_identifier(&args.owner)
        || !valid_commit(&args.source_commit)
    {
        return Err("sync repository, profile, owner, or source commit is invalid".to_owned());
    }
    let source_standards = source_root.join("standards");
    require_directory(&source_standards)?;
    let target_root = if target_root.exists() {
        target_root
            .canonicalize()
            .map_err(|error| format!("cannot read target root: {error}"))?
    } else {
        fs::create_dir_all(&target_root)
            .map_err(|error| format!("cannot create target root: {error}"))?;
        target_root
            .canonicalize()
            .map_err(|error| format!("cannot resolve target root: {error}"))?
    };
    if source_root == target_root {
        return Err("source and target roots must differ".to_owned());
    }

    let mut files = Vec::new();
    collect_files(&source_standards, &source_standards, &mut files)?;
    files.sort();
    let mut entries = Vec::new();
    let mut bundle_input = Vec::new();
    for path in files {
        let source_path = source_root.join(&path);
        let target_path = target_root.join(&path);
        let bytes = fs::read(&source_path)
            .map_err(|error| format!("cannot read {}: {error}", source_path.display()))?;
        copy_if_absent_or_equal(&target_path, &bytes)?;
        let digest = sha256_hex(&bytes);
        entries.push((path.clone(), digest));
        bundle_input.extend_from_slice(path.as_bytes());
        bundle_input.push(0);
        bundle_input.extend_from_slice(&bytes);
        bundle_input.push(0);
    }
    let bundle_digest = format!("sha256:{}", sha256_hex(&bundle_input));
    let profile = generated_profile(
        &args.profile_id,
        &args.repository,
        &args.owner,
        &args.source_commit,
        &bundle_digest,
    )?;
    let lock = generated_lock(
        &args.repository,
        &args.profile_id,
        &args.source_commit,
        &bundle_digest,
        &entries,
    );
    copy_if_absent_or_equal(
        &target_root.join("standards-profile.toml"),
        profile.as_bytes(),
    )?;
    copy_if_absent_or_equal(&target_root.join("standards.lock.json"), lock.as_bytes())?;
    println!(
        "synced {} files to {} bundle_digest={bundle_digest} published=false",
        entries.len(),
        target_root.display()
    );
    Ok(())
}

fn generated_profile(
    profile_id: &str,
    repository: &str,
    owner: &str,
    commit: &str,
    digest: &str,
) -> Result<String> {
    let (scopes, fast, required, extended) = match profile_id {
        "rust-pure" => (
            "rust, json, contracts",
            "git-diff-check, standards-validate, cargo-metadata, cargo-fmt",
            "repo-policy-strict, cargo-clippy, cargo-test, artifact-checksums",
            "contract-conformance",
        ),
        "rust-service" => (
            "rust, json, contracts",
            "git-diff-check, standards-validate, cargo-metadata, cargo-fmt",
            "repo-policy-strict, cargo-clippy, cargo-test, artifact-checksums",
            "contract-conformance, synthetic-boundary-tests",
        ),
        "rust-managed" => (
            "rust, csharp, shell, json, contracts",
            "git-diff-check, standards-validate, cargo-metadata, cargo-fmt",
            "repo-policy-strict, cargo-clippy, cargo-test, artifact-checksums, managed-source-probes",
            "managed-bridge-tests, exact-host-build",
        ),
        "web-php" => (
            "html, css, javascript, php",
            "git-diff-check, standards-validate, composer-validate",
            "phpunit, origin-regressions, persistence-regressions",
            "browser-check",
        ),
        "web-static" => (
            "html, css, javascript, rust",
            "git-diff-check, standards-validate, node-tests",
            "fixture-integrity, local-link-check",
            "browser-check, pinned-recipe",
        ),
        "operations" => (
            "shell, yaml, dockerfile, systemd",
            "git-diff-check, standards-validate, bash-n, shellcheck",
            "compose-invariants, compose-config, dockerfile-check",
            "synthetic-bootstrap",
        ),
        "planning-bootstrap" => (
            "markdown, json, rust-planned, browser-planned",
            "git-diff-check, standards-validate, package-shape",
            "",
            "",
        ),
        "brand-package" => (
            "python, html, json, markdown",
            "git-diff-check, standards-validate, python-syntax",
            "package-validation, unit-tests, schema-meta-validation",
            "offline-art-board",
        ),
        "org-governance" => (
            "markdown, yaml, json, rust",
            "git-diff-check, standards-validate",
            "standards-lock, schema-shape",
            "link-check",
        ),
        _ => return Err(format!("no generated profile template for {profile_id}")),
    };
    let list = |value: &str| {
        if value.is_empty() {
            "[]".to_owned()
        } else {
            format!(
                "[{}]",
                value
                    .split(", ")
                    .map(|item| format!("\"{item}\""))
                    .collect::<Vec<_>>()
                    .join(", ")
            )
        }
    };
    Ok(format!(
        "schema_version = 1\nprofile_id = \"{profile_id}\"\nrepository = \"{repository}\"\nowner = \"{owner}\"\nsource_bundle = \"AI-Ascension/.github\"\nsource_commit = \"{commit}\"\nsource_digest = \"{digest}\"\ndistribution = \"local\"\nscopes = [{}]\n\n[checks]\nfast = {}\nrequired = {}\nextended = {}\n\n[evidence]\nruntime = \"unverified\"\ndeployment = \"unverified\"\nprovider = \"unverified\"\n\n[exceptions]\nfile = \"\"\nstatus = \"none\"\n",
        scopes
            .split(", ")
            .map(|item| format!("\"{item}\""))
            .collect::<Vec<_>>()
            .join(", "),
        list(fast),
        list(required),
        list(extended)
    ))
}

fn generated_lock(
    repository: &str,
    profile_id: &str,
    commit: &str,
    digest: &str,
    files: &[(String, String)],
) -> String {
    let files_text = files
        .iter()
        .map(|(path, hash)| format!("    {{\"path\": \"{path}\", \"sha256\": \"{hash}\"}}"))
        .collect::<Vec<_>>()
        .join(",\n");
    format!(
        "{{\n  \"lock_version\": 1,\n  \"repository\": \"{repository}\",\n  \"profile_id\": \"{profile_id}\",\n  \"source\": {{\n    \"repository\": \"AI-Ascension/.github\",\n    \"commit\": \"{commit}\",\n    \"bundle_digest\": \"{digest}\",\n    \"distribution\": \"local\",\n    \"published\": false\n  }},\n  \"files\": [\n{files_text}\n  ],\n  \"protected_paths\": [\"standards/schemas\", \"standards/conformance\"],\n  \"generated_by\": \"standards-sync/1\"\n}}\n"
    )
}

fn copy_if_absent_or_equal(path: &Path, bytes: &[u8]) -> Result<()> {
    if path.exists() {
        require_regular_file(path)?;
        let existing =
            fs::read(path).map_err(|error| format!("cannot read {}: {error}", path.display()))?;
        if existing != bytes {
            return Err(format!(
                "refusing to overwrite differing managed file {}",
                path.display()
            ));
        }
        return Ok(());
    }
    let parent = path
        .parent()
        .ok_or_else(|| format!("managed path has no parent: {}", path.display()))?;
    fs::create_dir_all(parent)
        .map_err(|error| format!("cannot create {}: {error}", parent.display()))?;
    fs::write(path, bytes).map_err(|error| format!("cannot write {}: {error}", path.display()))
}

fn collect_files(root: &Path, directory: &Path, output: &mut Vec<String>) -> Result<()> {
    let mut entries = fs::read_dir(directory)
        .map_err(|error| format!("cannot list {}: {error}", directory.display()))?
        .collect::<io::Result<Vec<_>>>()
        .map_err(|error| format!("cannot read directory {}: {error}", directory.display()))?;
    entries.sort_by_key(|entry| entry.file_name());
    for entry in entries {
        let path = entry.path();
        let metadata = fs::symlink_metadata(&path)
            .map_err(|error| format!("cannot inspect {}: {error}", path.display()))?;
        if metadata.file_type().is_symlink() {
            return Err(format!(
                "symlink is not allowed in standards bundle: {}",
                path.display()
            ));
        }
        if metadata.is_dir() {
            collect_files(root, &path, output)?;
        } else if metadata.is_file() {
            let relative = path
                .strip_prefix(root)
                .map_err(|error| format!("cannot relativize {}: {error}", path.display()))?;
            output.push(format!(
                "standards/{}",
                relative.to_string_lossy().replace('\\', "/")
            ));
        } else {
            return Err(format!("unsupported standards entry {}", path.display()));
        }
    }
    Ok(())
}

fn safe_join(root: &Path, relative: &str) -> Result<PathBuf> {
    if !valid_relative_path(relative) {
        return Err(format!("unsafe path `{relative}`"));
    }
    let path = root.join(relative);
    let parent = path
        .parent()
        .ok_or_else(|| format!("path has no parent: {relative}"))?;
    let canonical_parent = parent
        .canonicalize()
        .map_err(|error| format!("cannot resolve {}: {error}", parent.display()))?;
    let canonical_root = root
        .canonicalize()
        .map_err(|error| format!("cannot resolve {}: {error}", root.display()))?;
    if !canonical_parent.starts_with(&canonical_root) {
        return Err(format!("path escapes root: {relative}"));
    }
    Ok(path)
}

fn require_directory(path: &Path) -> Result<()> {
    let metadata = fs::symlink_metadata(path)
        .map_err(|error| format!("missing directory {}: {error}", path.display()))?;
    if !metadata.is_dir() || metadata.file_type().is_symlink() {
        return Err(format!("{} is not a real directory", path.display()));
    }
    Ok(())
}
fn require_regular_file(path: &Path) -> Result<()> {
    let metadata = fs::symlink_metadata(path)
        .map_err(|error| format!("missing file {}: {error}", path.display()))?;
    if !metadata.is_file() || metadata.file_type().is_symlink() {
        return Err(format!("{} is not a regular file", path.display()));
    }
    Ok(())
}
fn read_text(path: &Path) -> Result<String> {
    let bytes =
        fs::read(path).map_err(|error| format!("cannot read {}: {error}", path.display()))?;
    String::from_utf8(bytes).map_err(|error| format!("{} is not UTF-8: {error}", path.display()))
}
fn required<'a, T>(value: &'a Option<T>, name: &str) -> Result<&'a T> {
    value.as_ref().ok_or_else(|| format!("{name} is required"))
}
fn unique(values: &[String]) -> bool {
    let mut set = BTreeSet::new();
    values.iter().all(|value| set.insert(value))
}
fn valid_commit(value: &str) -> bool {
    value.len() == 40
        && value
            .bytes()
            .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
}
fn valid_hex_digest(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
}
fn valid_prefixed_digest(value: &str) -> bool {
    value.strip_prefix("sha256:").is_some_and(valid_hex_digest)
}
fn valid_repository(value: &str) -> bool {
    let Some(name) = value.strip_prefix("AI-Ascension/") else {
        return false;
    };
    !name.is_empty()
        && name
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'.' | b'_' | b'-'))
}
fn valid_profile_id(value: &str) -> bool {
    (3..=49).contains(&value.len())
        && value.as_bytes().first().is_some_and(u8::is_ascii_lowercase)
        && value
            .bytes()
            .all(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'-')
}
fn valid_scope(value: &str) -> bool {
    !value.is_empty()
        && value.bytes().all(|byte| {
            byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'_' || byte == b'-'
        })
}
fn valid_check_name(value: &str) -> bool {
    !value.is_empty()
        && value.bytes().all(|byte| {
            byte.is_ascii_lowercase()
                || byte.is_ascii_digit()
                || matches!(byte, b'.' | b'_' | b':' | b'-')
        })
}
fn is_upper_identifier(value: &str) -> bool {
    (2..=16).contains(&value.len())
        && value
            .bytes()
            .all(|byte| byte.is_ascii_uppercase() || byte.is_ascii_digit() || byte == b'_')
}
fn valid_rule_id(value: &str) -> bool {
    let parts = value.split('-').collect::<Vec<_>>();
    parts.len() == 3
        && matches!(parts[0], "X" | "RUST" | "MANAGED" | "WEB" | "OPS" | "DOC")
        && !parts[1].is_empty()
        && parts[1]
            .bytes()
            .all(|byte| byte.is_ascii_uppercase() || byte.is_ascii_digit())
        && parts[2].len() == 3
        && parts[2].bytes().all(|byte| byte.is_ascii_digit())
}
fn valid_relative_path(value: &str) -> bool {
    !value.is_empty()
        && value != "."
        && !value.starts_with('/')
        && !value.contains('\\')
        && !value
            .split('/')
            .any(|part| part.is_empty() || part == "." || part == "..")
        && value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'.' | b'_' | b'/' | b'-'))
}
fn strip_comment(value: &str) -> &str {
    let mut quoted = false;
    for (index, byte) in value.bytes().enumerate() {
        if byte == b'"' {
            quoted = !quoted;
        } else if byte == b'#' && !quoted {
            return &value[..index];
        }
    }
    value
}
fn parse_string(value: &str, path: &Path, line: usize) -> Result<String> {
    if value.len() >= 2 && value.starts_with('"') && value.ends_with('"') {
        Ok(value[1..value.len() - 1]
            .replace("\\\"", "\"")
            .replace("\\\\", "\\"))
    } else {
        Err(format!(
            "{}:{}: expected quoted string",
            path.display(),
            line + 1
        ))
    }
}
fn parse_u32(value: &str, path: &Path, line: usize) -> Result<u32> {
    value
        .parse()
        .map_err(|error| format!("{}:{}: invalid integer: {error}", path.display(), line + 1))
}
fn parse_array(value: &str, path: &Path, line: usize) -> Result<Vec<String>> {
    if !value.starts_with('[') || !value.ends_with(']') {
        return Err(format!("{}:{}: expected array", path.display(), line + 1));
    }
    let inner = value[1..value.len() - 1].trim();
    if inner.is_empty() {
        return Ok(Vec::new());
    }
    inner
        .split(',')
        .map(|item| parse_string(item.trim(), path, line))
        .collect()
}
fn parse_yaml_array(value: &str) -> Result<Vec<String>> {
    if !value.starts_with('[') || !value.ends_with(']') {
        return Err("expected YAML inline array".to_owned());
    }
    let inner = value[1..value.len() - 1].trim();
    if inner.is_empty() {
        return Ok(Vec::new());
    }
    Ok(inner
        .split(',')
        .map(|item| item.trim().trim_matches('"').to_owned())
        .collect())
}

fn looks_like_json(text: &str) -> bool {
    let trimmed = text.trim();
    trimmed.starts_with('{') && trimmed.ends_with('}') && !text.contains('\0')
}
fn json_string_any(text: &str, key: &str) -> Result<String> {
    for line in text.lines() {
        if line.contains(&format!("\"{key}\"")) {
            return json_string_after_key(line, key);
        }
    }
    Err(format!("JSON key `{key}` is missing"))
}
fn json_string_at_indent(text: &str, key: &str, indent: usize) -> Result<String> {
    let prefix = " ".repeat(indent);
    for line in text.lines() {
        if line.starts_with(&prefix)
            && !line.starts_with(&(prefix.clone() + " "))
            && line.trim_start().starts_with(&format!("\"{key}\""))
        {
            return json_string_after_key(line, key);
        }
    }
    Err(format!("JSON key `{key}` at indent {indent} is missing"))
}
fn json_bool_at_indent(text: &str, key: &str, indent: usize) -> Result<bool> {
    let prefix = " ".repeat(indent);
    for line in text.lines() {
        if line.starts_with(&prefix)
            && !line.starts_with(&(prefix.clone() + " "))
            && line.trim_start().starts_with(&format!("\"{key}\""))
        {
            let value = line
                .split_once(':')
                .map(|(_, value)| value.trim().trim_end_matches(','))
                .ok_or_else(|| format!("JSON key `{key}` malformed"))?;
            return match value {
                "true" => Ok(true),
                "false" => Ok(false),
                _ => Err(format!("JSON key `{key}` is not boolean")),
            };
        }
    }
    Err(format!("JSON key `{key}` at indent {indent} is missing"))
}
fn json_u32(text: &str, key: &str, indent: usize) -> Result<u32> {
    let prefix = " ".repeat(indent);
    for line in text.lines() {
        if line.starts_with(&prefix)
            && !line.starts_with(&(prefix.clone() + " "))
            && line.trim_start().starts_with(&format!("\"{key}\""))
        {
            let value = line
                .split_once(':')
                .map(|(_, value)| value.trim().trim_end_matches(','))
                .ok_or_else(|| format!("JSON key `{key}` malformed"))?;
            return value
                .parse()
                .map_err(|error| format!("JSON key `{key}` is not an integer: {error}"));
        }
    }
    Err(format!("JSON key `{key}` at indent {indent} is missing"))
}
fn json_array_at_indent(text: &str, key: &str, indent: usize) -> Result<Vec<String>> {
    let prefix = " ".repeat(indent);
    for line in text.lines() {
        if line.starts_with(&prefix)
            && !line.starts_with(&(prefix.clone() + " "))
            && line.trim_start().starts_with(&format!("\"{key}\""))
        {
            let value = line
                .split_once(':')
                .map(|(_, value)| value.trim())
                .ok_or_else(|| format!("JSON key `{key}` malformed"))?;
            let value = value.trim_end_matches(',');
            if !value.starts_with('[') || !value.ends_with(']') {
                return Err(format!("JSON key `{key}` is not an inline array"));
            }
            let inner = value[1..value.len() - 1].trim();
            if inner.is_empty() {
                return Ok(Vec::new());
            }
            return inner
                .split(',')
                .map(|item| {
                    let item = item.trim();
                    if item.len() < 2 || !item.starts_with('"') || !item.ends_with('"') {
                        return Err(format!("JSON array `{key}` has an invalid string"));
                    }
                    Ok(item[1..item.len() - 1].to_owned())
                })
                .collect();
        }
    }
    Err(format!("JSON key `{key}` at indent {indent} is missing"))
}
fn json_string_after_key(line: &str, key: &str) -> Result<String> {
    let needle = format!("\"{key}\"");
    let start = line
        .find(&needle)
        .ok_or_else(|| format!("JSON key `{key}` missing"))?
        + needle.len();
    let rest = line[start..].trim_start();
    let rest = rest
        .strip_prefix(':')
        .ok_or_else(|| format!("JSON key `{key}` has no colon"))?
        .trim_start();
    if !rest.starts_with('"') {
        return Err(format!("JSON key `{key}` is not a string"));
    }
    let mut escaped = false;
    for (offset, byte) in rest.as_bytes().iter().enumerate().skip(1) {
        if *byte == b'"' && !escaped {
            return Ok(rest[1..offset].replace("\\\"", "\"").replace("\\\\", "\\"));
        }
        escaped = *byte == b'\\' && !escaped;
        if *byte != b'\\' {
            escaped = false;
        }
    }
    Err(format!("JSON key `{key}` has an unterminated string"))
}

// SHA-256 is included so validation and sync stay dependency-free and offline.
fn sha256_hex(input: &[u8]) -> String {
    let mut h: [u32; 8] = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab,
        0x5be0cd19,
    ];
    let mut data = input.to_vec();
    let bit_len = (data.len() as u64) * 8;
    data.push(0x80);
    while data.len() % 64 != 56 {
        data.push(0);
    }
    data.extend_from_slice(&bit_len.to_be_bytes());
    const K: [u32; 64] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
        0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,
        0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
        0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
        0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
        0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116,
        0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7,
        0xc67178f2,
    ];
    for chunk in data.chunks_exact(64) {
        let mut w = [0u32; 64];
        for index in 0..16 {
            w[index] = u32::from_be_bytes([
                chunk[index * 4],
                chunk[index * 4 + 1],
                chunk[index * 4 + 2],
                chunk[index * 4 + 3],
            ]);
        }
        for index in 16..64 {
            let s0 = w[index - 15].rotate_right(7)
                ^ w[index - 15].rotate_right(18)
                ^ (w[index - 15] >> 3);
            let s1 = w[index - 2].rotate_right(17)
                ^ w[index - 2].rotate_right(19)
                ^ (w[index - 2] >> 10);
            w[index] = w[index - 16]
                .wrapping_add(s0)
                .wrapping_add(w[index - 7])
                .wrapping_add(s1);
        }
        let (mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut hh) =
            (h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]);
        for index in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ ((!e) & g);
            let temp1 = hh
                .wrapping_add(s1)
                .wrapping_add(ch)
                .wrapping_add(K[index])
                .wrapping_add(w[index]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let temp2 = s0.wrapping_add(maj);
            hh = g;
            g = f;
            f = e;
            e = d.wrapping_add(temp1);
            d = c;
            c = b;
            b = a;
            a = temp1.wrapping_add(temp2);
        }
        h[0] = h[0].wrapping_add(a);
        h[1] = h[1].wrapping_add(b);
        h[2] = h[2].wrapping_add(c);
        h[3] = h[3].wrapping_add(d);
        h[4] = h[4].wrapping_add(e);
        h[5] = h[5].wrapping_add(f);
        h[6] = h[6].wrapping_add(g);
        h[7] = h[7].wrapping_add(hh);
    }
    h.iter().map(|word| format!("{word:08x}")).collect()
}
