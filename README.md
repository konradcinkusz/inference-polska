# Inference Polska

Strona internetowa usługi **Inference Polska**: analiza wrażliwych dokumentów offline, na maszynie bez dostępu do sieci. Klient dostaje wydrukowany raport, a po wydruku wszystkie dane cyfrowe są usuwane. Rozmowa wstępna jest bezpłatna, a analiza dokumentów kosztuje 150 zł brutto za każde rozpoczęte 50 stron.

## Sekcje strony

1. **Analiza dokumentów offline** (`#analiza`, `#rozwiazanie`, `#jak`, `#raport`): problem, rozwiązanie, przebieg, wynik i cena.
2. **Przykładowe sprawy** (`#przyklady`): 16 fikcyjnych akt w czterech grupach, z linkami do PDF-ów w `assets/akta/`. Pliki są kopią wydania `pdfs` z repozytorium `iference-polska-use-cases`; po zmianie akt trzeba je skopiować ponownie.
3. **Prywatna sztuczna inteligencja w Twoim gabinecie** (`#firmy`): Pakiet Biuro, Pakiet Gabinet i Pakiet Pro, wycena na zapytanie.
4. **POC w tydzień** (`#poc`).
5. **Książka na zamówienie** (`#ksiazka`).
6. **Tryb pracy** (`#tryb`): droższy *fully private* na modelach lokalnych i tańszy *cloud*, tylko dla POC i książek.
7. **Kim jestem** (`#o-mnie`).
8. **Umów rozmowę wstępną** (`#rozmowa`): kalendarz i formularz; przyciski z atrybutem `data-topic` ustawiają temat w formularzu.

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `index.html` | Cała strona: HTML, CSS i JavaScript w jednym pliku, bez zależności. |
| `.nojekyll` | Wyłącza przetwarzanie Jekyll na GitHub Pages. |
| `.github/workflows/deploy-pages.yml` | Akcja wdrażająca stronę na GitHub Pages. |
| `assets/` | Zdjęcie do sekcji „Kim jestem” oraz `akta/`: 16 fikcyjnych akt w PDF do sekcji „Przykładowe sprawy”. |
| `README.md` | Ten plik. |

Strona ma jasny i ciemny motyw: domyślnie zgodny z ustawieniem systemu, z przełącznikiem w nagłówku (wybór zapamiętywany w przeglądarce).

Strona jest statyczna: bez cookies, bez zewnętrznych skryptów i czcionek. Jedyne połączenie z zewnętrzną usługą to opcjonalne wysłanie formularza.

## Publikacja (GitHub Pages + GitHub Actions)

Workflow `.github/workflows/deploy-pages.yml` publikuje `index.html` przy każdym pushu do `main` (oraz ręcznie przez *Run workflow*).

Jednorazowo: **Settings → Pages → Build and deployment → Source → GitHub Actions**.

Strona będzie dostępna pod `https://konradcinkusz.github.io/inference-polska/`.

## Konfiguracja

Ustawienia są w obiekcie `CONFIG` na początku skryptu w `index.html`:

- `EMAIL`: adres kontaktowy,
- `FORM_ENDPOINT`: adres usługi formularza (np. Formspree). Puste: formularz otwiera program pocztowy (mailto),
- `START_DATE`, `MONTHS_AHEAD`, `WORKDAYS`, `SLOTS`, `BLOCKED_DATES`: kalendarz terminów rozmów wstępnych.

## Podgląd lokalny

```bash
python3 -m http.server 8000
```

Następnie otwórz `http://localhost:8000`.

## Autor

Konrad Cinkusz · konradcinkusz@gmail.com

© 2026 Konrad Cinkusz
