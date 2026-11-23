#!/usr/bin/env python3
"""Buduje stronę do publikacji.

1. Wybiera szablon strony: zmienna SITE_TEMPLATE (nazwa katalogu w templates/:
   klasyczny albo ekrany). Brak zmiennej oznacza "klasyczny". Nieznana nazwa
   przerywa budowanie.
2. Usuwa z szablonu elementy oferty wyłączone zmiennymi SHOW_* (GitHub: Settings ->
   Secrets and variables -> Actions -> Variables). Zmienna ma wartość true
   (widoczne) lub false (niewidoczne), wielkość liter nie ma znaczenia. Brak
   zmiennej oznacza, że element jest widoczny. Inna wartość przerywa budowanie,
   żeby literówka nie zostawiła na stronie elementu, który miał być ukryty.
3. Sprawdza, czy poza blokami ofert nie zostały frazy ukrytych usług
   (prototyp, książka, kontrakt programistyczny, szybkie pytanie). Jeśli
   zostały, przerywa budowanie z listą miejsc.
4. Podstawia dane firmy i adres strony (zmienne środowiskowe albo wartości
   domyślne poniżej). Puste pole zamienia się w widoczny znacznik [[TODO: pole]],
   a w danych strukturalnych (JSON-LD) jest pomijane.
5. Buduje stronę aplikacja/ (pages/aplikacja/index.html) z ustawieniami z
   pages/aplikacja/instalator.json: przycisk pobierania działa dopiero, gdy podano
   url (wtedy wersja i sha256 są wymagane); "widoczna": false ukrywa odnośnik w
   menu i w sitemap i ustawia noindex.
6. Zapisuje index.html, prywatnosc/, aplikacja/, assets/, filmy/, sitemap.xml,
   robots.txt i .nojekyll w podanym katalogu.

Użycie: build-site.py _site
"""
import html as htmllib
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = "klasyczny"

# Dane firmy i adresu. Wartość można podać zmienną środowiskową o tej samej
# nazwie (w workflow: zmienna repozytorium, Settings -> Secrets and variables ->
# Actions -> Variables) albo wpisać tutaj. Puste pole = znacznik [[TODO: ...]].
SITE = {
    "SITE_URL": "https://konradcinkusz.github.io/inference-polska/",  # DOMENA: gdy jest własna, ustaw zmienną SITE_URL
    # Dane stałe (CEIDG), zahardkodowane. Zmienna środowiskowa o tej samej nazwie je nadpisuje.
    "FIRMA_NAZWA_CEIDG": "Inżynieria Oprogramowania Konrad Cinkusz",
    "NIP": "7322050993",
    "REGON": "364549089",
    "ADRES_BIURA": "ul. 1 Maja 30/40/6, 95-100 Zgierz",
    "TELEFON": "+48 732 582 477",
    "EMAIL_KONTAKT": "konradcinkusz@gmail.com",  # docelowo adres we własnej domenie
}
TODO_FIELDS = ("FIRMA_NAZWA_CEIDG", "NIP", "REGON", "ADRES_BIURA", "TELEFON", "EMAIL_KONTAKT")

# klucz znacznika w szablonie -> człon nazwy zmiennej
OFFER = {
    "analiza": "ANALIZA",
    "pytanie": "PYTANIE",
    "gabinet": "GABINET",
    "prototyp": "PROTOTYP",
    "ksiazka": "KSIAZKA",
    "kontrakt": "KONTRAKT",
}
PAIR = re.compile(r"<!--offer:(\w+):(row|desc)-->(.*?)<!--/offer:\1:\2-->", re.S)
ANCHOR = re.compile(r'<a\b[^>]*?href="#([^"]+)"[^>]*>(.*?)</a>', re.S)
EMPTY_OFFER = re.compile(r'<div class="offer">\s*</div>')
# frazy usług, które nie mogą zostać poza blokami <!--offer:...-->
HIDDEN_PHRASES = ("prototyp", "książk", "kontrakt programistyczny", "szybkie pytanie", "RATE_SHORT")
TODO_RE = re.compile(r"\[\[TODO: [^\]]+\]\]")


def enabled(name):
    value = os.environ.get(name, "").strip().lower()
    if value in ("", "true"):
        return True
    if value == "false":
        return False
    sys.exit("Zmienna %s ma niedozwoloną wartość %r (dozwolone: true, false)." % (name, value))


def flag(key, kind):
    return "SHOW_" + OFFER[key] + ("" if kind == "row" else "_OPIS")


