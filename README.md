# compliance-rules

SOC2 logging-compliance gate: semgrep rules that block PII, credentials, and raw
payloads from reaching application logs. Consumed everywhere as a pre-commit hook
(instant, LLM-readable fix prompts) and a required CI check (non-bypassable control).

## Adopt in your repo (self-service, ~5 minutes)

**1. Local gate** — append to `.pre-commit-config.yaml` (create one if absent):

```yaml
  - repo: https://github.com/talgat-abdraimov/compliance-rules
    rev: v2.0.0
    hooks:
      - id: soc2-logging
```

**2. CI check** — add `.github/workflows/soc2-logging.yml`:

```yaml
name: SOC2 logging compliance

on:
  pull_request:

jobs:
  soc2-logging:
    uses: talgat-abdraimov/compliance-rules/.github/workflows/soc2-logging.yml@v2
```

**3. Agent guidance** — append the section from [docs/AGENTS-snippet.md](docs/AGENTS-snippet.md) to your `AGENTS.md` (create the file if absent) so coding agents write compliant logs on the first try.

Then run `pre-commit run soc2-logging --all-files`, fix what it finds (log opaque `_id`s instead of payloads/PII — the rule messages tell you exactly what to change), and make the check required:

```bash
repo=<org>/<repo>
branch=$(gh repo view "$repo" --json defaultBranchRef --jq .defaultBranchRef.name)
gh api -X POST "repos/$repo/branches/$branch/protection/required_status_checks/contexts" \
  -f 'contexts[]=soc2-logging / soc2-logging'
```

The context is `soc2-logging / soc2-logging` — GitHub names a reusable-workflow check
`<caller job> / <called job>`, and a required context that never reports blocks every PR
on "Expected — Waiting for status to be reported". This `POST` **appends**; the
`PATCH .../required_status_checks` form replaces the whole list and would silently
un-require your other checks. Branch protection must already exist on the branch (or
configure the check in a repo ruleset instead).

False positive? `# nosemgrep: <rule-id> — <why>` (justification mandatory and enforced in
CI — it's the SOC2 exceptions register; bare `nosemgrep` fails the build) — better: open a
PR here adding an `# ok:` fixture so the rule learns.

## Upgrading to v2

v2 widens coverage: positional log arguments (`logger.info('to %s', email)`), suffixed
denylist names (`phone_number`), logger aliases (`LOGGER`, `_logger`), `extra={...}`
dicts, `response.json()`, `vars()`/`asdict()`/`json.dumps()`/pydantic-v1 `.dict()`,
TypeScript shorthand properties (`{ email }`), `JSON.stringify`, `console.table/dir` and
winston levels. It also stops flagging LLM token counts (`prompt_tokens`, `max_tokens`),
`len(body)` and latency abbreviations (`p99_lat`).

Expect new findings on first run: bump the rev, run
`pre-commit run soc2-logging --all-files`, and fix or justify what appears.

## Known limits

The gate is a name-based static control on log call sites. It does not catch
`print(...)` (stdout is a log stream in services), string concatenation
(`'to ' + email`), or values embedded in exceptions (`logger.error(f'{e}')` where a
pydantic `ValidationError` carries the offending input). Treat a runtime scrubber in the
logging pipeline as the defence-in-depth backstop, not this gate.

## More

- **Writing/tuning rules** (conventions, fixture-first loop, commands): [AGENTS.md](AGENTS.md)
- **What's banned + the escape hatch**: [docs/AGENTS-snippet.md](docs/AGENTS-snippet.md)
- **Audit evidence**: [docs/exceptions-register.md](docs/exceptions-register.md)

## Versioning

Semver tags plus a moving major tag (`v2`). Consumers pin exact tags in
`.pre-commit-config.yaml` and the major tag in CI (`soc2-logging.yml@v2`). The CI
workflow checks out its own commit (`github.job_workflow_sha`), so the rules always match
the ref the consumer called — rules and workflow cannot drift.

| Change | Release |
|--------|---------|
| New blocking rule, widened pattern, denylist addition | **MAJOR** — announced in the internal releases channel |
| New `# ok:` carve-out, message improvement | MINOR |
| Fixture/doc-only | PATCH |
