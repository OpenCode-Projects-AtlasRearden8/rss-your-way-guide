#!/usr/bin/env python3
"""Build the static site from docs/*.md using only the Python standard library.

Usage:
    python3 build.py            # generate site/
    python3 build.py --clean    # remove generated site/ first, then build

Output is plain HTML with no JavaScript, no cookies, no analytics, and no
external requests of any kind. Everything stays in this folder.
"""

import argparse
import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
SITE_DIR = ROOT / "site"

CHUNK_ORDER = [
    "01-what-is-rss.md",
    "02-choosing-a-reader.md",
    "03-subscribing.md",
    "04-folders-and-filters.md",
    "05-the-triage-habit.md",
    "06-when-things-break.md",
]

BRAND = "Owning Your Reading Again"

TITLE_OF = {
    "README.md": "Owning Your Reading Again",
    "01-what-is-rss.md": "What RSS Actually Is",
    "02-choosing-a-reader.md": "Choosing a Free Reader",
    "03-subscribing.md": "Subscribing, Gently",
    "04-folders-and-filters.md": "Folders and Filters",
    "05-the-triage-habit.md": "The Triage Habit",
    "06-when-things-break.md": "When Things Break",
}

# ---------------------------------------------------------------- inline


def inline(text: str) -> str:
    """Convert inline markdown (code, bold, italic, links) to HTML."""
    out = html.escape(text, quote=False)

    # inline code first so other markers inside it are left alone
    code_spans: list[str] = []
    def stash_code(m):
        code_spans.append(m.group(1))
        return f"\x00CODE{len(code_spans) - 1}\x00"
    out = re.sub(r"`([^`]+)`", stash_code, out)

    # links [text](target)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    # render .md targets as .html (docs/ links become site/ links)
    out = re.sub(r"(<a href=\"[^\"]*)\.md(\")", r"\1.html\2", out)

    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", out)

    def unstash(m):
        return f"<code>{code_spans[int(m.group(1))]}</code>"
    out = re.sub(r"\x00CODE(\d+)\x00", unstash, out)
    return out


# ---------------------------------------------------------------- blocks

def split_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    """True for a markdown table delimiter row like | --- | :--- |."""
    stripped = line.strip()
    if "|" not in stripped:
        return False
    cells = split_table_row(stripped)
    return len(cells) >= 1 and re.fullmatch(r"\|?[-:|\s-]+\|?", stripped) and all(
        re.fullmatch(r":?-+:?", cell) for cell in cells
    )


def convert_blocks(md: str) -> str:
    lines = md.split("\n")
    blocks: list[str] = []
    para: list[str] = []

    def flush_para():
        if para:
            blocks.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    i = 0
    while i < len(lines):
        line = lines[i]

        # fenced code
        if line.startswith("```"):
            flush_para()
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append(
                "<pre><code>" + html.escape("\n".join(code)) + "</code></pre>"
            )
            i += 1  # skip closing fence
            continue

        # headings
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para()
            level = len(m.group(1)) + 1  # maps # -> <h2> inside the page body
            blocks.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}", line.strip()):
            flush_para()
            blocks.append("<hr>")
            i += 1
            continue

        # blockquote
        if line.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").rstrip())
                i += 1
            blocks.append(f"<blockquote>{inline(' '.join(quote))}</blockquote>")
            continue

        # table scan
        chunks = split_table_row(line)
        looks_like_table = (
            line.lstrip().startswith("|")
            and len(chunks) >= 1
            and i + 1 < len(lines)
            and is_table_separator(lines[i + 1])
        )
        if looks_like_table:
            flush_para()
            header = chunks
            i += 2  # skip header row and separator
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            thead = "".join(f"<th>{inline(c)}</th>" for c in header)
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>"
                for row in rows
            )
            blocks.append(
                "<table><thead><tr>" + thead + "</tr></thead><tbody>"
                + body + "</tbody></table>"
            )
            continue

        # lists (flat; nested items are indented and still match)
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            flush_para()
            ordered = bool(re.fullmatch(r"\d+\.", m.group(2)))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while True:
                if i < len(lines):
                    m2 = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                    if m2 and bool(re.fullmatch(r"\d+\.", m2.group(2))) == ordered:
                        text = m2.group(3).rstrip()
                        i += 1
                        # continuation lines (indented, not a new item)
                        while i < len(lines) and lines[i].startswith("  ") and not re.match(
                            r"^\s*([-*]|\d+\.)\s+", lines[i]
                        ):
                            text += " " + lines[i].strip()
                            i += 1
                        items.append(f"<li>{inline(text)}</li>")
                        continue
                break
            blocks.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue

        # blank line = paragraph break
        if not line.strip():
            flush_para()
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush_para()
    return "\n".join(blocks)


