# Owning Your Reading Again — a gentle guide to RSS

A beginner-friendly manual for taking back your reading, listening, and attention from the infinite feed. Plain English, step by step, never condescending — explained like a friend would.

Written and maintained by **Asdale Dynamics, LLC** as part of Dylan Asdale's beginner guide series ([dylanasdale.github.io](https://dylanasdale.github.io/)).

## What's inside

Six short chapters plus front matter, in `docs/`:

1. **What RSS actually is** — the idea in one page, and why a feed that *ends* beats a feed that doesn't
2. **Choosing a free reader** — calm, honest comparison of free options, phone or desktop
3. **Subscribing, gently** — blogs, podcasts, and library/institution newsletters
4. **Folders and filters** — organizing by reading mode, email filters, OPML backup
5. **The triage habit** — a five-minute daily ritual that replaces doomscrolling (ADHD-friendly, low-pressure, with a "bad week" fallback)
6. **When things break** — troubleshooting and a friendly glossary

Reading time for the whole thing: about half an hour, in any order.

## Build the static site

Requirements: Python 3.10+ only — no packages, no installs, no network at build time.

```sh
python3 build.py          # generates site/ from docs/ (site/index.html + chapters)
python3 -m unittest check # runs 26 checks: renderer, docs, generated pages
```

The generated site is plain static HTML with one local stylesheet:

- **No JavaScript, no cookies, no analytics, no external requests** — nothing phones home
- Works offline with any browser: `python3 -m http.server 8080 --directory site` or just open `site/index.html`
- Fully regenerable from `docs/`; the markdown remains the source of truth

## Design notes

- **Local-first and private.** No accounts, no telemetry, no tracking of any kind; the site makes zero requests beyond its own stylesheet.
- **Deliberately not a summarizer.** This guide is about reading your chosen sources directly and calmly. It is different from an automated RSS-digest tool (which summarizes feeds) and different from search technique guides (which help you *find*); both are complementary skills, not this project's topic.
- **Low-pressure by design.** The habits here assume tired evenings and bad weeks, and are built to shrink rather than collapse.

## Repository layout

```
docs/       the guide (markdown, source of truth)
site/       generated static site (build output, safe to delete and rebuild)
site-src/   source stylesheet, copied to site/assets/ at build time
build.py    builds docs/*.md into site/ (stdlib only)
check.py    renderer unit tests plus site and docs verification
```

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
