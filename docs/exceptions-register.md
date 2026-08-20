# SOC2 exceptions register — audit evidence

The gate's documented-exceptions register is the org-wide set of inline
`nosemgrep` suppressions, each carrying the rule id and a mandatory justification.

The requirement is machine-enforced, not conventional: `scripts/check_suppressions.py`
runs inside the required CI check and fails the build on a suppression with no
justification, and on a bare `nosemgrep` (which would blanket-suppress every rule on
the line and attribute the exception to nobody).

## Evidence queries

Across local checkouts of all active repos:

```bash
grep -rn "nosemgrep: soc2-logging" --include='*.py' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' .
```

Org-wide without checkouts:

```bash
gh search code --owner finelo-subpilot "nosemgrep: soc2-logging" --limit 100
gh search code --owner finelo-subpilot "nosemgrep" --limit 100   # unattributed suppressions
```

Every hit MUST show `soc2-logging.<lang>.<slug> — <justification>`. A hit without a
justification is a finding, not an exception.

## What auditors get

1. **The control**: `soc2-logging / soc2-logging` required status check on every active
   repo's default branch (`gh api repos/finelo-subpilot/<repo>/branches/<default>/protection`).
2. **The rules**: this repo, versioned by tag, every rule fixture-tested in CI, and the
   packaged wheel proven to ship them (`just check`, `just smoke`). The CI workflow pins
   the rules to its own commit (`github.job_workflow_sha`), so a consumer's ref and the
   rules it runs cannot diverge.
3. **The register**: output of the evidence queries above, enforced per PR by
   `check_suppressions.py`.

## Control integrity

The moving `v2` tag is what consumers' CI resolves, so whoever can move tags can change
the gate for every repo: keep tag protection enabled on this repo and restrict who may
push tags. Actions in the reusable workflow are SHA-pinned for the same reason.

**Owner**: platform team. **Cadence**: register reviewed at each SOC2 evidence
collection; exceptions older than two quarters get re-justified or fixed.
