---
name: seo-keywords
description: >
  Pick and size keywords for a local business the way The Local SEO Playbook does
  (step 3.1): one main "category + city" keyword first, then variations for
  services, areas and FAQs, grouped into pages. Optional search volumes through
  the DataForSEO extension or Google Keyword Planner; never invented. Use when the
  user says keyword research, main keyword, what should I rank for, search terms,
  "near me" terms, or keywords for a page plan.
user-invocable: true
argument-hint: "<business type> \"<city>\" [services...]"
license: MIT
metadata:
  author: Stolos Digital
  version: "2.4.4"
  category: seo
---

# Keyword research, local first

Blueprint: The Local SEO Playbook, step 3.1 ("Pick the main keyword") and the page
plan in 5.2. One main keyword comes first because categories, the title tag, the H1
and the pages all line up behind it.

## Steps

1. **Collect:** type of business, city, main services, areas served, website (optional).
2. **Candidates:** write the 5 terms a local customer is most likely to type, in the
   form "[category] [city]", ranked from most to least likely with one line why
   (the playbook's 3.1 prompt in `../seo-playbook/references/playbook-prompts.md`).
   If the site exists, read its title, H1 and services first so candidates match
   what the business really does.
3. **Size them (optional, needs data):** in order of preference:
   - DataForSEO extension: `dataforseo_labs_google_keyword_overview` or Keyword
     Planner volumes for the location (`/seo dataforseo`). Ask before paid calls and
     show the cost estimate from `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run dataforseo_costs.py`.
   - Google Ads Keyword Planner via `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run keyword_planner.py` (needs the user's
     Google Ads credentials).
   - No data source: mark volume `unknown` and rank by intent only. Never guess a number.
4. **Pick one main keyword.** Prefer the term with the clearest buying intent that
   matches the primary profile category. Ask the user to confirm it.
5. **Expand** around the main keyword, only for things the business really offers:
   - services: "[service] [city]" (one per core service, feeds 5.3)
   - areas: "[category] [area]" for about 5 real areas (feeds 5.4)
   - modifiers: "best", "near me", "emergency", "24/7", "open now" only if true
   - questions: real pre-call questions (feeds the 3.8 FAQ and page FAQs)
6. **Group into pages** (feeds 5.2). One page per intent; never two pages for the
   same intent. For a larger list, hand off to `/seo cluster` (SERP-overlap grouping).

## Output `KEYWORDS.md`

| Column | Meaning |
|---|---|
| keyword | the term |
| type | main / service / area / modifier / question |
| volume | monthly searches for the location, or `unknown` |
| source | DataForSEO / Keyword Planner / intent only |
| page | which page targets it (home, service hub, service page, area page, FAQ) |
| playbook step | 3.1, 3.8, 4.1, 5.3 or 5.4 |

Then 3 lines: the chosen main keyword, the title tag it implies (formula in
`../seo-playbook/references/playbook-steps.md`, 4.1) and the H1 (`<Category> in <City>`).

## Rules

- Local first. Wide national keywords only if the business serves the whole country.
- No keyword-stuffing advice for the profile name (playbook 3.3).
- No area keyword unless the business really serves that area; never a fake address.
- Volumes are estimates from the named source; say which source and month.
