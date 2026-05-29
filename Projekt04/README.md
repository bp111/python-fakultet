# Strona internetowa do monitorowania postępu skryptów z Projektu03

## Streszczenie 
Projekt składa się z:
- kodu aplikacji webowej napisanej przy użyciu frameworka Flask, stanowiącej interfejs do monitorowania działania skryptów z Projektu03 w czasie bieżącym
- dostosowanych pod to rozwiązanie zmodyfikowanych wersji skryptów.

## Struktura, najważniejsze użyte mechanizmy

- pliki składowe pipeline'u ML (main.py, evaluate.py) używają *yield* zamiast *print* do zwracania wiadomości
- route /run przyjmuje te wiadomości, wrapuje w JSON, przesyła do frontendu przy pomocy *Response(..., mimetype='text/event-stream')*

- evaluate.py używa *matplotlib.use('Agg')* - renderowanie obrazków w tle, zamiast pop-upów na serwerze (zapisywane w static/images/ jako .png)
- *yield* zwraca dla obrazków *IMAGE:/static/images/nazwa_pliku.png*, app.py obrabia ten ciąg i przesyła do frontendu jako obiekt JSON { "image": path }

- index.html używa JS-owego *new EventSource('/run')*, tworząc stałe połączenie z serwerem. Gdy ML-owy pipeline zwraca tekst za pomocą *yield*, frontend przechwytuje go używając eventu *onmessage*

## Set-up (Windows)
1. Sklonuj repozytorium.
2. Utwórz wirtualne środowisko: `python -m venv .venv`
3. Aktywuj środowisko:
   - `Set-ExecutionPolicy Unrestricted -Scope Process`, potem `.venv/Scripts/Activate.ps1`
4. Zainstaluj zależności: `pip install -r requirements.txt`
5. Uruchom projekt: `py app.py`

## Zakres korzystania z pomocy samouczków i AI:
- AI: pomoc przy zbudowaniu kodu HTML i CSS, pomoc w debugowaniu

## Bibliografia:
- samouczki, dokumentacja:
    - https://flask.palletsprojects.com/en/stable/#user-s-guide, 29.05.2026
    - https://docs.python.org/3/, 29.05.2026
    - https://developer.mozilla.org/en-US/docs/Web, 29.05.2026
       
- AI:
    - Google Gemini 3.1 Pro, 29.05.2026