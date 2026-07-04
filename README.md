# ◈ FinanceHub

**FinanceHub** — это современное веб-приложение для управления личными финансами, построенное на **Django**.  
Проект помогает контролировать доходы, расходы, лимиты бюджета и цели накоплений через удобный dashboard с аналитикой и графиками.

---

## 📌 О проекте


Приложение позволяет пользователю:

- отслеживать баланс;
- добавлять доходы и расходы;
- анализировать траты по категориям;
- контролировать месячные лимиты;
- создавать цели накоплений;
- видеть прогресс целей;
- получать поздравление при достижении цели;
- управлять операциями через личный кабинет.

---

## ✨ Основные возможности

### 📊 Dashboard

На главной панели отображается:

- общий баланс;
- доход за текущий месяц;
- расход за текущий месяц;
- средний чек;
- график расходов по категориям;
- динамика доходов и расходов по месяцам;
- лимиты бюджета;
- цели накоплений.

---

### 💸 Финансовые операции

Пользователь может:

- добавлять доходы;
- добавлять расходы;
- выбирать категории;
- указывать описание операции;
- фильтровать операции по типу и периоду;
- просматривать историю транзакций.

---

### 🎯 Цели накоплений

В FinanceHub можно создавать цели, например:

```txt
Dyson до 21.07.2026 — 100%
```

Когда цель достигает 100%, приложение автоматически удаляет её и показывает красивое поздравительное окно.

---

### 🧾 Лимиты бюджета

Пользователь может задавать лимиты по категориям:

```txt
Развлечения: 100 / 500
Жилье: 1000 / 1500
```

Если лимит превышен, прогресс-бар меняет цвет и визуально показывает проблему.

---

### 🔐 Авторизация

В проекте реализована система пользователей:

- регистрация;
- вход;
- выход;
- личный dashboard для каждого пользователя;
- защита данных пользователя.

---

## 🛠️ Технологии

### Backend

- Python
- Django 5
- Django ORM
- PostgreSQL
- Class-Based Views / Function-Based Views
- Django Templates

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js
- Glassmorphism UI
- Responsive Design

### DevOps

- Docker
- Docker Compose
- `.env` конфигурация
- PostgreSQL container

### Security / Utils

- `python-dotenv`
- `django-axes`
- `django-csp`
- `django-widget-tweaks`
- `psycopg`

---

## 📦 Requirements

```txt
Django>=5.0,<5.1
Pillow>=10.2.0
django-axes==6.3.0
django-csp==3.8
django-widget-tweaks==1.5.0
python-dotenv==1.2.2
psycopg[binary]>=3.1.8
```

---

## 📁 Структура проекта

```bash
FinanceHub/
│
├── apps/
│   ├── finance/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── users/
│       ├── migrations/
│       ├── templates/
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   └── landing.html
│
├── static/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Установка без Docker

### 1. Клонировать репозиторий

```bash
git clone https://github.com/YOUR_USERNAME/FinanceHub.git
cd FinanceHub
```

---

### 2. Создать виртуальное окружение

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

### 4. Создать `.env`

Создай файл `.env` в корне проекта:

```env
SECRET_KEY=your_secret_key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=financehub
DB_USER=financehub_user
DB_PASSWORD=financehub_password
DB_HOST=localhost
DB_PORT=5432
```

---

### 5. Применить миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

---

### 7. Запустить сервер

```bash
python manage.py runserver
```

Приложение будет доступно по адресу:

```txt
http://127.0.0.1:8000/
```

---

## 🐳 Запуск через Docker

Проект можно запустить полностью через Docker: Django + PostgreSQL.

### 1. Создать `.env`

Пример `.env` для Docker:

```env
SECRET_KEY=your_secret_key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=financehub
DB_USER=financehub_user
DB_PASSWORD=financehub_password
DB_HOST=db
DB_PORT=5432
```

Важно:

```env
DB_HOST=db
```

В Docker используется имя сервиса PostgreSQL из `docker-compose.yml`.

---

### 2. Запустить проект

```bash
docker compose up --build
```

После запуска приложение будет доступно:

```txt
http://127.0.0.1:8000/
```

---

### 3. Создать суперпользователя в Docker

В новом терминале:

```bash
docker compose exec web python manage.py createsuperuser
```

---

### 4. Остановить контейнеры

```bash
docker compose down
```

Если нужно удалить базу данных Docker:

```bash
docker compose down -v
```

---

## 🔐 Переменные окружения

В проекте используется `.env` файл.

Пример `.env.example`:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=financehub
DB_USER=financehub_user
DB_PASSWORD=change_me
DB_HOST=db
DB_PORT=5432
```

Файл `.env` нельзя добавлять в GitHub.

В `.gitignore` должно быть:

```gitignore
.env
.venv/
__pycache__/
*.pyc
db.sqlite3
.idea/
.vscode/
staticfiles/
media/
```

---

## 🐘 PostgreSQL

FinanceHub использует PostgreSQL в качестве основной базы данных.

Настройки подключения берутся из `.env`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}
```

---

## 📈 Dashboard

Пример данных на dashboard:

```txt
Баланс: 900 EUR

Доход за месяц:
+2000 EUR

Расход за месяц:
-1100 EUR

Средний чек:
550 EUR
```

Также dashboard показывает:

- траты текущего месяца;
- лимиты;
- цели накоплений;
- динамику по месяцам;
- визуальные графики через Chart.js.

---

## 🚀 Roadmap

Планируемые улучшения:

- [ ] REST API на Django REST Framework
- [ ] Экспорт операций в Excel
- [ ] Экспорт отчётов в PDF
- [ ] Email-подтверждение регистрации
- [ ] Telegram-уведомления
- [ ] AI-рекомендации по расходам
- [ ] Темная тема
- [ ] Мультивалютность

---

## 🧪 Полезные команды

### Django

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Docker

```bash
docker compose up --build
docker compose down
docker compose down -v
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py migrate
```

---

## 🧑‍💻 Автор

Разработчик: **Vitalii Burdash**

Проект создан для практики Django, PostgreSQL, Docker и разработки полноценного финансового веб-приложения.

---

## 📄 License

Этот проект создан в учебных целях и может быть использован как pet-project для портфолио.

---

## ⭐ FinanceHub

**FinanceHub** — управляй своими финансами умнее.