# Aplikacja Webowa "Mood Journal" napisana z frameworkiem Django w języku Python

Aplikacja oferuje każdemu klientowi/użytkownikowi końcowemu prosty interfejs do tworzenia 
wpisów zamieszczanych w swoim własnym dzienniku; wpisy składają się z daty, treści, oceny nastroju, oraz ewentualnych dodatkowych tagów. Użytkownik może również edytować, usunąć wpis lub dodać do niego notkę zwaną refleksją, pozwalającą skomentować wpis z perspektywy czasu.

Zarządzanie aplikacją odbywa się z poziomu serwera za pośrednictwem skryptu manage.py. Z poziomu klienta za pomocą podstrony panelu administratora. Administrator ma pełny dostęp
do zawartości bazy danych.

### Set-up aplikacji z poziomu serwera (Windows):
utwórz venv na poziomie roota projektu, aktywuj je:
``` 
py -m venv .venv 
Set-ExecutionPolicy Unrestricted -Scope Process
.venv/Scripts/Activate.ps1
```
zainstaluj zawartość requirements.txt:
```
pip install -r requirements.txt
```
nastepnie zainicjalizuj baze danych:
```
python manage.py makemigrations
python manage.py migrate
```
utworz konto admina (daje dostep do panelu admina w przegladarce):
```
python manage.py createsuperuser
```
gotowe, teraz mozna juz uruchamiac serwer:
```
python manage.py runserver
```

### Dodatkowe przydatne polecenia:
runuje wszystkie testy
```
py manage.py test
```
dodatkowe komendy manage.py, opisane w odpowiadajacych im plikach w /webapp/entries/management/commands/
```
py manage.py populate_db
py manage.py view_db
py manage.py erase_all_entries
```

### Zakres korzystania z pomocy samouczków i AI:
- samouczek: zbudowanie prototypu projektu
- AI: pomoc w debugowaniu, wygenerowanie testow, CSS i fragmentow HTMLa

### Bibliografia:
- samouczki, dokumentacja:
    - https://www.youtube.com/watch?v=H2EJuAcrZYU, 21.03.2026
    - https://www.youtube.com/watch?v=Rp5vd34d-z4, 22.03.2026
    - https://docs.djangoproject.com/en/6.0/, 24.03.2026
    - https://docs.python.org/3/, 24.03.2026
- AI:
    - Google Gemini 3.1 Pro, 24.03.2026
- frameworki:
    - Django 6.0.3