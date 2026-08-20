rules := "src/soc2_rules/rules"

sync:
    uv sync

# No --quiet here: it suppresses the rule-parse errors this recipe exists to surface.
validate:
    uv run semgrep scan --validate --config {{rules}} --metrics=off

test:
    #!/usr/bin/env bash
    set -euo pipefail
    ls {{rules}}/python/*.yml {{rules}}/typescript/*.yml > /dev/null
    # semgrep --test silently skips a rule file with no same-basename fixture,
    # which would let an untested rule ship.
    for lang in python:py typescript:ts; do
      for rule in {{rules}}/${lang%:*}/*.yml; do
        fixture="tests/${lang%:*}/$(basename "$rule" .yml).${lang#*:}"
        [ -f "$fixture" ] || { echo "no fixture for $rule (expected $fixture)"; exit 1; }
      done
    done
    uv run semgrep scan --test --config {{rules}}/python tests/python --metrics=off
    uv run semgrep scan --test --config {{rules}}/typescript tests/typescript --metrics=off

denylist:
    uv run python scripts/check_denylist.py

suppressions:
    uv run python scripts/check_suppressions.py . --self-test

# The wheel is what consumers actually install — a rule file missing from it is
# a silently disabled gate, so assert every rule ships.
package:
    #!/usr/bin/env bash
    set -euo pipefail
    rm -rf dist
    uv build --quiet
    want=$(ls {{rules}}/python/*.yml {{rules}}/typescript/*.yml | wc -l | tr -d ' ')
    got=$(unzip -l dist/*.whl | grep -c '\.yml$' || true)
    [ "$got" = "$want" ] || { echo "wheel ships $got rule files, expected $want"; exit 1; }
    echo "package: wheel ships all $want rule files"

# The consumer path end to end: install the wheel on the lowest supported
# python and check the hook entry point actually blocks a violation.
smoke:
    #!/usr/bin/env bash
    set -euo pipefail
    just package
    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"' EXIT
    uv venv --python 3.10 "$tmp/venv" --quiet
    uv pip install --python "$tmp/venv/bin/python" dist/*.whl --quiet
    printf 'from loguru import logger\n\n\ndef f(email):\n    logger.info("hi", email=email)\n' > "$tmp/leak.py"
    # --json because semgrep line-wraps rule ids in console output at terminal
    # width, which makes grepping for one depend on the length of $tmp.
    code=0
    "$tmp/venv/bin/soc2-logging" --json "$tmp/leak.py" > "$tmp/out" 2>&1 || code=$?
    grep -q 'no-pii-fields-in-logs' "$tmp/out" || { echo "hook did not flag the leak:"; cat "$tmp/out"; exit 1; }
    [ "$code" -ne 0 ] || { echo "hook exited 0 on a violation"; exit 1; }
    echo "smoke: hook installs on python 3.10 and blocks (exit $code)"

check: validate test denylist suppressions package

scan path:
    uv run semgrep scan --config {{rules}} --error --metrics=off {{path}}
