# Stolos SEO Audit

A free SEO and AI-search audit for your website. It runs inside Claude Code on your own computer: you type one
command with your website address, and a team of AI agents checks your technical setup, content, structured data,
local SEO and how ready your site is for AI answers (Google AI Overviews, ChatGPT, Perplexity). You get a full report
and a prioritised action plan. Under the hood: 29 sub-skills and 19 sub-agents.

Made available free by [Stolos Digital](https://stolosdigital.com). Based on
[claude-seo](https://github.com/AgriciDaniel/claude-seo) by AgriciDaniel (MIT). See [NOTICE.md](NOTICE.md).

## Quick start

In Claude Code, type these three lines (use your own website, service and city):

```
/plugin marketplace add AgiannidisMD/stolos-seo-audit
/plugin install claude-seo@stolosdigital
/seo playbook run yourwebsite.com "plumber" "Your City"
```

The last line runs the free Local SEO Playbook on your site. For a full audit instead, type `/seo audit yourwebsite.com`.

## What you need

- [Claude Code](https://claude.com/claude-code) (version 1.0.33 or newer) with a Claude account
- Python 3.10 or newer and Git (most Macs already have both). Python 3.11+ is recommended for the latest security fixes
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

Other useful commands: `/seo page <url>` for one page, `/seo local <url>` for a local SEO score, `/seo geo <url>` for
AI-search readiness. The full list is in [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md).

## Local business? Run the playbook

The audit tells you what is wrong. **The Local SEO Playbook** (our free 9-stage guide, the PDF you can get at
[stolosdigital.com](https://stolosdigital.com)) tells you what to do, week by week. This plugin runs it for you:

```
/seo playbook run yourwebsite.com "plumber" "Your City"
```

You get a folder `yourwebsite.com-playbook/` with the playbook checklist ticked from real checks of your site (title,
H1, NAP in the footer, map embed, LocalBusiness schema, page count, areas page), your top-10 benchmark, a dated
12-week plan, the monthly self-check table and the playbook prompts filled in with your details. Every line carries
the playbook's step number, so you can open the PDF at that page.

Then, each week:

```
/seo playbook next
```

tells you which week you are in and the next three steps. Two helpers follow the same playbook stages:
`/seo keywords` (pick your main keyword, step 3.1) and `/seo citations` (where to get listed, Stage 6).

The playbook is a method, not a promise: nobody can guarantee rankings.

## Good to know

- Each audit uses your Claude plan's usage. A full audit runs many agents at once, so it uses more than a normal chat.
- The report ends with a short Stolos Digital footer. You can delete it; it is plain text in the report.
- Nothing is sent to Stolos Digital. The audit runs on your machine with your own Claude account.

## Want the fixes done for you?

The audit tells you what to fix. If you would rather have it built, Stolos Digital can do it:
[book a free 30-minute call](https://stolosdigital.com/contact?utm_source=github&utm_medium=readme&utm_campaign=seo-audit).

## Licence

MIT. Original work © 2026 AgriciDaniel and contributors; Stolos Digital edition © 2026 Stolos Digital.
