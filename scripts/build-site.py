#!/usr/bin/env python3
"""Buduje stronę do publikacji.

1. Wybiera szablon strony: zmienna SITE_TEMPLATE (nazwa katalogu w templates/).
   Brak zmiennej oznacza szablon "klasyczny". Nieznana nazwa przerywa budowanie.
2. Usuwa z szablonu elementy oferty wyłączone zmiennymi SHOW_* (GitHub: Settings ->
   Secrets and variables -> Actions -> Variables). Zmienna ma wartość true
   (widoczne) lub false (niewidoczne), wielkość liter nie ma znaczenia. Brak
   zmiennej oznacza, że element jest widoczny. Inna wartość przerywa budowanie,
   żeby literówka nie zostawiła na stronie elementu, który miał być ukryty.
3. Zapisuje index.html, assets/ i .nojekyll w podanym katalogu.

Użycie: build-site.py _site
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = "klasyczny"

# klucz znacznika w szablonie -> człon nazwy zmiennej
OFFER = {
    "analiza": "ANALIZA",
    "gabinet": "GABINET",
    "prototyp": "PROTOTYP",
    "ksiazka": "KSIAZKA",
    "kontrakt": "KONTRAKT",
}
PAIR = re.compile(r"<!--offer:(\w+):(row|desc)-->(.*?)<!--/offer:\1:\2-->", re.S)
ANCHOR = re.compile(r'<a\b[^>]*?href="#([^"]+)"[^>]*>(.*?)</a>', re.S)


def enabled(name):
    value = os.environ.get(name, "").strip().lower()
    if value in ("", "true"):
        return True
    if value == "false":
        return False
    sys.exit("Zmienna %s ma niedozwoloną wartość %r (dozwolone: true, false)." % (name, value))


def flag(key, kind):
    return "SHOW_" + OFFER[key] + ("" if kind == "row" else "_OPIS")


def choose_template():
    names = sorted(p.parent.name for p in (ROOT / "templates").glob("*/index.html"))
    value = os.environ.get("SITE_TEMPLATE", "").strip().lower() or DEFAULT_TEMPLATE
    if value not in names:
        sys.exit("Zmienna SITE_TEMPLATE ma niedozwoloną wartość %r (dozwolone: %s)." % (value, ", ".join(names)))
    return value


def main(dst):
    name = choose_template()
    src = ROOT / "templates" / name / "index.html"
    html = src.read_text(encoding="utf-8")
    hidden = []

    def handle(m):
        key, kind, body = m.groups()
        if key not in OFFER:
            sys.exit("Nieznany klucz oferty w znaczniku: " + key)
        if not enabled(flag(key, kind)):
            hidden.append(flag(key, kind))
            return ""
        if kind == "row" and not enabled(flag(key, "desc")):
            # wiersz oferty bez opisu: zwykły blok zamiast odnośnika do usuniętej sekcji
            body = re.sub(r'<a href="#[^"]+">', "<div>", body, count=1)
            i = body.rindex("</a>")
            body = body[:i] + "</div>" + body[i + 4:]
        return body

    html = PAIR.sub(handle, html)
    if "<!--offer:" in html or "<!--/offer:" in html:
        sys.exit("Niedomknięty znacznik oferty w " + str(src))

    # odnośniki do usuniętych sekcji zamieniamy na zwykły tekst
    ids = set(re.findall(r'\sid="([^"]+)"', html)) | {"top"}
    html = ANCHOR.sub(lambda m: m.group(0) if m.group(1) in ids else m.group(2), html)

    out = Path(dst)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    shutil.copytree(ROOT / "assets", out / "assets", dirs_exist_ok=True)
    (out / ".nojekyll").touch()
    print("Szablon: " + name)
    print("Ukryte: " + (", ".join(sorted(set(hidden))) if hidden else "nic"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
