"""Pre-commit entry point: run the bundled semgrep rules against staged files.

pre-commit installs this repo as a package and invokes the `soc2-logging`
console script with the staged filenames. The bundled `rules/` directory is
resolved from package data so the scan is fully pinned and offline.
"""

import os
import sys
from importlib.resources import files
from pathlib import Path

# semgrep applies these only when it walks a directory (`soc2-logging .` in CI);
# for explicitly passed filenames it scans whatever it is given, which is why the
# hook also filters filenames via `exclude:` in .pre-commit-hooks.yaml.
EXCLUDED = (
    'tests',
    'test',
    '__tests__',
    '__snapshots__',
    'migrations',
    'test_*.py',
    '*_test.py',
    'conftest.py',
    '*.test.ts',
    '*.test.tsx',
    '*.test.js',
    '*.test.jsx',
    '*.spec.ts',
    '*.spec.tsx',
    '*.spec.js',
    '*.spec.jsx',
    '*.stories.*',
)


def _semgrep() -> str:
    """Prefer the pinned semgrep installed beside this package over PATH."""
    bundled = Path(sys.executable).with_name('semgrep')
    return str(bundled) if bundled.exists() else 'semgrep'


def main() -> None:
    """Exec semgrep over the bundled rules and the filenames passed by pre-commit."""
    semgrep = _semgrep()

    argv = [
        semgrep,
        'scan',
        '--config',
        str(files('soc2_rules') / 'rules'),
        '--error',
        '--metrics=off',
        *(f'--exclude={pattern}' for pattern in EXCLUDED),
        *sys.argv[1:],
    ]

    os.execvp(semgrep, argv)