# ---------------------------------------------------------------- page shell

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="site-head">
<p class="brand"><a href="{prefix}index.html">{brand}</a></p>
<p class="tagline">A gentle guide to owning your reading again</p>
</header>
<div class="wrap">
<nav class="crumbs">
{nav}
</nav>
<main>
{body}
</main>
<nav class="page-nav">
{pager}
</nav>
</div>
<footer class="site-foot">
<p>Owning Your Reading Again \u2014 a beginner guide by Asdale Dynamics, LLC.
No tracking, no analytics, no cookies: this site is static HTML and makes no
requests beyond its own stylesheet.</p>
<p><a href="https://dylanasdale.github.io/">dylanasdale.github.io</a> \u2014
MIT licensed (see LICENSE in the repository).</p>
</footer>
</body>
</html>
"""


def build_nav(src_name: str) -> str:
    links = []
    for name in ["README.md"] + CHUNK_ORDER:
        cls = ' class="current"' if name == src_name else ""
        out = "index.html" if name == "README.md" else name.replace(".md", ".html")
        links.append(f'<a href="{out}"{cls}>{html.escape(TITLE_OF[name])}</a>')
    return " \u00b7 ".join(links)


def build_pager(src_name: str) -> str:
    order = ["README.md"] + CHUNK_ORDER
    idx = order.index(src_name)
    parts = []
    if idx > 0:
        prev = order[idx - 1]
        out = "index.html" if prev == "README.md" else prev.replace(".md", ".html")
        parts.append(f'<a class="prev" href="{out}">\u2190 {html.escape(TITLE_OF[prev])}</a>')
    if idx < len(order) - 1:
        nxt = order[idx + 1]
        out = nxt.replace(".md", ".html")
        parts.append(f'<a class="next" href="{out}">{html.escape(TITLE_OF[nxt])} \u2192</a>')
    return " ".join(parts)


def strip_h1(md: str) -> str:
    """Remove the first H1 line from the source (the page shell provides it)."""
    return re.sub(r"^#[^\n]*\n\n?", "", md.lstrip(), count=1)


DEFINITIONS = {
    "README.md": "front matter: how to use the guide and what it covers",
    "01-what-is-rss.md": "the idea in one page, and why feeds beat the algorithm",
    "02-choosing-a-reader.md": "honest comparison of free reader options",
    "03-subscribing.md": "finding feeds for blogs, podcasts, and library newsletters",
    "04-folders-and-filters.md": "organizing by reading mode, plus filters and OPML",
    "05-the-triage-habit.md": "a 5-minute daily ritual that replaces doomscrolling",
    "06-when-things-break.md": "troubleshooting and a gentle glossary",
}


def convert_page(md: str, src_name: str) -> str:
    """One chunk of markdown -> a whole standalone HTML page."""
    body = convert_blocks(strip_h1(md))
    title = TITLE_OF[src_name]
    page_title = title if title == BRAND else f"{title} \u2014 {BRAND}"
    return PAGE_TEMPLATE.format(
        title=page_title,
        description=DEFINITIONS[src_name],
        prefix="",
        brand=BRAND,
        nav=build_nav(src_name),
        body=body,
        pager=build_pager(src_name),
    )


def build(clean: bool = False) -> None:
    if clean and SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(exist_ok=True)
    (SITE_DIR / "assets").mkdir(exist_ok=True)

    css_src = ROOT / "site-src" / "style.css"
    shutil.copy(css_src, SITE_DIR / "assets" / "style.css")

    pages = {}
    for name in ["README.md"] + CHUNK_ORDER:
        md = (DOCS_DIR / name).read_text(encoding="utf-8")
        out_name = "index.html" if name == "README.md" else name.replace(".md", ".html")
        pages[out_name] = convert_page(md, name)

    for out_name, content in pages.items():
        (SITE_DIR / out_name).write_text(content, encoding="utf-8")

    print(f"Built {len(pages)} pages into {SITE_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the static site.")
    ap.add_argument("--clean", action="store_true", help="wipe site/ before building")
    args = ap.parse_args()
    build(clean=args.clean)
