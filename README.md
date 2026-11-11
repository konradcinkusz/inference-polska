# Inference Polska

Strona internetowa usługi **Inference Polska**: analiza wrażliwych dokumentów offline, na maszynie bez dostępu do sieci. Klient dostaje wydrukowany raport, a po wydruku wszystkie dane cyfrowe są usuwane. Rozmowa wstępna jest bezpłatna, a analiza dokumentów kosztuje 150 zł brutto za każde rozpoczęte 50 stron. Analizę dokumentów, prototypy i książki na zamówienie można zlecić także w trybie cloud; strona opisuje, jak ten tryb działa i na jakich warunkach przetwarzane są dane.

## Układ

Na komputerze strona ma stałą lewą kolumnę (nazwa, jedno zdanie opisu, menu, przycisk rozmowy wstępnej) i treść po prawej. Na telefonie kolumna staje się górnym paskiem z rozwijanym menu. Jeden krój pisma, cienkie linie zamiast kart, bez cieni i ikon. Jedyny efekt to podświetlenie wiersza na liście „Oferta”. Szczegóły (kroki, układ raportu, granice usługi, warunki trybu cloud, publikacje) są w zwijanych blokach; odnośnik do kotwicy wewnątrz zwiniętego bloku sam go otwiera.

## Sekcje strony

0. **Oferta** (`#oferta`): cztery usługi jako duża lista z ceną lub „wycena po rozmowie”.

1. **Analiza dokumentów offline** (`#analiza`): rozwiązanie i cena, a w zwijanych blokach problem (`#problem`), przebieg (`#jak`), wynik (`#raport`) i granice usługi (`#granice`).
2. **Przykładowe sprawy** (`#przyklady`): 16 fikcyjnych akt w czterech grupach, z linkami do PDF-ów w `assets/akta/`. Pliki są kopią wydania `pdfs` z repozytorium `iference-polska-use-cases`; po zmianie akt trzeba je skopiować ponownie.
3. **Prywatna sztuczna inteligencja w Twoim gabinecie** (`#firmy`): Pakiet Biuro, Pakiet Gabinet i Pakiet Pro, wycena na zapytanie.
4. **Prototyp w tydzień** (`#poc`).
5. **Książka na zamówienie** (`#ksiazka`).
6. **Tryb pracy** (`#tryb`): droższy *fully private* na modelach lokalnych i tańszy *cloud*, dla analizy dokumentów, prototypu i książki (nie dla wynajmu urządzenia w gabinecie). Blok „Jak dokładnie działa tryb cloud” (`#cloud`): kroki, warunki przetwarzania, porównanie z kontem indywidualnym, kiedy nie cloud.
7. **Kim jestem** (`#o-mnie`).
8. **Umów rozmowę wstępną** (`#rozmowa`): przycisk do rezerwacji w Kalendarzu Google i adres e-mail. Każdy przycisk „Umów rozmowę wstępną” na stronie prowadzi wprost do rezerwacji (nowa karta, ikona Kalendarza Google). Kliknięcie adresu e-mail nie otwiera programu pocztowego, tylko kopiuje adres do schowka i pokazuje duży napis.

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `index.html` | Cała strona: HTML, CSS i JavaScript w jednym pliku, bez zależności. |
| `.nojekyll` | Wyłącza przetwarzanie Jekyll na GitHub Pages. |
| `.github/workflows/deploy-pages.yml` | Akcja wdrażająca stronę na GitHub Pages. |
| `assets/` | Zdjęcie do sekcji „Kim jestem” oraz `akta/`: 16 fikcyjnych akt w PDF do sekcji „Przykładowe sprawy”. |
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
- `BOOKING_URL`: adres strony rezerwacji z Kalendarza Google (terminarz spotkań); używają go wszystkie przyciski „Umów rozmowę wstępną”.

## Podgląd lokalny

```bash
python3 -m http.server 8000
```

Następnie otwórz `http://localhost:8000`.

## Autor

Konrad Cinkusz · konradcinkusz@gmail.com

© 2026 Konrad Cinkusz
