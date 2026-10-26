"""playbook_check.py: website checks from The Local SEO Playbook (Stages 2, 4, 5)."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import playbook_check  # noqa: E402

GOOD = """<!doctype html><html><head>
<title>Best Plumber Springfield - Acme Plumbing - Emergency Plumbing, Drain Cleaning near me</title>
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[
 {"@type":"Plumber","name":"Acme Plumbing","telephone":"+1 (217) 555-0142",
  "address":{"@type":"PostalAddress","addressLocality":"Springfield"}}]}</script>
</head><body>
<nav><a href="/services">Services</a><a href="/areas-we-serve">Areas we serve</a></nav>
<h1>Plumber in Springfield</h1><h2>Emergency plumbing</h2><h2>Drain cleaning</h2>
<iframe src="https://www.google.com/maps/embed?pb=abc"></iframe>
<footer>Acme Plumbing, 1 Main St, Springfield. Call <a href="tel:+12175550142">(217) 555-0142</a></footer>
</body></html>"""

WEAK = """<html><head><title>Home</title></head><body>
<h1>Welcome</h1><h1>About us</h1><p>We fix pipes.</p></body></html>"""

GREEK = """<html><head><title>Υδραυλικός Θεσσαλονίκη | Ακμή</title></head><body>
<h1>Υδραυλικός στη Θεσσαλονίκη</h1><h2>Αποφράξεις</h2>
<footer>Ακμή, Τσιμισκή 1, Θεσσαλονικη, τηλ. 2310 555 014</footer></body></html>"""


def _by_step(report):
    return {s["step"]: s for s in report["steps"]}


def test_good_local_page_passes_every_site_step():
    r = playbook_check.analyze(GOOD, "https://acme.example/", "plumber", "Springfield", 42)
    steps = _by_step(r)
    for step in ("4.1", "4.2", "4.3a", "4.3b", "5.1", "2.4", "5.4"):
        assert steps[step]["status"] == "pass", (step, steps[step])
    assert steps["2.2"]["status"] == "manual"
    assert r["summary"] == {"pass": 7, "fail": 0, "manual": 1}


def test_weak_page_fails_with_playbook_fixes():
    r = playbook_check.analyze(WEAK, "https://weak.example/", "plumber", "Springfield", 5)
    steps = _by_step(r)
    for step in ("4.1", "4.2", "4.3a", "4.3b", "5.1", "2.4", "5.4"):
        assert steps[step]["status"] == "fail", step
        assert steps[step]["fix"], step
    assert steps["4.2"]["evidence"]["h1"] == ["Welcome", "About us"]


def test_title_stuffing_and_length_fail():
    stuffed = "<title>Plumber Springfield plumber plumber Springfield plumber</title><h1>x</h1>"
    r = _by_step(playbook_check.analyze(stuffed, "https://x.example/", "plumber", "Springfield"))
    assert r["4.1"]["status"] == "fail"
    assert "plumber" in r["4.1"]["evidence"]["repeated_words"]
    long_title = "<title>Plumber Springfield " + "a" * 220 + "</title>"
    r = _by_step(playbook_check.analyze(long_title, "https://x.example/", "plumber", "Springfield"))
    assert r["4.1"]["evidence"]["length"] > playbook_check.TITLE_MAX
    assert r["4.1"]["status"] == "fail"


def test_greek_accents_fold_and_footer_phone():
    r = _by_step(playbook_check.analyze(GREEK, "https://akmi.example/", "υδραυλικός", "Θεσσαλονίκη"))
    assert r["4.1"]["status"] == "pass"
    assert r["4.2"]["status"] == "pass"
    assert r["4.3a"]["status"] == "pass"


def test_schema_phone_mismatch_is_flagged():
    html = GOOD.replace('"+1 (217) 555-0142"', '"+1 (217) 555-9999"')
    r = _by_step(playbook_check.analyze(html, "https://acme.example/", "plumber", "Springfield", 42))
    assert r["5.1"]["evidence"]["phone_mismatch"] is True
    assert r["5.1"]["status"] == "fail"


def test_no_sitemap_keeps_indexed_pages_manual():
    r = _by_step(playbook_check.analyze(GOOD, "https://acme.example/", "plumber", "Springfield"))
    assert r["2.4"]["status"] == "manual"


def test_cli_reads_local_html(tmp_path):
    page = tmp_path / "page.html"
    page.write_text(GOOD, encoding="utf-8")
    out = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "playbook_check.py"), "--html", str(page),
         "--url", "https://acme.example/", "--keyword", "plumber", "--city", "Springfield", "--json"],
        capture_output=True, text=True, check=True)
    data = json.loads(out.stdout)
    assert data["summary"]["fail"] == 0


def test_stems_match_inflected_words():
    html = "<title>Plumbers Springfield</title><h1>Υδραυλικοί στη Θεσσαλονίκης</h1>"
    r = _by_step(playbook_check.analyze(html, "https://x.example/", "plumbing", "Springfield"))
    assert r["4.1"]["evidence"]["keyword"] is True
    r = _by_step(playbook_check.analyze(html, "https://x.example/", "υδραυλικός", "Θεσσαλονίκη"))
    assert r["4.2"]["evidence"]["h1"] and r["4.2"]["status"] == "fail"  # no H2s
