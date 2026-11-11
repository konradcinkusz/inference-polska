#!/usr/bin/env python3
"""Buduje stronę do publikacji.

Usuwa z index.html elementy oferty wyłączone zmiennymi repozytorium (GitHub:
Settings -> Secrets and variables -> Actions -> Variables). Brak zmiennej
oznacza, że element jest widoczny. Wartość false, 0, no, off lub nie ukrywa go.

Użycie: build-site.py index.html _site/index.html
"""
import os
import re
import sys

# klucz znacznika w index.html -> człon nazwy zmiennej
OFFER = {
    "analiza": "ANALIZA",
    "gabinet": "GABINET",
    "prototyp": "PROTOTYP",
    "ksiazka": "KSIAZKA",
    "kontrakt": "KONTRAKT",
}
FALSE_VALUES = {"false", "0", "no", "off", "nie"}
PAIR = re.compile(r"<!--offer:(\w+):(row|desc)-->(.*?)<!--/offer:\1:\2-->", re.S)
ANCHOR = re.compile(r'<a\b[^>]*?href="#([^"]+)"[^>]*>(.*?)</a>', re.S)


def enabled(name):
    return os.environ.get(name, "").strip().lower() not in FALSE_VALUES


def flag(key, kind):
    return "SHOW_" + OFFER[key] + ("" if kind == "row" else "_OPIS")


def main(src, dst):
    html = open(src, encoding="utf-8").read()
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
        sys.exit("Niedomknięty znacznik oferty w " + src)

    # odnośniki do usuniętych sekcji zamieniamy na zwykły tekst
    ids = set(re.findall(r'\sid="([^"]+)"', html)) | {"top"}
    html = ANCHOR.sub(lambda m: m.group(0) if m.group(1) in ids else m.group(2), html)

    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(html)
    print("Ukryte: " + (", ".join(sorted(set(hidden))) if hidden else "nic"))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
