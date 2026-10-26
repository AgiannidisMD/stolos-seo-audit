#!/usr/bin/env python3
"""Website checks from The Local SEO Playbook (Stolos Digital), Stages 2, 4 and 5.

Runs the steps of the free playbook that can be read from the website itself and
reports each one with the playbook's step number, a status and the evidence:

    2.2 / 4.3  NAP visible on the page and in the footer
    2.3 / 4.1  Title tag: main keyword, city, length (playbook aims for ~200 max),
               repeated words (stuffing)
    2.3 / 4.2  One H1 with category + city; H2s present
    2.4        Indexed pages proxy: URL count in the XML sitemap (the playbook's
               own check is a ``site:`` search, which stays a manual step)
    2.5 / 5.1  LocalBusiness (or a subtype) JSON-LD, with a phone that matches
    2.6 / 4.3  Google map embed
    5.4        "Areas we serve" link in the navigation

Statuses: ``pass``, ``fail``, ``manual`` (needs a person or a logged-in tool).
Nothing here guarantees rankings; it reports what the page shows.

Usage:
    playbook_check.py URL --keyword "plumber" --city "Springfield" [--json]
    playbook_check.py --html page.html --url URL --keyword K --city C [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

TITLE_MAX = 200  # playbook 4.1: "aim for about 200 characters at most"
INDEXED_TARGET = 30  # playbook 2.4: rule of thumb, at least 30 indexed pages

# Schema.org LocalBusiness and the subtypes local sites use most. Any type that
# ends in one of these words, or carries address + telephone, also counts.
LOCAL_TYPES = {
    "localbusiness", "professionalservice", "homeandconstructionbusiness",
    "plumber", "electrician", "hvacbusiness", "locksmith", "roofingcontractor",
    "generalcontractor", "housepainter", "movingcompany", "dentist", "physician",
    "medicalclinic", "medicalbusiness", "beautysalon", "hairsalon", "nailsalon",
    "dayspa", "healthandbeautybusiness", "restaurant", "cafeorcoffeeshop",
    "bakery", "barorpub", "foodestablishment", "store", "autorepair",
    "automotivebusiness", "legalservice", "attorney", "accountingservice",
    "realestateagent", "lodgingbusiness", "hotel", "healthclub",
    "sportsactivitylocation", "veterinarycare", "childcare", "travelagency",
    "financialservice", "insuranceagency", "emergencyservice",
}
AREA_WORDS = ("areas we serve", "service area", "areas served", "we serve",
              "locations", "where we work", "περιοχές", "περιοχες")
PHONE_RE = re.compile(r"(?:\+|00)?\d[\d\s().\-]{7,}\d")


def fold(text: str) -> str:
    """Lowercase and strip accents so 'Θεσσαλονίκη' matches 'θεσσαλονικη'."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.casefold()).strip()


def digits(text: str) -> str:
    return re.sub(r"\D", "", text or "")


def phone_key(text: str) -> str:
    """Last 9 digits: survives +30 / 0030 / spacing differences."""
    return digits(text)[-9:]


def _stem(word: str) -> str:
    """Crude prefix stem: 'plumbers'/'plumbing', 'Θεσσαλονίκη'/'Θεσσαλονίκης'."""
    return word[:5] if len(word) >= 6 else word


def _contains(haystack: str, needle: str) -> bool:
    words = [w for w in fold(needle).split() if len(w) > 2] or fold(needle).split()
    hay = fold(haystack)
    return bool(words) and all(_stem(w) in hay for w in words)


def _step(step, stage, name, status, evidence, fix=""):
    return {"step": step, "stage": stage, "name": name, "status": status,
            "evidence": evidence, "fix": fix}


def _jsonld_nodes(soup):
    nodes = []
    for tag in soup.find_all("script", type=re.compile("ld\\+json", re.I)):
        try:
            data = json.loads(tag.string or tag.get_text() or "")
        except (ValueError, TypeError):
            continue
        stack = [data]
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict):
                nodes.append(item)
                stack.extend(v for k, v in item.items() if k == "@graph" or isinstance(v, (dict, list)))
    return nodes


def _types(node):
    t = node.get("@type", [])
    return [fold(x) for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)]


def _page_phones(soup, text):
    phones = [a["href"][4:] for a in soup.find_all("a", href=True) if a["href"].lower().startswith("tel:")]
    phones += [m.group(0) for m in PHONE_RE.finditer(text) if 10 <= len(digits(m.group(0))) <= 15]
    seen, out = set(), []
    for p in phones:
        k = phone_key(p)
        if len(k) == 9 and k not in seen:
            seen.add(k)
            out.append(p.strip())
    return out


