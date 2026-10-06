from __future__ import annotations

import re
from functools import partial
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from markdown import Markdown  # pyrefly: ignore [untyped-import]
from properdocs.structure.toc import get_toc

if TYPE_CHECKING:
    from collections.abc import Iterable

    from properdocs.config.defaults import ProperDocsConfig
    from properdocs.structure.files import Files
    from properdocs.structure.pages import Page
    from properdocs.structure.toc import AnchorLink

TOC_RE = re.compile(r"\[\s*toctree(\s[^]]+)?\]")


def _sub_toctree(page: Page, files: Files, m: re.Match) -> str:
    args: list[str] = m[1].strip().split()
    if not args:
        msg = "toctree directive missing required <page> argument"
        raise RuntimeError(msg)
    relpath = args.pop(0)
    kwargs = {}
    for arg in args:
        k, _, v = arg.partition("=")
        if not v:
            msg = f"Expected key=value argument pairs, got '{arg}'"
            raise RuntimeError(msg)

        kwargs[k] = v

    depth: int | None = None

    if "depth" in kwargs:
        depth = int(kwargs["depth"])

    root = PurePosixPath(page.file.src_uri).parent
    path = str(root / relpath)

    if (file := files.get_file_from_path(path)) is None:
        msg = f"File {path} not found"
        raise RuntimeError(msg)

    # Have to parse the file this way instead of using `page.render()`
    # Using the default list of markdown extensions creates duplicate header permalinks
    md = Markdown(extensions=["toc", "fenced_code", "attr_list"])
    _ = md.convert(file.content_string)
    toc = get_toc(getattr(md, "toc_tokens", []))

    def render_links(links: Iterable[AnchorLink], depth: int | None):
        if depth is not None:
            if depth <= 0:
                return

            depth -= 1

        for link in links:
            indent = "    " * (link.level - 1)
            bullet = f"- [{link.title}]({relpath}{link.url})\n"
            yield indent + bullet
            yield from render_links(link.children, depth)

    return "".join(render_links(toc, depth))


def on_page_markdown(markdown: str, page: Page, config: ProperDocsConfig, files: Files) -> str:
    return TOC_RE.sub(partial(_sub_toctree, page, files), markdown)
