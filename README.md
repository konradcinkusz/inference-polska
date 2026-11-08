# Inference Polska

Strona internetowa usługi **Inference Polska**: analiza dokumentów offline na lokalnym modelu językowym, na maszynie bez dostępu do sieci. Wynik trafia do klienta jako wydrukowany raport w formie książki, a po wydruku wszystkie dane cyfrowe są usuwane.

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `index.html` | Cała strona: HTML, CSS i JavaScript w jednym pliku, bez zależności. |
| `.nojekyll` | Wyłącza przetwarzanie Jekyll na GitHub Pages. |
| `.github/workflows/deploy-pages.yml` | Akcja wdrażająca stronę na GitHub Pages. |
| `assets/` | Zdjęcie do sekcji „Kim jestem”. |
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
- `START_DATE`, `MONTHS_AHEAD`, `WORKDAYS`, `SLOTS`, `BLOCKED_DATES`: kalendarz terminów konsultacji.

## Podgląd lokalny

```bash
python3 -m http.server 8000
```

Następnie otwórz `http://localhost:8000`.

## Autor

Konrad Cinkusz · konradcinkusz@gmail.com

© 2026 Konrad Cinkusz
