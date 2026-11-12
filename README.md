# Inference Polska

Strona internetowa usługi **Inference Polska**: analiza spraw i wrażliwych dokumentów przez prywatną sztuczną inteligencję: lokalny model na maszynie bez dostępu do sieci. Klient dostaje raport w jednym z dwóch formatów: elegancki PDF (wydrukowany albo wysłany zaszyfrowany) lub elegancki HTML w stylu Wikipedii. Po zakończeniu wszystkie dane cyfrowe są usuwane z maszyny. Rozmowa wstępna jest bezpłatna, a analiza spraw kosztuje 150 zł brutto za każde rozpoczęte 50 stron dokumentów. Analizę spraw, prototypy i książki na zamówienie można zlecić także w trybie cloud; strona opisuje, jak ten tryb działa i na jakich warunkach przetwarzane są dane.

## Układ

Na komputerze strona ma stałą lewą kolumnę (nazwa, jedno zdanie opisu, menu, przycisk rozmowy wstępnej) i treść po prawej. Na telefonie kolumna staje się górnym paskiem z rozwijanym menu. Jeden krój pisma, cienkie linie zamiast kart, bez cieni i ikon. Jedyny efekt to podświetlenie wiersza na liście „Oferta”. Szczegóły (kroki, układ raportu, granice usługi, warunki trybu cloud, publikacje) są w zwijanych blokach; odnośnik do kotwicy wewnątrz zwiniętego bloku sam go otwiera.

## Sekcje strony

0. **Oferta** (`#oferta`): pięć usług jako duża lista z ceną lub „wycena po rozmowie”.

1. **Analiza spraw** (`#analiza`): rozwiązanie i cena, a w zwijanych blokach problem (`#problem`), przebieg (`#jak`), wynik (`#raport`) i granice usługi (`#granice`).
2. **Przykładowe sprawy** (`#przyklady`): 16 fikcyjnych akt w czterech grupach, z linkami do PDF-ów w `assets/akta/`. Pliki są kopią wydania `pdfs` z repozytorium `iference-polska-use-cases`; po zmianie akt trzeba je skopiować ponownie.
3. **Prywatna sztuczna inteligencja w Twoim gabinecie** (`#firmy`): Pakiet Biuro, Pakiet Gabinet i Pakiet Pro, wycena na zapytanie.
4. **Prototyp w tydzień** (`#poc`).
5. **Książka na zamówienie** (`#ksiazka`).
6. **Kontrakt programistyczny** (`#kontrakt`): praca godzinowa, 180 zł netto za godzinę przy kontrakcie do 3 miesięcy, 125 zł netto przy kontrakcie na 3 lata (maksymalna długość), długość kontraktu wybiera się suwakiem (1–36 miesięcy), a stawka maleje liniowo między tymi punktami (orientacyjnie; dokładną ustala się po rozmowie wstępnej). Koszt tokenów ponosi wykonawca. Pole „Inferencja lokalna” dolicza 15% (słabsze modele, większy wkład programisty w weryfikację, dłuższe generowanie, zużycie energii). Stałe stawek są na początku skryptu kontraktu w `index.html` (`RATE_SHORT`, `RATE_LONG`, `LOCAL_SURCHARGE`).
7. **Tryb pracy** (`#tryb`): droższy *fully private* na modelach lokalnych i tańszy *cloud*, dla analizy spraw, prototypu, książki i kontraktu programistycznego (nie dla wynajmu urządzenia w gabinecie). Blok „Jak dokładnie działa tryb cloud” (`#cloud`): kroki, warunki przetwarzania, porównanie z kontem indywidualnym, kiedy nie cloud.
8. **Kim jestem** (`#o-mnie`).
9. **Umów darmową rozmowę wstępną** (`#rozmowa`): przycisk do rezerwacji w Kalendarzu Google i adres e-mail. Każdy przycisk „Umów darmową rozmowę wstępną” na stronie prowadzi wprost do rezerwacji (nowa karta, ikona Kalendarza Google). Kliknięcie adresu e-mail nie otwiera programu pocztowego, tylko kopiuje adres do schowka i pokazuje duży napis.

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `index.html` | Cała strona: HTML, CSS i JavaScript w jednym pliku, bez zależności. |
| `.nojekyll` | Wyłącza przetwarzanie Jekyll na GitHub Pages. |
| `.github/workflows/deploy-pages.yml` | Akcja wdrażająca stronę na GitHub Pages. |
| `filmy/index.html` | Osobna strona z trzema interaktywnymi filmami (prezentacje: analiza spraw, prywatna AI w gabinecie, kim jestem). Jedyne wejście do niej to odnośnik „Filmy” w stopce strony głównej; nie ma jej w menu ani w ofercie. Zdjęcie bierze z `assets/konrad-cinkusz.jpg`. |
| `scripts/build-site.py` | Skrypt budujący stronę: usuwa elementy oferty wyłączone zmiennymi repozytorium. |
| `assets/` | Zdjęcie do sekcji „Kim jestem”, `akta/` (16 fikcyjnych akt w PDF do sekcji „Przykładowe sprawy”) oraz `google-calendar.png` (ikona Kalendarza Google z przycisków rezerwacji, pomniejszona kopia pliku z Wikimedia Commons; znak towarowy Google). |
| `README.md` | Ten plik. |

