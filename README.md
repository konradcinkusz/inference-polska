# Inference Polska

Strona internetowa usługi **Inference Polska**: analiza spraw i wrażliwych dokumentów przez prywatną sztuczną inteligencję: lokalny model na maszynie bez dostępu do sieci. Klient dostaje raport w jednym z dwóch formatów: elegancki PDF (wydrukowany albo wysłany zaszyfrowany) lub elegancki HTML w stylu Wikipedii. Po zakończeniu wszystkie dane cyfrowe są usuwane z maszyny. Rozmowa wstępna jest bezpłatna, a analiza spraw kosztuje 150 zł brutto za każde rozpoczęte 50 stron dokumentów. Analizę spraw, prototypy i książki na zamówienie można zlecić także w trybie cloud; strona opisuje, jak ten tryb działa i na jakich warunkach przetwarzane są dane.

## Szablony strony

Ta sama treść jest dostępna w dwóch układach. Wybiera się go zmienną repozytorium `SITE_TEMPLATE` (**Settings → Secrets and variables → Actions → Variables**):

| Wartość | Układ | Plik |
|---|---|---|
| `klasyczny` (domyślnie, także gdy zmiennej nie ma) | stała lewa kolumna i długa strona z sekcjami oraz zwijanymi blokami | `templates/klasyczny/index.html` |
| `ekrany` | jeden ekran z jedną informacją w jednej chwili; przewijanie przechodzi do następnego ekranu | `templates/ekrany/index.html` |

Inna wartość (np. literówka) przerywa publikację z komunikatem w logu. Zmiana zmiennej **nie uruchamia** publikacji: po zmianie uruchom ręcznie **Actions → Deploy to GitHub Pages → Run workflow**. Zmienne `SHOW_*` (niżej) działają w obu szablonach.

Treść jest w obu plikach osobno. Zmiana tekstu, ceny, `CONFIG` (e-mail, adres rezerwacji) albo stawek kontraktu wymaga edycji obu szablonów.

## Układ szablonu „klasyczny”

Na komputerze strona ma stałą lewą kolumnę (nazwa, jedno zdanie opisu, menu, przycisk rozmowy wstępnej) i treść po prawej. Na telefonie kolumna staje się górnym paskiem z rozwijanym menu. Jeden krój pisma, cienkie linie zamiast kart, bez cieni i ikon. Szczegóły (kroki, układ raportu, granice usługi, warunki trybu cloud, publikacje) są w zwijanych blokach; odnośnik do kotwicy wewnątrz zwiniętego bloku sam go otwiera.

## Układ szablonu „ekrany”

W jednej chwili widać jeden ekran z jedną informacją. Na górze jest delikatny pasek: nazwa, cztery pozycje menu (Oferta, Tryb pracy, O mnie, Kontakt) i przełącznik motywu. Ekrany leżą jeden pod drugim, każdy na całą wysokość okna, a przewijanie (kółko, gest, klawiatura, strzałka ↓ na dole ekranu) przeskakuje do następnego ekranu (CSS `scroll-snap`). Menu i adres w pasku przeglądarki podążają za bieżącym ekranem, więc można podać odnośnik do konkretnego ekranu (`#analiza`, `#cena`).

Są trzy rodzaje ekranów:

- **Ekran z jednym przyciskiem** (strona główna, każda usługa, kontakt): nagłówek, najwyżej jedno zdanie i jeden duży przycisk „Umów darmową rozmowę wstępną”. Pod spodem drobnym drukiem cena i delikatne odnośniki do szczegółów.
- **Ekran ze szczegółem** (np. „Jak to działa”, „Cena”): jeden temat. Na górze powrót do usługi, na dole przycisk rezerwacji. Ekran wyższy niż okno przewija się wewnątrz.
- **Ekran wyboru** (`#oferta`): lista usług.

Powrót, przycisk na dole, strzałki i lista szczegółów pod usługą powstają w skrypcie z atrybutów `data-parent` i `data-title` ekranu, w kolejności z pliku. Nowy ekran ze szczegółem to nowy `<section class="view" id="..." data-parent="..." data-title="...">`. Bez JavaScriptu ekrany są widoczne jeden pod drugim.

