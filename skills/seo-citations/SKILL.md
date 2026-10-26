---
name: seo-citations
description: >
  Build the citation and directory plan from The Local SEO Playbook (Stage 6):
  the core listings (Bing Places, Apple Business Connect, Foursquare, Yelp, Data
  Axle in the US), the top directories that rank for the keyword, a competitor
  source gap list and local link ideas, each with how to get listed. Use when the
  user says citations, directories, listings, NAP consistency, local links,
  link prospecting, or "where should my business be listed".
user-invocable: true
argument-hint: "<url> \"<keyword>\" \"<city>\" [competitor domains...]"
license: MIT
metadata:
  author: Stolos Digital
  version: "2.4.4"
  category: seo
---

# Citations and local link prospects

Blueprint: The Local SEO Playbook, Stage 6 (Weeks 9-10). Citations = listings of the
business's name, address and phone (NAP) on other sites. They help Google trust the
details; they only help when every one matches the profile exactly.

## Steps (playbook order)

1. **6.1 Core listings (Basic run).** Bing Places, Apple Business Connect,
   Foursquare, Yelp, Data Axle (US only). For each: does a listing exist (search
   `"<business name>" <city> site:<domain>`), and does its NAP match the website's
   (read the site NAP with `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run playbook_check.py <url> --keyword "<keyword>" --city "<city>" --json`). Status: `listed / missing / mismatch / unknown`.
2. **6.2 Directories that rank (Basic run).** Search the main keyword and 2-3
   variations; list the directories on page 1-2 (not competitors' own sites). These
   are the directories Google already trusts for this search. Target: top 20.
3. **6.3 Competitor gap (Advanced).** For 3-5 competitors from the playbook's
   competitor scan (3.2): where are they listed that this business is not?
   - With the DataForSEO extension: backlinks of each competitor, filtered to
     directory and local domains (ask before paid calls, show the estimate).
   - With Moz or Bing Webmaster (free tiers, see `/seo backlinks`): linking domains.
   - Without data: search `"<competitor name>" "<city>"` and record the sites found.
4. **6.4 Ideas from AI, checked.** Run the playbook's 6.4 prompt
   (`../seo-playbook/references/playbook-prompts.md`), then open every suggestion
   and keep only sites that exist and take listings in this country.
5. **Local link prospects.** Associations, suppliers, sponsors, local news and
   community sites, chambers, schools and clubs. For each: why it fits, how to get
   the link (membership, sponsorship, story, supplier page), effort low/med/high.
6. **6.5 / 6.6 (Advanced).** Point to the wider source list in the playbook (maps,
   voice, social, directories, in-car). Listing services are optional and paid;
   state that, never push one.

## Output `CITATIONS.md`

| # | Source | Type | Status | NAP match | How to get listed | Step |
|---|---|---|---|---|---|---|

Sort: 6.1 first, then 6.2 by position, then gap list, then link prospects. End with
the 3 to do this week and the note: copy NAP, hours, categories, description and
photos from the profile so everything matches; keep the phone at hand for
verification codes (Week 9).

## Rules

- Never create listings or accounts for the user. Give the steps.
- No paid link schemes, private networks or bought reviews (Stage 8: white hat).
- One business, one NAP. Flag every mismatch, even a suite number or phone format.
- Directories change or close. Mark anything you could not open as `unverified`.
