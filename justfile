sync:
    uv sync

validate:
    uv run semgrep scan --validate --config rules/ --quiet --metrics=off

test:
    #!/usr/bin/env bash
    set -euo pipefail
    ls rules/python/*.yml rules/typescript/*.yml > /dev/null
    uv run semgrep scan --test --config rules/python tests/python --metrics=off
    uv run semgrep scan --test --config rules/typescript tests/typescript --metrics=off

denylist-diff:
    #!/usr/bin/env bash
    set -euo pipefail
    py=$(grep -o 'PII_DENYLIST:.*' rules/python/pii_fields.yml | head -1)
    ts=$(grep -o 'PII_DENYLIST:.*' rules/typescript/pii_fields.yml | head -1)
    [ "$py" = "$ts" ] || { echo "PII denylist copies differ between packs"; exit 1; }

check: validate test denylist-diff

scan path:
    uv run semgrep scan --config rules/ --error --metrics=off {{path}}