Strona ma jasny i ciemny motyw: domyślnie zgodny z ustawieniem systemu, z przełącznikiem w lewej kolumnie (na telefonie w górnym pasku) (wybór zapamiętywany w przeglądarce).

Strona jest statyczna: bez cookies, bez zewnętrznych skryptów, czcionek i formularzy. Rezerwacja terminu odbywa się poza stroną, w Kalendarzu Google.

## Publikacja (GitHub Pages + GitHub Actions)

Workflow `.github/workflows/deploy-pages.yml` publikuje `index.html` przy każdym pushu do `main` (oraz ręcznie przez *Run workflow*).

Jednorazowo: **Settings → Pages → Build and deployment → Source → GitHub Actions**.

Strona będzie dostępna pod `https://konradcinkusz.github.io/inference-polska/`.

## Konfiguracja

Ustawienia są w obiekcie `CONFIG` na początku skryptu w `index.html`:

- `EMAIL`: adres kontaktowy,
- `BOOKING_URL`: adres strony rezerwacji z Kalendarza Google (terminarz spotkań); używają go wszystkie przyciski „Umów darmową rozmowę wstępną”.

## Widoczność oferty (zmienne repozytorium)

Każdą usługę z oferty można ukryć bez zmiany kodu, zmiennymi repozytorium GitHub: **Settings → Secrets and variables → Actions → Variables → New repository variable**. Każda usługa ma dwie zmienne: jedną dla jej wiersza na liście oferty i jedną dla opisu (sekcja i pozycja w menu).

| Zmienna | Co ukrywa |
|---|---|
| `SHOW_ANALIZA` | wiersz „Analiza spraw” na liście oferty |
| `SHOW_ANALIZA_OPIS` | sekcje „Analiza spraw” (`#analiza`) i „Przykładowe sprawy” (`#przyklady`) oraz ich pozycje w menu |
| `SHOW_GABINET`, `SHOW_GABINET_OPIS` | wiersz i sekcja „Prywatna sztuczna inteligencja w Twoim gabinecie” (`#firmy`) |
| `SHOW_PROTOTYP`, `SHOW_PROTOTYP_OPIS` | wiersz i sekcja „Prototyp w tydzień” (`#poc`) |
| `SHOW_KSIAZKA`, `SHOW_KSIAZKA_OPIS` | wiersz i sekcja „Książka na zamówienie” (`#ksiazka`) |
| `SHOW_KONTRAKT`, `SHOW_KONTRAKT_OPIS` | wiersz i sekcja „Kontrakt programistyczny” (`#kontrakt`) |

- Zmienna ma wartość `true` (widoczne) albo `false` (niewidoczne); wielkość liter nie ma znaczenia. Brak zmiennej oznacza, że element jest widoczny. Inna wartość (np. literówka `flase`) przerywa publikację z komunikatem w logu, żeby element, który miał być ukryty, nie został po cichu na stronie.
- Ukryty element w ogóle nie trafia do opublikowanej strony (ani HTML, ani ceny). Wiersz oferty bez ukrytego opisu zostaje jako zwykły tekst bez odnośnika, a odnośniki do usuniętych sekcji w tekście zamieniają się w zwykły tekst.
- Zmiana zmiennej **nie uruchamia** publikacji. Po zmianie uruchom ręcznie workflow: **Actions → Deploy to GitHub Pages → Run workflow**.
- Przełączane są tylko wiersze oferty, sekcje i menu (`scripts/build-site.py`). Wzmianki w zwykłym tekście (opis w lewej kolumnie, `<meta>`, sekcja „Tryb pracy”) pozostają bez zmian.
- Lokalnie (`index.html` otwarty wprost) widać wszystko. Podgląd z flagami: `SHOW_KONTRAKT=false python3 scripts/build-site.py index.html _site/index.html`.

## Podgląd lokalny

```bash
python3 -m http.server 8000
```

Następnie otwórz `http://localhost:8000`.

## Autor

Konrad Cinkusz · konradcinkusz@gmail.com

© 2026 Konrad Cinkusz
