# Django Chat (Channels)

A simple room‑based chat application built with Django and Channels (ASGI). It demonstrates WebSocket messaging, persistence with Django ORM, and a modern Tailwind‑powered UI.

## Features
- Room list and room detail views
- Real‑time chat via WebSockets (Django Channels)
- Message persistence (SQLite by default)
- Authenticated chat (uses Django auth)
- Modern UI with dark mode

## Quick start

1) Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip setuptools wheel
pip install django==4.1.3 channels==3.0.4 daphne==3.0.2
```

2) Apply migrations and create a superuser:
```bash
python mysite/manage.py migrate
python mysite/manage.py createsuperuser
```

3) (Optional) Seed a room in the Django shell:
```bash
python mysite/manage.py shell -c "from chatapp.models import ChatRoom; ChatRoom.objects.get_or_create(name='General', slug='general')"
```

4) Run the development server:
```bash
python mysite/manage.py runserver
```
Open `http://127.0.0.1:8000/rooms/` in your browser.

## Configuration
Environment variables supported:
- `DJANGO_SECRET_KEY` – overrides default secret key
- `DJANGO_DEBUG` – set to `0` to disable debug
- `DJANGO_ALLOWED_HOSTS` – comma‑separated hostnames
- `REDIS_URL` – enables Redis channels layer (e.g. `redis://localhost:6379/0`)

## Production notes
- Use `REDIS_URL` for Channels in production
- Set `DJANGO_DEBUG=0` and configure `DJANGO_ALLOWED_HOSTS`
- Set `DJANGO_SECRET_KEY` to a strong secret
- Run with Daphne/Uvicorn or behind a reverse proxy

## Project structure
```
mysite/
  manage.py
  mysite/
    settings.py
    asgi.py
    urls.py
  chatapp/
    models.py
    views.py
    consumers.py
    routing.py
    services.py
    templates/
```

## Licence
MIT
