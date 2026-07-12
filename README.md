# FinanceHub

FinanceHub - веб-приложение для управления личными финансами на Django. Проект помогает вести учет доходов и расходов, анализировать финансовую активность, контролировать лимиты, отслеживать цели накоплений и получать персональные финансовые подсказки.

[Live demo](https://finance-hub-00sk.onrender.com)

## Что внутри

- регистрация, вход, выход и личный профиль пользователя;
- автоматическое создание базовых категорий при регистрации;
- пользовательские категории доходов и расходов;
- добавление, редактирование, удаление и фильтрация операций;
- дашборд с балансом, доходами, расходами, средним чеком и количеством операций;
- интерактивные графики Chart.js для расходов по категориям и динамики доходов/расходов;
- переключение периодов графиков: день, неделя, месяц, год;
- месячные лимиты расходов по категориям;
- цели накоплений с прогрессом и дедлайнами;
- автоматическое удаление выполненных целей и поздравительное модальное окно;
- финансовые инсайты на основе текущего и прошлого месяца;
- выбор основной валюты аккаунта: UAH, USD, EUR;
- пересчет операций, лимитов и целей при смене валюты;
- адаптивный интерфейс на Bootstrap 5 и собственном CSS;
- PostgreSQL, Docker, Gunicorn, WhiteNoise и деплой на Render.

## Последние изменения

После коммита `c8d6eec` проект заметно обновлен:

- стили вынесены из шаблонов в `static/css/style.css`;
- добавлен модуль `apps/finance/charts.py` для подготовки данных графиков;
- добавлен API `api/charts/data/` для динамического обновления Chart.js;
- добавлена страница создания пользовательских категорий;
- форма операции получила быстрый переход к созданию категории;
- профиль теперь умеет менять валюту и пересчитывать все суммы;
- добавлен модуль `apps/finance/currency.py` для работы с обменным курсом;
- подключен WhiteNoise storage для production-статики;
- обновлены шаблоны дашборда, операций, профиля, авторизации и landing page;

## Технологии

- Python 3.12
- Django 5.x
- PostgreSQL
- Django ORM
- Bootstrap 5
- Chart.js
- django-widget-tweaks
- django-axes
- django-csp
- WhiteNoise
- Gunicorn
- Docker и Docker Compose
- Render

## Структура проекта

```text
FinanceHub/
├── apps/
│   ├── finance/
│   │   ├── charts.py
│   │   ├── currency.py
│   │   ├── filters.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users/
│       ├── forms.py
│       ├── models.py
│       ├── signals.py
│       ├── urls.py
│       └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── finance/
│   ├── users/
│   ├── base.html
│   └── landing.html
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

`staticfiles/` - результат сборки статики командой `collectstatic`. Исходные стили проекта находятся в `static/`.

## Основные сущности

### User

Пользователь основан на `AbstractUser` и дополнен полями:

- `avatar`;
- `bio`;
- `currency`.

При создании нового пользователя сигнал `post_save` добавляет стартовые категории: зарплата, инвестиции, продукты, транспорт, жилье и развлечения.

### Category

Категория принадлежит конкретному пользователю и имеет тип:

- `INCOME` - доход;
- `EXPENSE` - расход.

Названия категорий уникальны в рамках пользователя и типа категории.

### Transaction

Финансовая операция пользователя: категория, сумма, дата и описание. Операции используются для расчета баланса, графиков, фильтров и инсайтов.

### Budget

Месячный лимит расходов по категории. Модель считает текущие траты за месяц и показывает, превышен ли лимит.

### SavingsGoal

Цель накопления с целевой суммой, текущим прогрессом и дедлайном. Прогресс считается в процентах и ограничивается 100%.

## Дашборд

Дашборд показывает:

- общий баланс;
- доход за текущий месяц;
- расход за текущий месяц;
- средний расход;
- последние операции;
- финансовые инсайты;
- лимиты бюджета;
- цели накоплений;
- расходы по категориям;
- динамику доходов и расходов.

Графики загружают данные через JSON API и позволяют отдельно выбирать период для диаграммы категорий и графика динамики.

## Финансовые инсайты

FinanceHub анализирует операции пользователя и показывает до пяти подсказок:

- положительный или отрицательный баланс месяца;
- рост или снижение расходов относительно прошлого месяца;
- самую затратную категорию;
- превышенные лимиты;
- цели, выполненные на 75% и больше.

Если данных пока мало, пользователь видит нейтральную подсказку с предложением добавить операции.

## Валюты

Пользователь может выбрать валюту аккаунта: `UAH`, `USD` или `EUR`.

При смене валюты приложение:

1. получает актуальный курс через `open.er-api.com`;
2. пересчитывает суммы операций;
3. пересчитывает лимиты бюджета;
4. пересчитывает цели накоплений;
5. сохраняет изменения в одной транзакции.

Для этой функции серверу нужен исходящий доступ в интернет.

## Локальный запуск

### 1. Создать и активировать окружение

```bash
python -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Подготовить `.env`

Пример для локальной PostgreSQL:

```env
SECRET_KEY=your_secret_key
DEBUG=True
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

DB_NAME=financehub
DB_USER=financehub_user
DB_PASSWORD=financehub_password
DB_HOST=localhost
DB_PORT=5432
```

Если используется `DATABASE_URL`, приложение возьмет подключение к базе из него:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 4. Применить миграции

```bash
python manage.py migrate
```

### 5. Создать администратора

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

Приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

## Запуск через Docker

```bash
docker compose up --build
```

Контейнер приложения будет доступен по адресу:

```text
http://localhost:8000/
```

Для Docker Compose значения подключения к базе в `.env` должны совпадать с настройками сервиса `db` в `docker-compose.yml`. Обычно `DB_HOST` должен быть равен `db`.

Полезные команды:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose down
docker compose down -v
```

## Production и Render

Проект подготовлен для деплоя через Docker.

В production используются:

- Gunicorn;
- PostgreSQL;
- WhiteNoise;
- переменные окружения Render;
- `DATABASE_URL` для подключения к базе;
- `collectstatic` для сборки статики.

Команда запуска внутри Dockerfile:

```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Пример production-переменных:

```env
SECRET_KEY=your_secret_key
DEBUG=False
CSRF_TRUSTED_ORIGINS=https://finance-hub-00sk.onrender.com
DATABASE_URL=your_render_postgresql_internal_database_url
```

`ALLOWED_HOSTS` сейчас задан в `config/settings.py`.

## Безопасность

В проекте используются:

- CSRF-защита Django;
- изоляция данных по пользователю;
- авторизация пользователей и ограничения доступа к личным данным;
- django-axes для ограничения неудачных попыток входа;
- Content Security Policy через django-csp;
- переменные окружения для секретов;
- WhiteNoise для безопасной раздачи static files в production.

## Полезные команды

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

## Возможные улучшения

- экспорт операций в CSV или Excel;
- импорт банковских операций;
- повторяющиеся операции;
- восстановление пароля;
- подтверждение email;
- отдельная страница отчетов;
- больше валют и история курсов;
- тесты для сервисов, форм, графиков и профиля.

## 🧑‍💻 Автор

Разработчик: **Vitalii Burdash**

Проект создан для практики Django, PostgreSQL, Docker, Render Deploy и разработки полноценного финансового веб-приложения.

---

## 📄 License

Этот проект создан в учебных целях и может быть использован как pet-project для портфолио.

---