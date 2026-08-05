"""Pre-commit entry point: run the bundled semgrep rules against staged files.

pre-commit installs this repo as a package and invokes the `soc2-logging`
console script with the staged filenames. The bundled `rules/` directory is
resolved from package data so the scan is fully pinned and offline.
"""

import os
import sys
from importlib.resources import files


def main() -> None:
    """Exec semgrep over the bundled rules and the filenames passed by pre-commit."""
    rules_dir = str(files('soc2_rules') / 'rules')

    argv = [
        'semgrep',
        'scan',
        '--config',
        rules_dir,
        '--error',
        '--quiet',
        '--metrics=off',
        *sys.argv[1:],
    ]

    os.execvp('semgrep', argv)
