# Stolos SEO Audit

A free SEO and AI-search audit for your website. It runs inside Claude Code on your own computer: you type one
command with your website address, and a team of AI agents checks your technical setup, content, structured data,
local SEO and how ready your site is for AI answers (Google AI Overviews, ChatGPT, Perplexity). You get a full report
and a prioritised action plan. Under the hood: 26 sub-skills and 19 sub-agents.

Made available free by [Stolos Digital](https://stolosdigital.com). Based on
[claude-seo](https://github.com/AgriciDaniel/claude-seo) by AgriciDaniel (MIT). See [NOTICE.md](NOTICE.md).

## What you need

- [Claude Code](https://claude.com/claude-code) (version 1.0.33 or newer) with a Claude account
- Python 3.10 or newer and Git (most Macs already have both)
- About 10 minutes for the first run

No API keys are required. Google Search Console, PageSpeed and GA4 connections are optional.

## Install (2 commands)

Open Claude Code and type:

```
/plugin marketplace add AgiannidisMD/stolos-seo-audit
/plugin install claude-seo@stolosdigital
```

Prefer a terminal installer? Run:

```bash
curl -fsSL https://raw.githubusercontent.com/AgiannidisMD/stolos-seo-audit/main/install.sh | bash
```

## Run your audit

In Claude Code, type:

```
/seo audit yourwebsite.com
```

The audit takes a few minutes and creates a folder `yourwebsite.com-audit/` with:

- `FULL-AUDIT-REPORT.md`: everything that was checked and what was found
- `ACTION-PLAN.md`: what to fix first, from critical to low
- an optional PDF report

Other useful commands: `/seo page <url>` for one page, `/seo local <url>` for local businesses, `/seo geo <url>` for
AI-search readiness. The full list is in [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md).

## Good to know

- Each audit uses your Claude plan's usage. A full audit runs many agents at once, so it uses more than a normal chat.
- The report ends with a short Stolos Digital footer. You can delete it; it is plain text in the report.
- Nothing is sent to Stolos Digital. The audit runs on your machine with your own Claude account.

## Want the fixes done for you?

The audit tells you what to fix. If you would rather have it built, Stolos Digital can do it:
[book a free 30-minute call](https://stolosdigital.com/contact?utm_source=github&utm_medium=readme&utm_campaign=seo-audit).

## Licence

MIT. Original work © 2026 AgriciDaniel and contributors; Stolos Digital edition © 2026 Stolos Digital.
