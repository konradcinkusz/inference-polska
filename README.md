# Inference Polska

Strona internetowa usługi **Inference Polska**: gotowy raport z analizy sprawy na podstawie dokumentów, zamawiany zdalnie. Domyślnie analiza odbywa się w **trybie online** (treść trafia szyfrowanym połączeniem przez API do dostawcy modelu, Anthropic, USA; domyślnie nie służy do trenowania modeli, u dostawcy jest przechowywana do 30 dni). **Tryb offline**, bez wysyłania czegokolwiek poza biuro, jest dostępny jako opcja i jest jedyny dla dokumentacji medycznej, danych objętych tajemnicą zawodową i danych szczególnych kategorii. Rozmowa wstępna jest bezpłatna i zdalna (Google Meet). Ceny: 150 zł brutto (online) albo 450 zł brutto (offline) za każde rozpoczęte 50 stron, w cenie raport i 3 rundy pytań, standardowo do 7 dni.

## Szablon i układ

Jest jeden szablon: `templates/klasyczny/index.html` (HTML, CSS i JavaScript w jednym pliku, bez zależności). Układ: stała lewa kolumna (nazwa, menu, przycisk rezerwacji), po prawej treść: nagłówek z ceną i zdaniem o trybie domyślnym, oferta i cena, krótka granica usługi, zwijane szczegóły, przykładowy raport (ukryty, patrz niżej), trzy kroki, cztery przykłady spraw, usługi dodatkowe (według zmiennych `SHOW_*`), „Kim jestem”, kontakt. Tryb online (jak działa, warunki, porównanie z własnym czatem AI, kiedy nie online) oraz w „Kim jestem” film i publikacje są w popupach (`<dialog class="pop">`, przyciski `data-open`; bez JavaScriptu wyświetlają się jako zwykłe bloki). Pozostałe szczegóły (droga materiału online, analiza offline, układ raportu, granice usługi) są w zwijanych blokach `<details>`; odnośnik do kotwicy wewnątrz zwiniętego bloku sam go otwiera. Drugi szablon („ekrany”) został usunięty; zmienna `SITE_TEMPLATE` jest ignorowana (można ją usunąć).

Sekcja „Przykładowy raport” jest w szablonie ukryta komentarzem HTML (znacznik `[[TODO: przykładowy_raport_pdf]]`). Aby ją odkryć: dodaj prawdziwe raporty PDF do `assets/raporty/`, usuń komentarz i wpisz nazwy plików. Nie generuj fikcyjnych raportów.

Dodatkowe strony: `prywatnosc/index.html` (szkielet informacji o przetwarzaniu danych z Załącznika nr 1 regulaminu, źródło: `pages/prywatnosc/index.html`) oraz `filmy/index.html` (pięć interaktywnych prezentacji).

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `templates/klasyczny/index.html` | Szablon strony głównej. |
| `pages/prywatnosc/index.html` | Szkielet strony z informacją o przetwarzaniu danych (pola `[[TODO: ...]]` do uzupełnienia). |
| `filmy/index.html` | Pięć interaktywnych prezentacji: analiza spraw, prywatna AI w gabinecie, kim jestem, „akta z pułapkami” (MIX-02), „Dlaczego warto rozwiązywać problemy na prywatnej AI” (wycieki danych w Polsce, każdy fakt oznaczony jako potwierdzony albo hipotetyczny, stan na 15.11.2026). Skróty klawiszowe 1–5 uruchamiają film z menu. Jedyne wejście to odnośnik „Filmy” w stopce. |
| `scripts/build-site.py` | Buduje stronę: usuwa elementy oferty wyłączone zmiennymi `SHOW_*`, sprawdza, czy frazy ukrytych usług nie zostały poza blokami ofert, podstawia dane firmy, generuje `sitemap.xml`, `robots.txt` i JSON-LD. |
| `scripts/check-links.py` | Sprawdza, czy każdy lokalny `href` i `src` (oraz kotwica) w zbudowanej stronie istnieje. Uruchamiany w workflow wdrożenia, przerywa je przy braku pliku. |
| `.github/workflows/deploy-pages.yml` | Wdraża stronę na GitHub Pages. |
| `.github/workflows/build-docs-pdf.yml` | Ręczne budowanie PDF-ów z `docs/papers/*.tex` (regulamin). Uruchom dopiero po ukończeniu regulaminu. |
| `assets/` | Zdjęcie, `akta/` (16 fikcyjnych akt wejściowych w PDF, na stronie są cztery), `google-calendar.png`, `og-image.svg` i `og-image.png` (grafika 1200×630 do podglądów linków). |