## Zawartość (ekrany i sekcje)

| Ekran lub sekcja | Szczegóły (ekrany podrzędne; w szablonie „klasycznym” to zwijane bloki) |
|---|---|
| Strona główna (`#top`) | |
| Oferta (`#oferta`) | pięć usług z ceną lub „wycena po rozmowie” |
| Analiza spraw (`#analiza`) | `#jak`, `#rozwiazanie`, `#diagram`, `#raport`, `#cena`, `#przyklady`, `#granice`, `#problem` |
| Prywatna sztuczna inteligencja w Twoim gabinecie (`#firmy`) | `#firmy-jak`, `#pakiety` |
| Prototyp w tydzień (`#poc`) | `#poc-jak` |
| Książka na zamówienie (`#ksiazka`) | `#ksiazka-opis`, `#ksiazka-kroki` |
| Kontrakt programistyczny (`#kontrakt`) | `#stawka` |
| Tryb pracy (`#tryb`) | `#cloud`, `#cloud-warunki`, `#cloud-porownanie`, `#cloud-kiedy-nie` |
| Kim jestem (`#o-mnie`) | |
| Kontakt (`#rozmowa`) | |

- **Przykładowe sprawy** (`#przyklady`): 16 fikcyjnych akt w czterech grupach, z linkami do PDF-ów w `assets/akta/`. Pliki są kopią wydania `pdfs` z repozytorium `iference-polska-use-cases`; po zmianie akt trzeba je skopiować ponownie.
- **Kontrakt programistyczny** (`#stawka`): praca godzinowa, 180 zł netto za godzinę przy kontrakcie do 3 miesięcy, 125 zł netto przy kontrakcie na 3 lata (maksymalna długość), długość kontraktu wybiera się suwakiem (1–36 miesięcy), a stawka maleje liniowo między tymi punktami (orientacyjnie; dokładną ustala się po rozmowie wstępnej). Koszt tokenów ponosi wykonawca. Pole „Inferencja lokalna” dolicza 15% (słabsze modele, większy wkład programisty w weryfikację, dłuższe generowanie, zużycie energii). Stałe stawek są na początku skryptu kontraktu w szablonie (`RATE_SHORT`, `RATE_LONG`, `LOCAL_SURCHARGE`).
- **Tryb pracy** (`#tryb`): droższy *fully private* na modelach lokalnych i tańszy *cloud*, dla analizy spraw, prototypu, książki i kontraktu programistycznego (nie dla wynajmu urządzenia w gabinecie). Ekrany `#cloud…`: kroki, warunki przetwarzania, porównanie z kontem indywidualnym, kiedy nie cloud.
- **Kontakt** (`#rozmowa`): duży przycisk do rezerwacji w Kalendarzu Google i adres e-mail. Każdy przycisk „Umów darmową rozmowę wstępną” na stronie prowadzi wprost do rezerwacji (nowa karta, ikona Kalendarza Google). Kliknięcie adresu e-mail nie otwiera programu pocztowego, tylko kopiuje adres do schowka i pokazuje duży napis.

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `templates/klasyczny/index.html`, `templates/ekrany/index.html` | Szablony strony: HTML, CSS i JavaScript w jednym pliku, bez zależności. |
| `.nojekyll` | Wyłącza przetwarzanie Jekyll na GitHub Pages. |
| `.github/workflows/deploy-pages.yml` | Akcja wdrażająca stronę na GitHub Pages. |
| `scripts/build-site.py` | Skrypt budujący stronę: wybiera szablon (`SITE_TEMPLATE`) i usuwa elementy oferty wyłączone zmiennymi repozytorium. |
| `assets/` | Zdjęcie do sekcji „Kim jestem”, `akta/` (16 fikcyjnych akt w PDF do sekcji „Przykładowe sprawy”) oraz `google-calendar.png` (ikona Kalendarza Google z przycisków rezerwacji, pomniejszona kopia pliku z Wikimedia Commons; znak towarowy Google). |
| `README.md` | Ten plik. |