def site_values():
    values = {}
    for key, default in SITE.items():
        values[key] = os.environ.get(key, "").strip() or default
    if not values["SITE_URL"].endswith("/"):
        values["SITE_URL"] += "/"
    if not values["SITE_URL"].startswith("https://"):
        sys.exit("SITE_URL musi zaczynać się od https:// (jest: %r)." % values["SITE_URL"])
    return values


def json_ld(v):
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Inference Polska",
        "url": v["SITE_URL"],
        "description": "Gotowy raport z analizy sprawy na podstawie dokumentów: tryb online (domyślny) lub offline. Rozmowa wstępna bezpłatna.",
        "priceRange": "od 150 zł brutto za każde rozpoczęte 50 stron",
        "areaServed": "PL",
        "founder": {"@type": "Person", "name": "Konrad Cinkusz"},
    }
    if v["FIRMA_NAZWA_CEIDG"]:
        data["legalName"] = v["FIRMA_NAZWA_CEIDG"]
    if v["NIP"]:
        data["taxID"] = v["NIP"]
    if v["EMAIL_KONTAKT"]:
        data["email"] = v["EMAIL_KONTAKT"]
    if v["TELEFON"]:
        data["telephone"] = v["TELEFON"]
    if v["ADRES_BIURA"]:
        data["address"] = {"@type": "PostalAddress", "streetAddress": v["ADRES_BIURA"], "addressCountry": "PL"}
    body = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return '<script type="application/ld+json">\n' + body + "\n</script>"


def substitute(text, v):
    """Podstawia {{...}}; puste pola firmowe stają się znacznikami [[TODO: ...]]."""
    out = text.replace("{{JSONLD}}", json_ld(v))
    for key in SITE:
        value = v[key]
        if not value and key in TODO_FIELDS:
            value = "[[TODO: %s]]" % key
        out = out.replace("{{%s}}" % key, htmllib.escape(value, quote=True))
    left = re.findall(r"\{\{\w+\}\}", out)
    if left:
        sys.exit("Niepodstawione pola w szablonie: " + ", ".join(sorted(set(left))))
    return out


INSTALLER_BLOCK = re.compile(r"<!--installer:(ready|soon)-->(.*?)<!--/installer:\1-->", re.S)
APP_LINK = re.compile(r"<!--app:link-->(.*?)<!--/app:link-->", re.S)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_app_config():
    """Ustawienia strony aplikacja/ z pages/aplikacja/instalator.json (z walidacją)."""
    cfg = json.loads((ROOT / "pages" / "aplikacja" / "instalator.json").read_text(encoding="utf-8"))
    url, version, sha = (cfg.get(k, "").strip() for k in ("url", "wersja", "sha256"))
    if not isinstance(cfg.get("widoczna"), bool):
        sys.exit("instalator.json: pole widoczna musi być true albo false.")
    if url and not url.startswith("https://"):
        sys.exit("instalator.json: url instalatora musi zaczynać się od https:// (jest: %r)." % url)
    if url and not (version and sha):
        sys.exit("instalator.json: przy ustawionym url wersja i sha256 są wymagane.")
    if sha and not SHA256_RE.match(sha):
        sys.exit("instalator.json: sha256 musi mieć 64 znaki szesnastkowe małymi literami.")
    cfg["url"], cfg["wersja"], cfg["sha256"] = url, version, sha
    cfg["rozmiar"] = cfg.get("rozmiar", "").strip()
    return cfg


def app_page(text, v, cfg):
    """Podstawia ustawienia instalatora i wybiera blok ready albo soon."""
    ready = bool(cfg["url"])
    text = INSTALLER_BLOCK.sub(lambda m: m.group(2) if (m.group(1) == "ready") == ready else "", text)
    size = (", " + cfg["rozmiar"]) if cfg["rozmiar"] else ""
    for key, value in (("APP_ROBOTS", "index,follow" if cfg["widoczna"] else "noindex,nofollow"),
                       ("INSTALLER_URL", cfg["url"]), ("INSTALLER_VERSION", cfg["wersja"]),
                       ("INSTALLER_SIZE_TEXT", size), ("INSTALLER_SHA256", cfg["sha256"])):
        text = text.replace("{{%s}}" % key, htmllib.escape(value, quote=True))
    return substitute(text, v)


def check_hidden_phrases(html, src):
    """Frazy ukrytych usług poza blokami ofert są błędem (przeciekają mimo SHOW_*=false)."""
    bare = html
    while PAIR.search(bare):
        bare = PAIR.sub(lambda m: "\n" * m.group(0).count("\n"), bare)
    found = []
    for n, line in enumerate(bare.split("\n"), 1):
        low = line.lower()
        for phrase in HIDDEN_PHRASES:
            if phrase.lower() in low:
                found.append("  %s:%d: %r: %s" % (src.name, n, phrase, line.strip()[:110]))
    if found:
        sys.exit("Frazy ukrytych usług poza blokami <!--offer:...-->:\n" + "\n".join(found))