Strona ma jasny i ciemny motyw (domyślnie zgodny z systemem, przełącznik w pasku). Strona jest statyczna: bez cookies, bez zewnętrznych skryptów, czcionek i formularzy. Rezerwacja odbywa się poza stroną, w Kalendarzu Google. Jedyny element zewnętrzny to filmy YouTube (`youtube-nocookie.com`, identyfikator w `data-yt`), których odtwarzacz ładuje się dopiero po kliknięciu.

## Publikacja (GitHub Pages + GitHub Actions)

Workflow `deploy-pages.yml` publikuje stronę przy każdym pushu do `main` (oraz ręcznie przez *Run workflow*). Jednorazowo: **Settings → Pages → Build and deployment → Source → GitHub Actions**. Zmiana zmiennej repozytorium **nie uruchamia** publikacji: po zmianie uruchom ręcznie **Actions → Deploy to GitHub Pages → Run workflow**.

## Konfiguracja (zmienne repozytorium)

**Settings → Secrets and variables → Actions → Variables.** Dane firmy i adres strony (puste pole daje na stronie widoczny znacznik `[[TODO: nazwa]]`, a w JSON-LD jest pomijane):

| Zmienna | Znaczenie |
|---|---|
| `EMAIL_KONTAKT` | adres kontaktowy (docelowo we własnej domenie); używany w stopce, w kontakcie i w przycisku „Kopiuj adres” |
| `FIRMA_NAZWA_CEIDG`, `NIP`, `REGON`, `ADRES_BIURA`, `TELEFON` | dane firmy ze stopki i JSON-LD |
| `SITE_URL` | adres strony z `https://` (canonical, `og:url`, sitemap); domyślnie adres github.io |

Adres rezerwacji w Kalendarzu Google jest w obiekcie `CONFIG` (`BOOKING_URL`) na początku skryptu szablonu; `CONFIG.EMAIL` jest podstawiany ze zmiennej `EMAIL_KONTAKT`.

## Widoczność oferty

Każdą usługę można ukryć bez zmiany kodu: wiersz na liście oferty (`SHOW_*`) i opis (`SHOW_*_OPIS`).

| Zmienna | Co ukrywa |
|---|---|
| `SHOW_ANALIZA`, `SHOW_ANALIZA_OPIS` | wiersz i cała sekcja głównej usługi: oferta, zwijane bloki, kroki, przykłady |
| `SHOW_PYTANIE`, `SHOW_PYTANIE_OPIS` | „Szybkie pytanie” (100 zł brutto, zawsze offline) |
| `SHOW_GABINET`, `SHOW_GABINET_OPIS` | „Prywatna sztuczna inteligencja w Twoim gabinecie” (zawsze offline) |
| `SHOW_PROTOTYP`, `SHOW_PROTOTYP_OPIS` | „Prototyp w tydzień” |
| `SHOW_KSIAZKA`, `SHOW_KSIAZKA_OPIS` | „Książka na zamówienie” |
| `SHOW_KONTRAKT`, `SHOW_KONTRAKT_OPIS` | „Kontrakt programistyczny” razem z kalkulatorem stawek |

Wartość `true` albo `false`; brak zmiennej oznacza widoczne; inna wartość przerywa publikację. Wszystkie wzmianki o danej usłudze (też w menu, tekście i skryptach) są w blokach `<!--offer:KLUCZ:row|desc-->`. Build przerywa się, jeśli frazy ukrytych usług zostały poza takimi blokami.

## Podgląd lokalny

```bash
SHOW_PYTANIE=false SHOW_PYTANIE_OPIS=false SHOW_PROTOTYP=false SHOW_PROTOTYP_OPIS=false SHOW_KSIAZKA=false SHOW_KSIAZKA_OPIS=false SHOW_KONTRAKT=false SHOW_KONTRAKT_OPIS=false python3 scripts/build-site.py _site
python3 scripts/check-links.py _site
python3 -m http.server 8000 -d _site
```

Katalog `_site/` jest w `.gitignore`.

## Autor

Konrad Cinkusz

© 2026 Konrad Cinkusz
