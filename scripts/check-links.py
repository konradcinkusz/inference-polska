#!/usr/bin/env python3
"""Sprawdza, czy lokalne odnośniki i zasoby w zbudowanej stronie istnieją.

Dla każdego pliku HTML w katalogu (domyślnie wszystkie *.html) sprawdza
atrybuty href i src wskazujące na plik lokalny (bez schematu http/https/mailto/
data i bez samych kotwic #...). Odnośnik do katalogu wymaga index.html.
Odnośniki z kotwicą (plik.html#id) sprawdza także pod kątem istnienia id.
Brak pliku lub kotwicy przerywa wykonanie (kod 1) z listą błędów.

Użycie: check-links.py _site
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "//")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append((key, a[key].strip()))


def parse(path):
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


def main(root):
    root = Path(root).resolve()
    pages = sorted(root.rglob("*.html"))
    if not pages:
        sys.exit("Brak plików HTML w " + str(root))
    cache = {}
    errors = []
    checked = 0
    for page in pages:
        c = cache.setdefault(page, parse(page))
        for key, ref in c.refs:
            if not ref or ref.startswith(SKIP):
                continue
            parts = urlsplit(ref)
            where = "%s: %s=%r" % (page.relative_to(root), key, ref)
            if parts.path:
                base = page.parent
                target = (root / unquote(parts.path).lstrip("/")) if parts.path.startswith("/") else (base / unquote(parts.path))
                target = target.resolve()
                if root not in target.parents and target != root:
                    errors.append(where + " (poza katalogiem strony)")
                    continue
                if target.is_dir():
                    target = target / "index.html"
                if not target.is_file():
                    errors.append(where + " (brak pliku)")
                    continue
            else:
                target = page
            checked += 1
            if parts.fragment and target.suffix == ".html":
                ids = cache.setdefault(target, parse(target)).ids
                if unquote(parts.fragment) not in ids and unquote(parts.fragment) != "top":
                    errors.append(where + " (brak kotwicy #%s)" % parts.fragment)
    for e in errors:
        print("BŁĄD:", e)
    print("Sprawdzono %d odnośników lokalnych w %d plikach HTML, błędów: %d." % (checked, len(pages), len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
