from __future__ import annotations

import logging
import re
import shutil
import subprocess

log = logging.getLogger("properdocs.plugins.towncrier")

_NO_CHANGE_RE = re.compile(r"^No significant changes.\s+\Z", flags=re.MULTILINE)


def macro() -> str:
    """Macro that generates pending changelog updates using towncrier."""
    if (cmd := shutil.which("towncrier")) is None:
        log.warning("'towncrier' command not found, skipping changelog update")
        return ""

    res = subprocess.run([cmd, "build", "--draft"], check=True, capture_output=True, text=True)  # noqa: S603
    out = res.stdout

    if _NO_CHANGE_RE.search(out):
        log.info("Changelog already up to date")
        return ""

    log.info("Changelog updated")
    return out
