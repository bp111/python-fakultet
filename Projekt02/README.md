# Aplikacja Webowa "Mutt Journal" napisana z frameworkiem Flask w języku Python

Aplikacja prezentuje wydawany w formie cyfrowej dziennik, dostępny do czytania dla każdego użytkownika strony, z częścią wydań oznaczonych jako eksluzywne, przez co są dostępne jedynie dla zalogowanych użytkowników.
Użytkownicy mogą przeglądać wydania oraz komentować pod nimi, edytować, usuwać własne komentarze.
Administrator może publikować (dodawać) nowe wydania.

### Set-up aplikacji z poziomu serwera (Windows):
Powershell (z poziomu rootu projektu):
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
flask --app mutt_journal init-db
flask --app mutt_journal populate-db
flask --app mutt_journal run --debug
```

### Zakres korzystania z pomocy samouczków i AI:
- samouczek: zbudowanie szkieletu projektu
- AI: pomoc w debugowaniu, CSS, fragmenty HTMLa + testy

### Bibliografia:
- samouczki, dokumentacja:
    - https://flask.palletsprojects.com/en/stable/tutorial/, 19.04.2026        
    - https://flask.palletsprojects.com/en/stable/#user-s-guide, 21.04.2026
- AI:
    - Google Gemini 3.1 Pro, 21.04.2026
- frameworki:
    - Flask 3.1.3
    - sqlite3