Strona ma jasny i ciemny motyw: domyślnie zgodny z ustawieniem systemu, z przełącznikiem w górnym pasku (wybór zapamiętywany w przeglądarce).

Strona jest statyczna: bez cookies, bez zewnętrznych skryptów, czcionek i formularzy. Rezerwacja terminu odbywa się poza stroną, w Kalendarzu Google.

## Publikacja (GitHub Pages + GitHub Actions)

Workflow `.github/workflows/deploy-pages.yml` publikuje stronę zbudowaną z wybranego szablonu przy każdym pushu do `main` (oraz ręcznie przez *Run workflow*).

Jednorazowo: **Settings → Pages → Build and deployment → Source → GitHub Actions**.

Strona będzie dostępna pod `https://konradcinkusz.github.io/inference-polska/`.

## Konfiguracja

Ustawienia są w obiekcie `CONFIG` na początku skryptu w każdym szablonie (`templates/*/index.html`, zmieniaj w obu):

- `EMAIL`: adres kontaktowy,
- `BOOKING_URL`: adres strony rezerwacji z Kalendarza Google (terminarz spotkań); używają go wszystkie przyciski „Umów darmową rozmowę wstępną”.

## Widoczność oferty (zmienne repozytorium)

Każdą usługę z oferty można ukryć bez zmiany kodu, zmiennymi repozytorium GitHub: **Settings → Secrets and variables → Actions → Variables → New repository variable**. Każda usługa ma dwie zmienne: jedną dla jej wiersza na liście oferty i jedną dla opisu (ekran usługi razem z ekranami szczegółów).

| Zmienna | Co ukrywa |
|---|---|
| `SHOW_ANALIZA` | wiersz „Analiza spraw” na liście oferty |
| `SHOW_ANALIZA_OPIS` | ekran „Analiza spraw” (`#analiza`) i wszystkie jego ekrany szczegółów, w tym „Przykładowe sprawy” (`#przyklady`) |
| `SHOW_GABINET`, `SHOW_GABINET_OPIS` | wiersz i ekrany „Prywatna sztuczna inteligencja w Twoim gabinecie” (`#firmy`) |
| `SHOW_PROTOTYP`, `SHOW_PROTOTYP_OPIS` | wiersz i ekrany „Prototyp w tydzień” (`#poc`) |
| `SHOW_KSIAZKA`, `SHOW_KSIAZKA_OPIS` | wiersz i ekrany „Książka na zamówienie” (`#ksiazka`) |
| `SHOW_KONTRAKT`, `SHOW_KONTRAKT_OPIS` | wiersz i ekrany „Kontrakt programistyczny” (`#kontrakt`) |

- Zmienna ma wartość `true` (widoczne) albo `false` (niewidoczne); wielkość liter nie ma znaczenia. Brak zmiennej oznacza, że element jest widoczny. Inna wartość (np. literówka `flase`) przerywa publikację z komunikatem w logu, żeby element, który miał być ukryty, nie został po cichu na stronie.
- Ukryty element w ogóle nie trafia do opublikowanej strony (ani HTML, ani ceny). Wiersz oferty bez ukrytego opisu zostaje jako zwykły tekst bez odnośnika, a odnośniki do usuniętych ekranów w tekście zamieniają się w zwykły tekst.
- Zmiana zmiennej **nie uruchamia** publikacji. Po zmianie uruchom ręcznie workflow: **Actions → Deploy to GitHub Pages → Run workflow**.
- Przełączane są tylko wiersze oferty i ekrany usług (`scripts/build-site.py`). Wzmianki w zwykłym tekście (`<meta>`, ekran „Tryb pracy”) pozostają bez zmian.
- Podgląd z flagami: `SHOW_KONTRAKT=false python3 scripts/build-site.py _site`.

## Podgląd lokalny

```bash
SITE_TEMPLATE=ekrany python3 scripts/build-site.py _site
python3 -m http.server 8000 -d _site
```

Następnie otwórz `http://localhost:8000`. Bez `SITE_TEMPLATE` powstaje szablon „klasyczny”; katalog `_site/` jest w `.gitignore`.

## Autor

Konrad Cinkusz · konradcinkusz@gmail.com

© 2026 Konrad Cinkusz
