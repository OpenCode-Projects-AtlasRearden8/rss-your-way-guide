# Chapter 1: What RSS Actually Is

RSS stands for *Really Simple Syndication*, which is almost funny, because the underlying idea is simpler than the name.

## The one-paragraph version

Every blog, podcast, and many newsletters publish a **feed**: a plain, boring, machine-readable list of everything they've posted. A **feed reader** is an app that checks those lists for you, all at once, and shows you what's new. That's it. You're reading a table of contents for the whole internet you actually care about — one place, in order, no algorithm deciding anything.

## Why that's a big deal

You may be used to social media feeds that feel like this:

> Someone else's algorithm picks what you see, ranks it, mixes in ads, and — this is the important part — **never ends.**

An RSS feed is the opposite animal:

| | Social feeds | RSS feeds |
| --- | --- | --- |
| What you see | Whatever ranks highest | Only the sources *you chose* |
| Order | Algorithmic | Chronological |
| Ads | Mixed in | Never (from the feed itself) |
| The end | There is no end | **There is an end.** You finish. |

That last row is the whole point. A feed reader has a bottom. When you've seen everything new, you're done. Done is a real state. Doomscrolling is, by construction, endless — RSS gives you back the sensation of finishing.

## A tiny bit of history (to demystify)

Feed files have been around since roughly 1999. They look like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Ada's Writing Desk</title>
    <item>
      <title>What I learned rewriting chapter four</title>
      <link>https://example.com/chapter-four</link>
      <pubDate>Fri, 06 Nov 2026 08:00:00 -0500</pubDate>
    </item>
  </channel>
</rss>
```

Every item is just: **title, link, date, maybe a few lines of text.** No engagement graph, no "you might also like." Almost every serious blog, newspaper section, podcast, and journal publishes one of these — it has quietly outlived every platform that tried to replace it.

## What you can subscribe to (a preview)

- **Blogs** — personal sites, authors, engineers, scientists
- **Podcasts** — most podcast apps *are* feed readers under the hood
- **News sites, journals, and news sections** — even a single author's column
- **Library and museum newsletters** — when they offer feeds or email digests you can route into folders
- **YouTube channels and Reddit searches** — both still emit feed files. More on that in chapter 4.

## What RSS is *not*

- **Not a social network.** You don't friend anyone. You subscribe or you don't.
- **Not dead.** It looks unglamorous, which is exactly why it never gets canceled. Large tech companies have left it alone since the 2010s, and it's been quietly excellent ever since.
- **Not a time sink.** The reader doesn't want your attention more than it already has. There are no notifications unless you ask for them.
- **Not a summarizer.** This guide is about *reading your sources directly, calmly, your way.* It is deliberately different from an automated "RSS digest" tool, which compresses your feeds with AI. Both approaches are fine; this one is about the plain, unhurried relationship between you and the writers you chose.

That's the concept. Next: pick a reader. It takes ten minutes and it's free.