def analyze(html: str, url: str, keyword: str, city: str, sitemap_count=None) -> dict:
    soup = BeautifulSoup(html or "", "lxml")
    for bad in soup(["script", "style", "noscript"]):
        if bad.get("type", "").lower() != "application/ld+json":
            bad.extract()
    nodes = _jsonld_nodes(BeautifulSoup(html or "", "lxml"))
    text = soup.get_text(" ", strip=True)
    steps = []

    # 2.3 / 4.1 title
    title = (soup.title.get_text(" ", strip=True) if soup.title else "")
    has_kw, has_city = _contains(title, keyword), _contains(title, city)
    words = [w for w in re.findall(r"\w+", fold(title)) if len(w) > 3]
    repeats = sorted({w for w in words if words.count(w) > 2})
    ok = bool(title) and has_kw and has_city and len(title) <= TITLE_MAX and not repeats
    steps.append(_step("4.1", 4, "Title tag: category + city, ~200 chars max, no stuffing",
                       "pass" if ok else "fail",
                       {"title": title, "length": len(title), "keyword": has_kw,
                        "city": has_city, "repeated_words": repeats},
                       "" if ok else "BEST (if true) + category + city + business name + "
                       "2-3 top services + near me (if space). No repeated keywords."))

    # 4.2 H1 / H2
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(" ", strip=True) for h in soup.find_all("h2")]
    h1_ok = len(h1s) == 1 and _contains(h1s[0], keyword) and _contains(h1s[0], city)
    steps.append(_step("4.2", 4, "One H1 = category + city; H2s = services",
                       "pass" if h1_ok and h2s else "fail",
                       {"h1": h1s, "h2_count": len(h2s), "h2_sample": h2s[:8]},
                       "" if h1_ok and h2s else "One H1 such as '<Category> in <City>'; "
                       "H2s for secondary categories and top services."))

    # 2.2 / 4.3 NAP
    phones = _page_phones(soup, text)
    footer = soup.find("footer") or soup.find(attrs={"role": "contentinfo"})
    footer_text = footer.get_text(" ", strip=True) if footer else ""
    footer_phone = any(phone_key(p) in digits(footer_text) for p in phones) if footer_text else False
    address_nodes = [n.get("address") for n in nodes if n.get("address")]
    city_on_page = _contains(text, city)
    nap_ok = bool(phones) and city_on_page and footer_phone
    steps.append(_step("4.3a", 4, "NAP on the page and in the footer of every page",
                       "pass" if nap_ok else "fail",
                       {"phones_found": phones[:4], "city_on_page": city_on_page,
                        "footer_found": bool(footer_text), "phone_in_footer": footer_phone,
                        "schema_address": bool(address_nodes)},
                       "" if nap_ok else "Same name, address and phone as the profile, "
                       "on the homepage and in the site-wide footer."))
    steps.append(_step("2.2", 2, "NAP matches the Google Business Profile character by character",
                       "manual", {"phones_found": phones[:4]},
                       "Compare with the profile: street format, suite, phone format, name."))

    # 2.6 / 4.3 map embed
    frames = [f.get("src", "") or f.get("data-src", "") for f in soup.find_all("iframe")]
    maps = [s for s in frames if re.search(r"google\.[a-z.]+/maps|maps\.google\.", s)]
    steps.append(_step("4.3b", 4, "Google map of the profile embedded",
                       "pass" if maps else "fail", {"map_iframes": maps[:2]},
                       "" if maps else "Google Maps: open the profile > Share > Embed a map."))

    # 2.5 / 5.1 schema
    local = [n for n in nodes if any(t in LOCAL_TYPES or t.endswith("business") for t in _types(n))
             or (n.get("address") and n.get("telephone"))]
    schema_phone = [str(n.get("telephone", "")) for n in local if n.get("telephone")]
    mismatch = bool(schema_phone and phones) and not any(
        phone_key(s) in {phone_key(p) for p in phones} for s in schema_phone)
    s_ok = bool(local) and not mismatch
    steps.append(_step("5.1", 5, "LocalBusiness schema with the same NAP",
                       "pass" if s_ok else "fail",
                       {"jsonld_types": sorted({t for n in nodes for t in _types(n)}),
                        "local_nodes": len(local), "schema_phone": schema_phone[:2],
                        "phone_mismatch": mismatch},
                       "" if s_ok else "Add LocalBusiness (or the most specific type) JSON-LD "
                       "with NAP, URL, hours, geo and the profile URL; validate at validator.schema.org."))

    # 2.4 indexed pages (proxy)
    if sitemap_count is None:
        steps.append(_step("2.4", 2, "Indexed pages (aim for 30+)", "manual", {"sitemap_urls": None},
                           "Search site:yourdomain on Google and note the count."))
    else:
        steps.append(_step("2.4", 2, "Indexed pages (aim for 30+), sitemap proxy",
                           "pass" if sitemap_count >= INDEXED_TARGET else "fail",
                           {"sitemap_urls": sitemap_count, "note": "Sitemap URLs, not indexed pages. "
                            "Confirm with a site: search."},
                           "" if sitemap_count >= INDEXED_TARGET else "Stage 5: one page per "
                           "service and per area served."))

    # 5.4 areas page
    host = urlparse(url).netloc
    nav_links = [(a.get_text(" ", strip=True), urljoin(url, a["href"])) for a in soup.find_all("a", href=True)]
    areas = [h for t, h in nav_links if urlparse(h).netloc in ("", host)
             and any(w in fold(t) or w.replace(" ", "-") in fold(h) for w in AREA_WORDS)]
    steps.append(_step("5.4", 5, "'Areas we serve' page linked from the site",
                       "pass" if areas else "fail", {"area_links": areas[:3]},
                       "" if areas else "Advanced: an 'Areas we serve' page in the main menu, "
                       "one true page per area. Never claim an address you don't have."))

    summary = {s: sum(1 for x in steps if x["status"] == s) for s in ("pass", "fail", "manual")}
    return {"url": url, "keyword": keyword, "city": city, "summary": summary, "steps": steps}


