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
src/soc2_rules/
├── cli.py              # the `soc2-logging` console script: semgrep flags + dir-scan excludes
└── rules/
    ├── python/         # one family per file: model_dump.yml, payload_kwargs.yml, ... (services, lambdas)
    └── typescript/     # console_objects.yml, pii_fields.yml (web apps)
tests/
├── python/             # annotated fixtures: # ruleid: / # ok:, basenames mirror rules/
└── typescript/
scripts/                # check_denylist.py, check_suppressions.py — gates run by `just check`
.pre-commit-hooks.yaml  # hook definition consumers reference by `repo:` + tag
.github/workflows/
├── soc2-logging.yml    # reusable workflow (workflow_call) — the required CI check
└── ci.yml              # this repo's own gate: check + consumer-install smoke
docs/
└── AGENTS-snippet.md   # "Logging compliance (SOC2)" section fanned out to consumer AGENTS.md files
```

No application code beyond the console script. No database. Rules, fixtures, two check
scripts, one hook, one reusable workflow, docs.

## Commands

| Command | Purpose |
|---------|---------|
| `just check` | validate + test + denylist + suppressions + package — the single gate, run after every change |
| `just validate` | `semgrep --validate` — rules parse (never add `--quiet`: it hides parse errors) |
| `just test` | `semgrep --test` — fixtures pass |
| `just denylist` | the two PII denylists agree and every documented term is enforced |
| `just suppressions` | no unjustified/bare `nosemgrep` in this repo (+ the checker's self-test) |
| `just package` | the built wheel actually ships every rule file |
| `just smoke` | install the wheel on the lowest supported python and confirm the hook blocks |
| `just scan <path>` | run the pack against a real repo checkout (tuning aid) |

## Rule conventions

- Rule ids are kebab-case with a language segment: `soc2-logging.python.no-model-dump-in-logs`.
- Every rule message: WHAT is banned → WHY (one clause) → the replacement. Agents fix
  violations from the message alone; write it as the prompt you would want.
- `severity: ERROR` for everything blocking. No WARNING rules — warnings train people
  (and agents) to scroll past output.
- **One denylist per pack.** Every branch of a denylist rule binds the same metavariable
  (`$V` — a kwarg name, a kwarg value, a positional arg, an f-string interpolation, a
  dict key or a dict value), so the regex is written once and filtered at the top level.
  Two copies is how `phone_number` reached the kwarg branch but not the f-string branch;
  `scripts/check_denylist.py` now fails if a copy reappears. Semgrep's `--validate`
  rejects a YAML anchor in `regex:`, so the shared metavariable is the mechanism.
- Sinks: `$LOG` matches `logger`/`logging`/`log` with any case and leading underscores
  (`LOGGER`, `_logger`, `self._log`), plus `console` in the TypeScript packs. `$METHOD`
  covers loguru, stdlib, winston and pino levels.
- Every pattern variant has a `# ruleid:` fixture; every legitimate near-miss you decide
  to allow has an `# ok:` fixture. Fixture data is always invented, never production.
  `semgrep --test` pairs a rule file with the fixture of the same basename, so a line
  matched by another family's rule does not affect this family's test.
- False positives in consumer repos are silenced inline with
  `# nosemgrep: <rule-id> — <justification>`; the justification is mandatory, greppable
  (it is the SOC2 exceptions register) and enforced by `scripts/check_suppressions.py`
  inside the required check.

## Consumer integration (what an adopting repo adds — see README for the full walkthrough)

Pre-commit block in each repo's `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/finelo-subpilot/compliance-rules
  rev: v2.0.0
  hooks:
    - id: soc2-logging
```

CI job in each repo's existing workflow:

```yaml
soc2-logging:
  uses: finelo-subpilot/compliance-rules/.github/workflows/soc2-logging.yml@v2
```

The required status check is named `soc2-logging / soc2-logging` (caller job / called
job). Plus the `docs/AGENTS-snippet.md` section appended to the adopting repo's AGENTS.md
so coding agents avoid the patterns instead of tripping the gate.

## Releases

Tag `vMAJOR.MINOR.PATCH` and move the major tag. New blocking rule or widened pattern =
major bump, announced in the internal releases channel. Consumers upgrade via
`pre-commit autoupdate` and the `@v2` major workflow ref.

Two release gates exist because the pack is consumed as a wheel, not as a checkout:
`just package` proves the wheel ships every rule (a rules-less wheel is a silently
disabled gate), and `just smoke` proves the hook installs and blocks on the lowest
supported python (pre-commit builds hook envs with its own interpreter, not this repo's).
`requires-python` therefore tracks semgrep's floor, not the version used for development.
