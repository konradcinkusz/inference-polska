# Inference Polska

Strona internetowa usługi **Inference Polska**: analiza dokumentów offline na lokalnym modelu językowym, na maszynie bez dostępu do sieci. Wynik trafia do klienta jako wydrukowany raport w formie książki, a po wydruku wszystkie dane cyfrowe są usuwane.

## Co jest w repozytorium

| Plik | Opis |
|---|---|
| `index.html` | Cała strona: HTML, CSS i JavaScript w jednym pliku, bez zależności. |
| `.nojekyll` | Wyłącza przetwarzanie Jekyll na GitHub Pages. |
| `README.md` | Ten plik. |

Strona jest statyczna: bez cookies, bez zewnętrznych skryptów i czcionek. Jedyne połączenie z zewnętrzną usługą to opcjonalne wysłanie formularza.

## Publikacja z brancha (GitHub Pages)

1. Wejdź w **Settings → Pages**.
2. W **Build and deployment → Source** wybierz **Deploy from a branch**.
3. Wybierz branch (np. `main`) i folder `/ (root)`, zapisz.
4. Strona będzie dostępna pod `https://konradcinkusz.github.io/inference-polska/`.

Każdy push do wybranego brancha publikuje nową wersję automatycznie.

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
