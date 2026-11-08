# STATUS.md

Project: **Owning Your Reading Again — a gentle guide to RSS**
By Asdale Dynamics, LLC. Beginner manual + static HTML site, local-first, no tracking.
Last updated: 2026-11-08.

## What was built

- `docs/` — the guide as markdown (source of truth), seven files:
  - `README.md` — front matter: purpose, chapter map, how to use, no-tracking commitment
  - `01-what-is-rss.md` — what RSS is, feed vs. algorithmic feed, why feeds are finite
  - `02-choosing-a-reader.md` — free reader options (NetNewsWire, Feedbro, FreshRSS, Feeder), a 10-minute starter exercise
  - `03-subscribing.md` — finding and adding feeds: blogs, podcasts (podcast apps are feed readers), library/institution newsletters
  - `04-folders-and-filters.md` — folders organized by reading mode, email filters for newsletters, monthly OPML export, seasonal pruning
  - `05-the-triage-habit.md` — the five-minute three-pass triage (keep / skim / drop) replacing doomscrolling, with an explicit two-minute "bad week" fallback (ADHD-friendly)
  - `06-when-things-break.md` — troubleshooting, OPML/RSS/Atom glossary
- `build.py` — stdlib-only Python 3.10+ generator: `docs/*.md` → `site/*.html` (headings, tables, lists, blockquotes, fenced code, inline formatting, `.md`→`.html` link rewriting); `--clean` flag
- `site-src/style.css` — the site's single stylesheet source (copied to `site/assets/` at build; no web fonts, no external requests)
- `site/` — generated static site (7 pages): index + 6 chapter pages, prev/next pager, nav bar, responsive, **zero JavaScript, zero cookies, zero analytics, zero requests beyond its own stylesheet**
- `check.py` — 25 unittest checks: markdown renderer unit tests, docs integrity, built-site tests (all 7 pages present, all relative links resolve, correct titles, LLC credit, no tracking markers, no `<script>`/inline handlers, single local stylesheet)
- `README.md` — credits Asdale Dynamics, LLC, explains usage and the "not a digest tool / not a search guide" distinction
- `LICENSE` — MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`

## How to run it

```sh
python3 build.py              # (re)generate site/ from docs/
python3 -m unittest check     # run the 25 verification checks
python3 -m http.server 8080 --directory site   # optional local preview
# or simply open site/index.html in any browser (works offline)
```

Requirements: Python 3.10+ only. No packages, no network needed at build or run time.

## Verification results

- `python3 -m py_compile build.py check.py` — clean
- `python3 build.py --clean && python3 build.py` — builds all 7 pages
- `python3 -m unittest check` — **Ran 25 tests … OK** (all pass; two failures found and fixed during development: single-column table separator detection, nav-link check exception for the stylesheet)
- HTML structure: all 7 pages verified well-formed via stdlib `html.parser` (balanced tags, no mismatches)
- Live preview served: `python3 -m http.server` returned HTTP 200 for `index.html`, chapter page, and `assets/style.css`
- No secrets, API keys, or personal data in any file (email-pattern scan included in checks)

## Known gaps / intentionally out of scope

- **Renderer is a subset of Markdown**, by design: it covers what the guide uses (headings through ####, tables, flat lists with wrapped continuation lines, blockquotes, fenced code, hr, inline formatting). Nested/corner-case Markdown outside that set may render unexpectedly.
- **No images** ship with the guide; no RSS-icon image is included.
- No RSS/RSS-proxy feed-generation features, no OPML processing code, no feed validation tooling — this project is documentation + a static site, deliberately narrow (a digest/summarizer CLI and search-technique guide are separate projects).
- No deployment automation (per instructions: nothing pushed, nothing published).
- External links in prose (e.g., dylanasdale.github.io) are navigational links in the footer/body; the site itself never fetches anything external automatically.
- The `../LICENSE` link from the index page resolves inside the repository but would not resolve on a hosted copy of `site/` alone.
