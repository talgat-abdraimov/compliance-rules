"""Fail if the python and typescript PII denylists drift apart.

Each pack defines its denylist exactly once (a YAML anchor aliased by every
pattern branch) and documents it in a `# PII_DENYLIST:` header. This asserts the
headers agree and that every documented term is actually enforced by the regex —
a term present in the header but missing from the pattern is coverage the gate
claims and does not have.
"""

import re
import sys
from pathlib import Path

PACKS = {
    'python': Path('src/soc2_rules/rules/python/pii_fields.yml'),
    'typescript': Path('src/soc2_rules/rules/typescript/pii_fields.yml'),
}


def normalize(pattern: str) -> str:
    """Reduce case-class and optional-separator spellings to plain snake_case."""
    return re.sub(r'\[(\w)\w\]', r'\1', pattern).replace('_?', '_').lower()


def main() -> int:
    errors: list[str] = []
    headers: dict[str, str] = {}

    for lang, path in PACKS.items():
        body = path.read_text()

        header = re.search(r'# PII_DENYLIST: (.+)', body)
        if not header:
            errors.append(f'{path}: missing the "# PII_DENYLIST:" header')
            continue
        headers[lang] = header.group(1).strip()

        # Only the patterns count as enforcement — a term named in the rule
        # message but absent from the regex is documentation, not a control.
        enforced = normalize(
            ' '.join(line for line in body.splitlines() if line.strip().startswith('regex:'))
        )

        copies = enforced.count('snippet')
        if copies != 1:
            errors.append(
                f'{path}: denylist is written {copies} times, expected once — '
                'divergent copies are how phone_number slipped past the f-string branch'
            )

        unenforced = [term for term in headers[lang].split('|') if term not in enforced]
        if unenforced:
            errors.append(f'{path}: documented but not enforced: {", ".join(unenforced)}')

    if len(set(headers.values())) > 1:
        errors.append('PII_DENYLIST headers differ between the python and typescript packs')

    for error in errors:
        print(f'denylist: {error}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
