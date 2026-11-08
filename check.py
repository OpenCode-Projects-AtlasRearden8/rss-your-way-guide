#!/usr/bin/env python3
"""Checks for the built site and the docs source. Run after build.py."""

import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

import build as sitebuild

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"

TRACKING_MARKERS = [
    "google-analytics", "googletagmanager", "gtag(", "fathom", "plausible.io",
    "matomo", "cloudflareinsights", "hotjar", "mixpanel", "segment.io",
    "facebook.com/plugins", "twitter.com/widgets", "<script", "document.cookie",
    "consent.js", "quantserve", "scorecardresearch", "onclick", "onload=",
]


class MarkdownToHtmlTests(unittest.TestCase):
    def convert(self, md):
        return sitebuild.convert_blocks(md)

    def test_headings_map_to_h2_plus(self):
        self.assertEqual(
            self.convert("# Big\n## Sub"),
            "<h2>Big</h2>\n<h3>Sub</h3>",
        )

    def test_paragraphs_and_inline_formatting(self):
        out = self.convert("Some **bold**, *soft*, and `code` text.")
        self.assertEqual(
            out,
            "<p>Some <strong>bold</strong>, <em>soft</em>, "
            "and <code>code</code> text.</p>",
        )

    def test_links_and_html_escaping(self):
        out = self.convert('Go to [the site](https://x.example) — "now" <now>')
        self.assertIn('<a href="https://x.example">the site</a>', out)
        self.assertIn("&lt;now&gt;", out)
        self.assertNotIn("<now>", out)

    def test_markdown_links_gain_html_extension(self):
        out = self.convert("See [chapter 1](01-what-is-rss.md).")
        self.assertIn('href="01-what-is-rss.html"', out)

    def test_unordered_and_ordered_lists(self):
        out = self.convert("- one\n- two\n")
        self.assertEqual(out, "<ul><li>one</li><li>two</li></ul>")
        out = self.convert("1. first\n2. second\n")
        self.assertEqual(out, "<ol><li>first</li><li>second</li></ol>")

    def test_list_continuation_lines(self):
        out = self.convert("- a point\n  that wraps onto two lines\n")
        self.assertEqual(out, "<ul><li>a point that wraps onto two lines</li></ul>")

    def test_mixed_list_kinds_do_not_merge(self):
        out = self.convert("- item\n\n1. item\n")
        self.assertEqual(out, "<ul><li>item</li></ul>\n<ol><li>item</li></ol>")

    def test_table_with_header_and_rows(self):
        md = "| a | b |\n| --- | --- |\n| 1 | 2 |\n"
        out = self.convert(md)
        self.assertIn("<thead><tr><th>a</th><th>b</th></tr></thead>", out)
        self.assertIn("<tbody><tr><td>1</td><td>2</td></tr></tbody>", out)

    def test_table_cell_content_is_inline_formatted(self):
        md = "| x |\n| --- |\n| **y** |\n"
        self.assertIn("<td><strong>y</strong></td>", self.convert(md))

    def test_fenced_code_block_escapes_html(self):
        out = self.convert("```\n<a href='x'>glyph & such</a>\n```\n")
        self.assertIn("<pre><code>", out)
        self.assertIn("&lt;a href=&#x27;x&#x27;&gt;", out)

    def test_blockquote(self):
        out = self.convert("> a quiet thought\n")
        self.assertEqual(out, "<blockquote>a quiet thought</blockquote>")

    def test_hr_and_blank_lines(self):
        out = self.convert("before\n\n---\n\nafter\n")
        self.assertIn("<hr>", out)
        self.assertTrue(out.startswith("<p>before</p>"))
        self.assertTrue(out.endswith("<p>after</p>"))

    def test_src_paths_are_never_leaked_body(self):
        out = self.convert("[link](../LICENSE)")
        self.assertIn('href="../LICENSE"', out)


class DocsSourceTests(unittest.TestCase):
    ALL = ["README.md"] + sitebuild.CHUNK_ORDER

    def test_all_source_files_exist(self):
        for name in self.ALL:
            self.assertTrue((ROOT / "docs" / name).exists(), name)

    def test_every_chunk_starts_with_chapter_one_h1(self):
        for name in self.ALL:
            first = (ROOT / "docs" / name).read_text(encoding="utf-8").splitlines()[0]
            self.assertTrue(first.startswith("# "), f"{name}: {first!r}")

    def test_no_personal_data_in_docs(self):
        pattern = re.compile(
            r"\b(?:[A-Za-z0-9._%+-]+)@(?:[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b"
        )
        for name in self.ALL:
            text = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIsNone(pattern.search(text), f"email-like text in {name}")

    def test_required_terms_present_guide_wide(self):
        combined = "\n".join(
            (ROOT / "docs" / n).read_text(encoding="utf-8") for n in self.ALL
        )
        for needle in [
            "RSS", "reader", "podcast", "library", "folder", "filter",
            "triage", "doomscrolling", "OPML", "Asdale Dynamics, LLC",
        ]:
            self.assertIn(needle, combined, needle)


class BuiltSiteTests(unittest.TestCase):
    def setUp(self):
        for required in ["index.html", "01-what-is-rss.html", "assets/style.css"]:
            self.assertTrue(
                (SITE / required).exists(),
                f"site not built? missing {required}: run python3 build.py",
            )
        self.pages = {
            p.name: p.read_text(encoding="utf-8")
            for p in SITE.glob("*.html")
        }

    def test_all_seven_pages_built(self):
        self.assertEqual(len(self.pages), 7, list(self.pages))

    def test_nav_links_resolve(self):
        names = set(self.pages)
        for html_text in self.pages.values():
            for target in re.findall(r'href="([^"]+)"', html_text):
                parts = urlsplit(target)
                if parts.scheme or parts.netloc:
                    continue
                path = parts.path.split("#")[0]
                if not path or path == "assets/style.css":
                    continue
                self.assertIn(path, names | {"../LICENSE"})

    def test_marker_terminology_in_page_titles(self):
        expected = {
            "index.html": "Owning Your Reading Again",
            "01-what-is-rss.html": "What RSS Actually Is",
            "02-choosing-a-reader.html": "Choosing a Free Reader",
            "03-subscribing.html": "Subscribing, Gently",
            "04-folders-and-filters.html": "Folders and Filters",
            "05-the-triage-habit.html": "The Triage Habit",
            "06-when-things-break.html": "When Things Break",
        }
        for name, needle in expected.items():
            self.assertIn(needle, self.pages[name])

    def test_no_tracking_markers_anywhere(self):
        for name, html_text in self.pages.items():
            low = html_text.lower()
            for marker in TRACKING_MARKERS:
                self.assertNotIn(marker, low, f"{name} contains {marker!r}")

    def test_no_javascript_tags(self):
        for name, html_text in self.pages.items():
            self.assertNotIn("<script", html_text.lower(), name)
            self.assertNotIn("onclick=", html_text.lower(), name)

    def test_footer_has_llc_credit_and_license_pointer(self):
        idx = self.pages["index.html"]
        self.assertIn("Asdale Dynamics, LLC", idx)
        self.assertIn("MIT", idx)

    def test_single_stylesheet_local_only(self):
        for name, html_text in self.pages.items():
            hrefs = re.findall(r'<link[^>]+href="([^"]+)"', html_text)
            self.assertEqual(
                hrefs, ["assets/style.css"],
                f"{name} must reference only the local stylesheet",
            )

    def test_every_page_has_prev_or_next_pager(self):
        for name, html_text in self.pages.items():
            self.assertRegex(
                html_text, r'(class="prev"|class="next")',
                f"{name}: expected a prev/next link",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
