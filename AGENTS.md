# compliance-rules

Centralized SOC2 logging-compliance gate for finelo-subpilot repos. Semgrep rules that
block PII, tokens, and full-payload dumps from reaching application logs — consumed by
every repo as a pre-commit hook and a required CI check.

Non-negotiable principles: every rule ships with its annotated test corpus (fixture
first, watch it fail); rule messages are fix prompts (WHAT → WHY → replacement);
deterministic and low-noise (tune or delete noisy rules, never demote to warning);
fixtures contain invented data only — never real log lines, payloads, or identifiers.

## What lives here

```
rules/
├── python/             # one family per file: model_dump.yml, payload_kwargs.yml, ... (services, lambdas)
└── typescript/         # console_objects.yml, pii_fields.yml (web apps)
tests/
├── python/             # annotated fixtures: # ruleid: / # ok:, basenames mirror rules/
└── typescript/
.pre-commit-hooks.yaml  # hook definition consumers reference by `repo:` + tag
.github/workflows/
└── soc2-logging.yml    # reusable workflow (workflow_call) — the required CI check
docs/
└── AGENTS-snippet.md   # "Logging compliance (SOC2)" section fanned out to consumer AGENTS.md files
```

No application code. No database. Rules, fixtures, one hook, one workflow, docs.

## Commands

| Command | Purpose |
|---------|---------|
| `just check` | validate + test — the single gate, run after every change |
| `just validate` | `semgrep --validate --config rules/` — rules parse |
| `just test` | `semgrep --test --config rules/ tests/` — fixtures pass |
| `just scan <path>` | run the pack against a real repo checkout (tuning aid) |

## Rule conventions

- Rule ids are kebab-case with a language segment: `soc2-logging.python.no-model-dump-in-logs`.
- Every rule message: WHAT is banned → WHY (one clause) → the replacement. Agents fix
  violations from the message alone; write it as the prompt you would want.
- `severity: ERROR` for everything blocking. No WARNING rules — warnings train people
  (and agents) to scroll past output.
- Every pattern variant has a `# ruleid:` fixture; every legitimate near-miss you decide
  to allow has an `# ok:` fixture. Fixture data is always invented, never production.
- False positives in consumer repos are silenced inline with
  `# nosemgrep: <rule-id> — <justification>`; the justification is mandatory by
  convention and greppable (it is the SOC2 exceptions register).

## Consumer integration (what an adopting repo adds — see README for the full walkthrough)

Pre-commit block in each repo's `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/finelo-subpilot/compliance-rules
  rev: v1.1.0
  hooks:
    - id: soc2-logging
```

CI job in each repo's existing workflow:

```yaml
soc2-logging:
  uses: finelo-subpilot/compliance-rules/.github/workflows/soc2-logging.yml@v1
```

Plus the `docs/AGENTS-snippet.md` section appended to the adopting repo's AGENTS.md
so coding agents avoid the patterns instead of tripping the gate.

## Releases

Tag `vMAJOR.MINOR.PATCH`. New blocking rule or widened pattern = major bump, announced
in the internal releases channel. Consumers upgrade via `pre-commit autoupdate` and the `@v1` major
workflow ref.