def count_sitemap(url: str, timeout: int = 20):
    from url_safety import decode_response_text, safe_requests_get  # noqa: E402
    root = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    seen, todo, count = set(), [], 0
    try:
        robots = safe_requests_get(root + "/robots.txt", timeout=timeout)
        if robots.status_code == 200:
            todo += re.findall(r"(?im)^\s*sitemap:\s*(\S+)", decode_response_text(robots))
    except Exception:  # noqa: BLE001
        pass
    todo += [root + "/sitemap.xml", root + "/sitemap_index.xml"]
    while todo and len(seen) < 25:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            resp = safe_requests_get(sm, timeout=timeout)
        except Exception:  # noqa: BLE001
            continue
        if resp.status_code != 200:
            continue
        body = decode_response_text(resp)
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
        if "<sitemapindex" in body:
            todo.extend(locs)
        else:
            count += len(locs)
        if count and not todo:
            break
    return count if seen and count else None


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[1])
    ap.add_argument("url", nargs="?")
    ap.add_argument("--url", dest="url_opt")
    ap.add_argument("--html", help="Read HTML from a local file instead of fetching")
    ap.add_argument("--keyword", required=True, help="Main keyword without the city, e.g. 'plumber'")
    ap.add_argument("--city", required=True)
    ap.add_argument("--no-sitemap", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    url = args.url or args.url_opt
    if not url:
        ap.error("URL required")
    if not urlparse(url).scheme:
        url = "https://" + url
    sitemap = None
    if args.html:
        with open(args.html, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
    else:
        from url_safety import URLSafetyError, decode_response_text, safe_requests_get  # noqa: E402
        try:
            resp = safe_requests_get(url, timeout=30, allow_redirects=True)
        except URLSafetyError as exc:
            print(json.dumps({"error": f"url_safety: {exc}"}))
            return 1
        except Exception as exc:  # noqa: BLE001
            print(json.dumps({"error": str(exc)}))
            return 1
        if resp.status_code != 200:
            # A blocked or missing page would show up as a wall of false "fail" lines.
            print(json.dumps({"error": f"HTTP {resp.status_code} for {resp.url}. The site may block "
                              "automated requests: save the page from a browser and use --html."}))
            return 1
        html, url = decode_response_text(resp), resp.url
        if not args.no_sitemap:
            sitemap = count_sitemap(url)
    report = analyze(html, url, args.keyword, args.city, sitemap)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for s in report["steps"]:
            print(f"[{s['status']:>6}] {s['step']:<5} {s['name']}")
            if s["fix"] and s["status"] != "pass":
                print(f"         fix: {s['fix']}")
        print("summary:", report["summary"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
