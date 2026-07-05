# FinanceHub

FinanceHub — это веб-приложение для управления личными финансами, созданное на Django.

Проект позволяет пользователю вести учёт доходов и расходов, анализировать финансовую активность, устанавливать лимиты по категориям, создавать цели накоплений и получать умные финансовые инсайты на основе своих операций.

---

## Live Demo

https://finance-hub-00sk.onrender.com

---

## Основные возможности

- Регистрация и авторизация пользователей
- Персональный dashboard
- Добавление доходов и расходов
- Категории операций
- Финансовая статистика за месяц
- Графики доходов и расходов
- Диаграмма расходов по категориям
- Лимиты бюджета по категориям
- Цели накоплений
- Автоматическое удаление выполненных целей
- Модальное поздравление при достижении цели
- Финансовые инсайты
- Адаптивный современный интерфейс
- PostgreSQL база данных
- Docker-контейнеризация
- Деплой на Render

---

## Финансовые инсайты

На dashboard добавлен блок умной аналитики.

Приложение анализирует операции пользователя и показывает полезные подсказки:

- положительный или отрицательный баланс месяца;
- рост или снижение расходов по сравнению с прошлым месяцем;
- самую затратную категорию;
- превышенные лимиты;
- почти достигнутые цели накоплений.

Пример:

```text
Положительный баланс месяца
Доходы превышают расходы на 400.00 EUR.

Самая затратная категория
Жилье — 1000.00 EUR.

Лимит превышен
Транспорт: 600 / 500 EUR.
```

---

## Технологии

- Python
- Django
- PostgreSQL
- Django ORM
- Bootstrap 5
- Chart.js
- HTML / CSS
- Docker
- Gunicorn
- WhiteNoise
- Render

---

## Структура проекта

```text
FinanceHub/
│
├── apps/
│   ├── finance/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── users/
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       └── migrations/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── base.html
│   ├── finance/
│   └── users/
│
├── static/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## Установка и запуск локально

### 1. Клонировать репозиторий

```bash
git clone <your-repository-url>
cd FinanceHub
```

---

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

Активировать окружение:

```bash
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

---

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

### 4. Создать `.env` файл

В корне проекта создай файл `.env`:

```env
SECRET_KEY=your_secret_key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

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

```text
http://127.0.0.1:8000/
```

---

## Запуск через Docker

Проект можно запустить через Docker и PostgreSQL.

### 1. Собрать и запустить контейнеры

```bash
docker compose up --build
```

---

### 2. Применить миграции

Если миграции не применились автоматически:

```bash
docker compose exec web python manage.py migrate
```

---

### 3. Создать суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

---

### 4. Открыть сайт

```text
http://localhost:8000/
```

---

## Переменные окружения

### Для локального запуска

```env
SECRET_KEY=your_secret_key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

DB_NAME=financehub
DB_USER=financehub_user
DB_PASSWORD=financehub_password
DB_HOST=localhost
DB_PORT=5432
```

---

### Для Docker Compose

```env
SECRET_KEY=your_secret_key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

DB_NAME=financehub
DB_USER=financehub_user
DB_PASSWORD=financehub_password
DB_HOST=db
DB_PORT=5432
```

---

### Для Render

На Render нужно добавить переменные окружения:

```env
SECRET_KEY=your_secret_key
DEBUG=False

ALLOWED_HOSTS=finance-hub-00sk.onrender.com
CSRF_TRUSTED_ORIGINS=https://finance-hub-00sk.onrender.com

DATABASE_URL=your_render_postgresql_internal_database_url
```

Важно: секретные данные нельзя хранить в репозитории.

---

## Деплой

Проект задеплоен на Render с использованием Docker.

Для production используются:

- Docker
- Gunicorn
- PostgreSQL
- WhiteNoise
- Render Environment Variables

Команда запуска внутри Docker:

```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

---

## Основные модели

### Category

Категория операции.

Тип категории может быть:

- `INCOME` — доход
- `EXPENSE` — расход

---

### Transaction

Финансовая операция пользователя.

Содержит:

- пользователя;
- категорию;
- сумму;
- дату;
- описание.

---

### Budget

Лимит расходов по категории.

Позволяет отслеживать, превышен ли месячный бюджет.

---

### SavingsGoal

Цель накопления.

Содержит:

- название цели;
- целевую сумму;
- текущую сумму;
- дедлайн;
- процент выполнения.

---

## Dashboard

Dashboard показывает основную финансовую информацию пользователя:

- текущий баланс;
- доходы за месяц;
- расходы за месяц;
- средний чек;
- расходы по категориям;
- динамику доходов и расходов;
- лимиты;
- цели накоплений;
- финансовые инсайты.

---

## Безопасность

В проекте используются:

- CSRF-защита Django;
- авторизация пользователей;
- изоляция данных по пользователю;
- переменные окружения для секретов;
- `.env` не хранится в репозитории;
- production-настройки для Render.

---

## Полезные команды

### Создать миграции

```bash
python manage.py makemigrations
```

---

### Применить миграции

```bash
python manage.py migrate
```

---

### Создать администратора

```bash
python manage.py createsuperuser
```

---

### Собрать static files

```bash
python manage.py collectstatic --noinput
```

---

### Запуск локально

```bash
python manage.py runserver
```

---

### Запуск Docker

```bash
docker compose up --build
```

---

### Остановить Docker

```bash
docker compose down
```

---

### Полностью пересоздать базу Docker

```bash
docker compose down -v
docker compose up --build
```

---

## Планы по развитию

Возможные улучшения проекта:

- страница финансовых отчётов;
- экспорт операций в CSV / Excel;
- подтверждение email;
- восстановление пароля;
- повторяющиеся операции;
- импорт банковских операций;
- фильтры и поиск по операциям;
- улучшенная аналитика расходов.

---

## 🧑‍💻 Автор

Разработчик: **Vitalii Burdash**

Проект создан для практики Django, PostgreSQL, Docker, Render Deploy и разработки полноценного финансового веб-приложения.

---

## 📄 License

Этот проект создан в учебных целях и может быть использован как pet-project для портфолио.

---

## ⭐ FinanceHub

**FinanceHub** — управляй своими финансами умнее.