#!/usr/bin/env python3
"""Builds privacy.html from texts.py.

All languages sit on one page; the reader's browser language picks one, and an
anchor such as privacy.html#ru overrides it. Built the same way as
~/Developer/wow-fasting-legal and ~/Developer/toshas-farm-legal so the three
are maintained alike.
"""
import html
import json
import os

from texts import LANGS, NAMES, SECTIONS, TEXTS

EMAIL = "vladislava.bogaturova@gmail.com"
DEV = "Vladyslava Ostapchuk"
UPDATED = "2026-10-17"
APP = "Tinta"

# Colours come from the app itself (app/src/theme.ts): warm paper, near-black ink.
CSS = """
:root{--accent:#16150f;--bg:#ffffff;--surface:#f6f5f3;--fg:#16150f;--muted:#6e6a60;--rule:#e2dfd9}
@media (prefers-color-scheme:dark){:root{--accent:#f3f1ec;--bg:#131210;--surface:#1d1b18;--fg:#f3f1ec;--muted:#a8a299;--rule:#332f2a}}
*{box-sizing:border-box}
/* Long words such as «конфіденційності» overflow a phone screen otherwise. */
body{margin:0;font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
header{border-bottom:1px solid var(--rule);padding:22px 16px}
header .in,main{max-width:760px;margin:0 auto}
header h1{margin:0;font-size:28px;letter-spacing:-.4px}
header p{margin:4px 0 0;color:var(--muted)}
nav.lang{display:flex;flex-wrap:wrap;gap:6px;margin:18px 0}
nav.lang a{padding:4px 12px;border-radius:14px;background:var(--surface);color:var(--fg);text-decoration:none;font-size:14px;border:1px solid var(--rule)}
nav.lang a.on{background:var(--accent);color:var(--bg);border-color:var(--accent)}
main{padding:8px 16px 48px}
h2{margin:28px 0 6px;font-size:19px}
section.l h1{font-size:24px;margin:8px 0 4px}
em{color:var(--muted)}
a{color:var(--fg)}
section.l{display:none}
section.l.on{display:block}
footer{max-width:760px;margin:0 auto;padding:0 16px 32px;font-size:14px;color:var(--muted)}
"""

JS = """
(function(){var L=%s;var q=(location.hash||'').replace('#','');
function pick(){if(L.indexOf(q)>=0)return q;var n=(navigator.languages||[navigator.language||'en']);
for(var i=0;i<n.length;i++){var c=String(n[i]).toLowerCase().slice(0,2);if(L.indexOf(c)>=0)return c;}return 'en';}
function show(c){document.documentElement.lang=c;document.querySelectorAll('section.l').forEach(function(s){s.classList.toggle('on',s.id==='l-'+c)});
document.querySelectorAll('nav.lang a').forEach(function(a){a.classList.toggle('on',a.dataset.l===c)});}
document.querySelectorAll('nav.lang a').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();history.replaceState(null,'','#'+a.dataset.l);show(a.dataset.l)})});
show(pick());})();
""" % json.dumps(LANGS)


def e(s):
    return html.escape(s, quote=False)


def build_page(kind):
    nav = "".join(f'<a href="#{c}" data-l="{c}">{NAMES[c]}</a>' for c in LANGS)
    sections = []
    for c in LANGS:
        t = TEXTS[c]
        if kind == "privacy":
            body = [f"<p><em>{e(t['updated'])}: {UPDATED}</em></p>"]
            for key in SECTIONS:
                body.append(f"<h2>{e(t[key + '_h'])}</h2><p>{e(t[key])}</p>")
            title = t["title"]
        else:
            body = [f"<p>{e(t['s_intro'])}</p>"]
            body.append(f"<h2>{e(t['contact_h'])}</h2><p>{e(t['contact'])} <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>")
            for key in ("s1", "s2", "s3"):
                body.append(f"<h2>{e(t[key + '_h'])}</h2><p>{e(t[key])}</p>")
            title = t["support_title"]
        if kind == "privacy":
            body.append(f"<h2>{e(t['contact_h'])}</h2><p>{e(t['contact'])} <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>")
        body.append(f"<p>{e(DEV)}</p>")
        sections.append(
            f'<section class="l" id="l-{c}" lang="{c}"><h1>{e(title)}</h1>{"".join(body)}</section>'
        )

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(APP)}: {e(TEXTS['en']['title' if kind == 'privacy' else 'support_title'])}</title><meta name="robots" content="index,follow"><style>{CSS}</style></head><body>
<header><div class="in"><h1>{e(APP)}</h1><p>{e(DEV)}</p></div></header>
<main><nav class="lang">{nav}</nav>{''.join(sections)}</main>
<footer><a href="privacy.html">Privacy</a> · <a href="support.html">Support</a><br>© 2026 {e(DEV)}</footer><script>{JS}</script></body></html>"""
    name = "privacy.html" if kind == "privacy" else "support.html"
    with open(os.path.join(os.path.dirname(__file__) or ".", name), "w", encoding="utf-8") as f:
        f.write(page)
    print("built", name, ":", len(LANGS), "languages")


def build():
    build_page("privacy")
    build_page("support")


if __name__ == "__main__":
    build()
