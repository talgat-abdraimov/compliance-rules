# compliance-rules

SOC2 logging-compliance gate for finelo-subpilot repos: semgrep rules that block PII,
credentials, and raw payloads from reaching application logs. Consumed everywhere as a
pre-commit hook (instant, LLM-readable fix prompts) and a required CI check
(non-bypassable control).

## Adopt in your repo (self-service, ~5 minutes)

**1. Local gate** — append to `.pre-commit-config.yaml` (create one if absent):

```yaml
  - repo: https://github.com/finelo-subpilot/compliance-rules
    rev: v1.1.0
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
    uses: finelo-subpilot/compliance-rules/.github/workflows/soc2-logging.yml@v1
```

**3. Agent guidance** — append the section from [docs/AGENTS-snippet.md](docs/AGENTS-snippet.md) to your `AGENTS.md` (create the file if absent) so coding agents write compliant logs on the first try.

Then run `pre-commit run soc2-logging --all-files`, fix what it finds (log opaque `_id`s instead of payloads/PII — the rule messages tell you exactly what to change), and make the check required:

```bash
gh api -X PATCH "repos/finelo-subpilot/<repo>/branches/$(gh repo view finelo-subpilot/<repo> --json defaultBranchRef --jq .defaultBranchRef.name)/protection/required_status_checks" -f 'contexts[]=soc2-logging'
```

False positive? `# nosemgrep: <rule-id> — <why>` (justification mandatory — it's the SOC2 exceptions register) — better: open a PR here adding an `# ok:` fixture so the rule learns.

## More

- **Writing/tuning rules** (conventions, fixture-first loop, commands): [AGENTS.md](AGENTS.md)
- **What's banned + the escape hatch**: [docs/AGENTS-snippet.md](docs/AGENTS-snippet.md)
- **Audit evidence**: [docs/exceptions-register.md](docs/exceptions-register.md)

## Versioning

Semver tags plus a moving major tag (`v1`). Consumers pin exact tags in
`.pre-commit-config.yaml` and the major tag in CI (`soc2-logging.yml@v1`) — both
resolve to the same commit lineage, so rules and workflow never drift.

| Change | Release |
|--------|---------|
| New blocking rule, widened pattern, denylist addition | **MAJOR** — announced in the internal releases channel |
| New `# ok:` carve-out, message improvement | MINOR |
| Fixture/doc-only | PATCH |