def process(html, v, hide):
    def handle(m):
        key, kind, body = m.groups()
        if key not in OFFER:
            sys.exit("Nieznany klucz oferty w znaczniku: " + key)
        if not enabled(flag(key, kind)):
            hide.append(flag(key, kind))
            return ""
        if kind == "row" and not enabled(flag(key, "desc")):
            # wiersz oferty bez opisu: zwykły blok zamiast odnośnika do usuniętej sekcji
            body = re.sub(r'<a href="#[^"]+">', "<div>", body, count=1)
            i = body.rindex("</a>")
            body = body[:i] + "</div>" + body[i + 4:]
        return body

    while PAIR.search(html):  # bloki mogą być zagnieżdżone (np. punkt o gabinecie w bloku analizy)
        html = PAIR.sub(handle, html)
    if "<!--offer:" in html or "<!--/offer:" in html:
        sys.exit("Niedomknięty znacznik oferty.")
    html = EMPTY_OFFER.sub("", html)
    # odnośniki do usuniętych sekcji zamieniamy na zwykły tekst
    ids = set(re.findall(r'\sid="([^"]+)"', html)) | {"top"}
    html = ANCHOR.sub(lambda m: m.group(0) if m.group(1) in ids else m.group(2), html)
    return substitute(html, v)


def choose_template():
    names = sorted(p.parent.name for p in (ROOT / "templates").glob("*/index.html"))
    value = os.environ.get("SITE_TEMPLATE", "").strip().lower() or DEFAULT_TEMPLATE
    if value not in names:
        sys.exit("Zmienna SITE_TEMPLATE ma niedozwoloną wartość %r (dozwolone: %s)." % (value, ", ".join(names)))
    return value


def main(dst):
    TEMPLATE = choose_template()
    v = site_values()
    src = ROOT / "templates" / TEMPLATE / "index.html"
    template = src.read_text(encoding="utf-8")
    check_hidden_phrases(template, src)

    hide = []
    app = load_app_config()
    index = process(template, v, hide)
    index = APP_LINK.sub(lambda m: m.group(1) if app["widoczna"] else "", index)
    pages = {"index.html": index}
    priv = ROOT / "pages" / "prywatnosc" / "index.html"
    pages["prywatnosc/index.html"] = substitute(priv.read_text(encoding="utf-8"), v)
    pages["aplikacja/index.html"] = app_page((ROOT / "pages" / "aplikacja" / "index.html").read_text(encoding="utf-8"), v, app)

    out = Path(dst)
    out.mkdir(parents=True, exist_ok=True)
    for rel, text in pages.items():
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    shutil.copytree(ROOT / "assets", out / "assets", dirs_exist_ok=True)
    if (ROOT / "filmy").is_dir():
        shutil.copytree(ROOT / "filmy", out / "filmy", dirs_exist_ok=True)
        # film o aplikacji jest w menu dopiero, gdy aplikacja jest widoczna (inaczej tylko po adresie #aplikacja)
        films = out / "filmy" / "index.html"
        text = films.read_text(encoding="utf-8")
        if text.count("/*APP_HIDDEN*/true") != 1:
            sys.exit("filmy/index.html: brak znacznika /*APP_HIDDEN*/true (dokładnie jeden).")
        films.write_text(text.replace("/*APP_HIDDEN*/true", "false" if app["widoczna"] else "true"), encoding="utf-8")

    base = v["SITE_URL"]
    urls = [base, base + "prywatnosc/", base + "filmy/"] + ([base + "aplikacja/"] if app["widoczna"] else [])
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join("  <url><loc>%s</loc></url>\n" % u for u in urls) + "</urlset>\n"
    (out / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (out / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % base, encoding="utf-8")
    (out / ".nojekyll").touch()

    print("Szablon: " + TEMPLATE)
    print("Aplikacja: " + ("widoczna" if app["widoczna"] else "ukryta (noindex, bez menu)") + ", instalator " + ("podany" if app["url"] else "jeszcze nie"))
    print("Ukryte: " + (", ".join(sorted(set(hide))) if hide else "nic"))
    todos = sorted({t for text in pages.values() for t in TODO_RE.findall(text)})
    print("Znaczniki do uzupełnienia: " + (", ".join(todos) if todos else "brak"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
