# SOC2 exceptions register — audit evidence

The gate's documented-exceptions register is the org-wide set of inline
`nosemgrep` suppressions, each carrying the rule id and a mandatory justification.

## Evidence queries

Across local checkouts of all active repos:

```bash
grep -rn "nosemgrep: soc2-logging" --include='*.py' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' .
```

Org-wide without checkouts:

```bash
gh search code --owner finelo-subpilot "nosemgrep: soc2-logging" --limit 100
```

Every hit MUST show `soc2-logging.<lang>.<slug> — <justification>`. A hit without a
justification is a finding, not an exception.

## What auditors get

1. **The control**: `soc2-logging` required status check on every active repo's
   default branch (`gh api repos/finelo-subpilot/<repo>/branches/<default>/protection`).
2. **The rules**: this repo, versioned by tag, every rule fixture-tested in CI.
3. **The register**: output of the evidence query above.

**Owner**: platform team. **Cadence**: register reviewed at each SOC2 evidence
collection; exceptions older than two quarters get re-justified or fixed.
