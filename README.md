# epcandi

Django project for EPCandi.

## Prerequisites

- Python 3.14 (or your selected project Python)
- pip

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notes

- On Windows PowerShell, use `python manage.py makemigrations` (not `make migrations`).
- `db.sqlite3` is intentionally ignored in Git.
