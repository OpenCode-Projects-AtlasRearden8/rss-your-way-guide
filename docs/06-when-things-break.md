# Chapter 6: When Things Break

Real feeds, real quirks. This chapter is for the two or three moments per year when something doesn't work, plus a small glossary so nothing here is a mystery word.

## Common problems, quick fixes

**The feed won't add.** The reader says "no feed found" or the URL errors out.
- Check the URL opens as XML in your browser (lots of `<item>` or `<entry>` tags, definitely not a web page). If it's a web page, you copied the site, not the feed.
- Try the guess-the-URL patterns from chapter 3 (`/feed/`, `/rss`, `/atom.xml`) before giving up.

**The feed adds but shows nothing.**
- Some feeds only include the last 10 items; if the blog is new or infrequent, that's just all it has.
- WordPress + certain plugins hide feeds; look for a "Feed" link in the footer again and try that exact URL.

**The feed is "behind" — a post I can see on the site isn't in the reader.**
- Readers check on a schedule (as often as hourly, sometimes less). Wait a bit before concluding anything's wrong. Very quiet blogs can lag in some readers' politeness policies — that's normal.

**Everything disappeared.**
- Before panic: most readers have an "unread" toggle you're not aware you pressed. Check the sidebar for "Unread only."
- Then: your OPML. If you exported last month (chapter 4 said monthly; please do, sincerely), import elsewhere and you're back in five minutes.

**I accidentally unsubscribed / removed a folder.**
- Re-add them. If you have an old OPML export, import it; folders usually survive as category structure in the file. Loss of one week's items is the worst case, and it's rare.

## The web of it: OPML, RSS vs. Atom, and other words

| Word | What it is | What you need to know |
| --- | --- | --- |
| **RSS** | The classic feed format (XML) | You'll never edit it. Readers read it for you. |
| **Atom** | A second feed format, doing the same job | Copy-paste either into a reader; it handles both. |
| **OPML** | An export file listing your feeds | The escape hatch. Export monthly, per chapter 4. |
| **Full text vs. summary feed** | Whether the feed has whole posts or just a preview | Some feeds make you click through to the site to read. That's the publisher's choice, not the reader's fault. |
| **Self-hosted** | A reader you run on your own server (like FreshRSS) | Skip until you want it; chapters 2–5 work anywhere. |
| **Sync** | Whether feeds read on your phone show as read on your laptop | Nice to have; don't block your start on it. |

## A word on scope

This guide deliberately stays *reading-first* and tool-agnostic: pick any reader, keep any podcast app, filter any email. That's the part that survives everything. Specific app instructions age; the triage habit and the folder logic here don't.

If you want to go further someday, there are two adjacent but *different* directions people take:

- **Automated digests:** separate tools that pull your feeds together and have an AI summarize them into one daily email. That's a different workflow with a different tradeoff; this guide keeps the relationship direct and unhurried, but the technologies can coexist.
- **Better searching:** feeds are for *staying* current; *finding* is a related skill with its own techniques, well covered in search-focused beginner guides.

Both are fine extensions. Neither is required to own your reading. Start with one folder and one feed, and let it grow into whatever it becomes.

## Glossary in friendly words

- **Feed** — a blog's automatic "what's new" list.
- **Feed reader** — the app that collects your feeds and shows you what's new, in one place.
- **Subscribe** — pick a feed to appear in your reader.
- **Unread** — an item you haven't triaged yet.
- **OPML** — the file that backs up your subscriptions.
- **Folder / category** — the reading-mode groups from chapter 4.
- **Filter** — an inbox rule that routes email newsletters into your reading area.
- **Triage** — the three-pass habit from chapter 5: keep, skim, or drop.

That's everything. Take your time, keep the pile small on purpose, and don't subscribe to anything you wouldn't be pleased to see arrive. Happy reading.
