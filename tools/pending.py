"""Script that parses comments in Python source code to find pending actions for a given release.

Recursively searches the given root directory and parses comments with the format:
    `# when [version_spec]: message`

Prints each message whose version spec is matched by the passed version.
Returns non-zero when matches are found so that it can be used in CI or as a pre-commit hook.

Usage:
    $ python tools/pending.py <root directory> <version>

"""

from __future__ import annotations

import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING

from semantic_version import SimpleSpec, Version

if TYPE_CHECKING:
    from collections.abc import Iterator

TAG = re.compile(r"\#[ \t]*when[ \t]*\[([^\]\n\r]+?)\][ \t]*:([^\n\r]+)")


def search_file(file: Path) -> Iterator[tuple[SimpleSpec, str, int]]:
    for num, line in enumerate(file.read_text().splitlines(), 1):
        if (mch := TAG.search(line)) is not None:
            spec, msg = mch.groups()

            yield SimpleSpec.parse(spec), msg.strip(), num


def search(root: Path, version: Version) -> Iterator[tuple[Path, SimpleSpec, str, int]]:
    for file in root.rglob("**/*.py"):
        for spec, msg, line in search_file(file):
            if spec.match(version):
                yield file, spec, msg, line


def main():
    parser = ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("version")

    args = parser.parse_args()
    version = Version.coerce(args.version)

    clean = True

    for file, _spec, msg, line in search(args.root, version):
        clean = False
        print(f"{file}:{line}: {msg}")

    sys.exit(0 if clean else 1)


if __name__ == "__main__":
    main()
