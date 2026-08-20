"""Fail on nosemgrep suppressions that are not usable register entries.

The SOC2 exceptions register IS the set of inline suppressions (see
docs/exceptions-register.md), so each one must name the rule id and carry a
justification. A bare `nosemgrep` is rejected outright: it blanket-suppresses
every rule on the line and attributes the exception to nobody.
"""

import re
import sys
import tempfile
from pathlib import Path

CODE_SUFFIXES = {'.py', '.ts', '.tsx', '.js', '.jsx'}
SKIP_DIRS = {
    '.compliance-rules',
    '.git',
    '.mypy_cache',
    '.next',
    '.ruff_cache',
    '.venv',
    '__pycache__',
    'build',
    'dist',
    'node_modules',
    'vendor',
    'venv',
}
SUPPRESSION = re.compile(r'(?:#|//)\s*nosemgrep(?::\s*(?P<rest>.*))?$')
JUSTIFIED = re.compile(r'^(?P<ids>[\w.\-]+(?:\s*,\s*[\w.\-]+)*)\s*(?:—|--)\s*(?P<why>.+)$')
MIN_JUSTIFICATION = 10


def findings_for(path: Path, text: str) -> list[str]:
    findings = []

    for number, line in enumerate(text.splitlines(), start=1):
        match = SUPPRESSION.search(line.rstrip())
        if not match:
            continue

        where = f'{path}:{number}'
        rest = match.group('rest')

        if rest is None:
            findings.append(f'{where}: bare `nosemgrep` — name the rule id and justify it')
            continue

        justified = JUSTIFIED.match(rest.strip())
        if justified and len(justified.group('why').strip()) >= MIN_JUSTIFICATION:
            continue
        if 'soc2-logging' in rest:
            findings.append(
                f'{where}: `nosemgrep: {rest.strip()}` has no justification — '
                'append " — <why>, <ticket>"'
            )

    return findings


def scan(root: Path) -> list[str]:
    findings = []

    for path in sorted(root.rglob('*')):
        if path.suffix not in CODE_SUFFIXES or not path.is_file():
            continue
        if SKIP_DIRS & set(path.parts):
            continue
        findings.extend(findings_for(path, path.read_text(errors='replace')))

    return findings


def self_test() -> None:
    # Assembled at runtime: a literal suppression comment in this file would be
    # a finding against the file itself.
    marker = 'nosemgr' + 'ep'
    rule = 'soc2-logging.python.no-pii-fields-in-logs'

    with tempfile.TemporaryDirectory() as directory:
        good = Path(directory) / 'good.py'
        good.write_text(
            f"logger.info('a', email=e)  # {marker}: {rule} — scrubbed by sanitize(), TICKET-1\n"
        )
        assert scan(Path(directory)) == [], 'a justified suppression must pass'

        for bad, label in (
            (f'x = 1  # {marker}\n', 'bare'),
            (f'x = 1  # {marker}: {rule}\n', 'unjustified'),
            (f'x = 1  # {marker}: {rule} — wip\n', 'too short'),
        ):
            good.write_text(bad)
            assert scan(Path(directory)), f'{label} suppression must fail'

    print('check_suppressions: self-test ok')


def main(argv: list[str]) -> int:
    if '--self-test' in argv:
        self_test()
        argv = [argument for argument in argv if argument != '--self-test']

    findings = scan(Path(argv[0] if argv else '.'))
    for finding in findings:
        print(f'suppression: {finding}')

    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
