# DJHotel

## ✨ Описание
DJHotel — backend-сервис для бронирования номеров в отеле.

Проект позволяет:
- создавать комнаты;
- получать список комнат с сортировкой;
- удалять комнаты;
- создавать брони;
- получать список броней конкретной комнаты;
- удалять брони;
- валидировать даты бронирования;
- запрещать пересечение броней для одной комнаты;
- просматривать логи приложения через Grafana + Loki.

## 🗃️ Модели БД
В проекте используются 2 основные модели: `Room` и `Booking`.

### Room
Модель комнаты.

Поля:
- `id` — первичный ключ комнаты
- `type` — тип комнаты
- `description` — описание комнаты
- `price` — цена комнаты
- `created_at` — дата и время создания записи
- `updated_at` — дата и время последнего обновления записи

Допустимые значения поля `type`:
- `S` — стандартный номер
- `B` — BDSM-комната с приколами
- `V` — VIP-комната

### Booking
Модель бронирования комнаты.

Поля:
- `id` — первичный ключ брони
- `room_id` — ссылка на комнату (`ForeignKey` на `Room`)
- `start_date` — дата заезда
- `end_date` — дата выезда
- `created_at` — дата и время создания записи
- `updated_at` — дата и время последнего обновления записи

Ограничения:
- `start_date` должна быть раньше `end_date`
- нельзя создать пересекающиеся брони для одной и той же комнаты
- при удалении комнаты удаляются все связанные с ней брони

## 🚀 Быстрый старт
1. Склонировать проект и перейти в корень репозитория.
2. Создать `.env` на основе `.env-example`.
3. Запустить проект:

```bash
docker compose up --build
```

После запуска будут доступны:
- API: `http://localhost:8000`
- Grafana: `http://localhost:3000`

## ⚙️ Переменные окружения
Пример `.env`:

```env
DB_NAME=djhotel
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
TEST_DB_NAME=test_djhotel
SECRET_KEY=your_secret_key
DEBUG=False
APP_ENV=prod
LOG_LEVEL=INFO
```

Описание переменных:
- `DB_NAME` — имя основной базы данных PostgreSQL
- `DB_USER` — пользователь PostgreSQL
- `DB_PASSWORD` — пароль PostgreSQL
- `DB_HOST` — хост базы данных
- `DB_PORT` — порт базы данных
- `TEST_DB_NAME` — имя тестовой базы данных
- `SECRET_KEY` — секретный ключ Django
- `DEBUG` — режим отладки Django
- `APP_ENV` — режим логирования (`dev` / `prod`)
- `LOG_LEVEL` — уровень логирования

## 🔧 Установка
Запуск проекта выполняется через Docker Compose:

```bash
docker compose up --build
```

Миграции применяются автоматически при старте контейнера `web`.

Полезные команды:

```bash
docker compose down
docker compose ps
docker compose logs -f web
```

## 🧪 Тесты
Запуск тестов внутри контейнера:

```bash
docker compose exec web uv run python manage.py test
```

В проекте покрыты тестами:
- создание комнат;
- получение списка комнат;
- сортировка комнат;
- удаление комнат;
- каскадное удаление броней при удалении комнаты;
- создание броней;
- получение списка броней по `room_id`;
- сортировка броней;
- удаление броней;
- валидация диапазона дат;
- запрет пересечения броней.

## 🥞 Стек технологий
- Python 3.13
- Django 6
- Django REST Framework
- PostgreSQL 17
- Docker / Docker Compose
- Loguru
- Grafana
- Loki
- Promtail
- Ruff
- Mypy
- Bandit
- Radon

## 🔌 API
Базовый URL локального API:

```text
http://localhost:8000
```

### Комнаты

#### Создать комнату
```http
POST /api/v1/rooms/
```

Пример тела запроса:

```json
{
  "type": "B",
  "description": "Room with jacuzzi",
  "price": 69600
}
```

Пример ответа:

```json
{
  "room_id": 1
}
```

#### Получить список комнат
```http
GET /api/v1/rooms/
```

Сортировка:

```http
GET /api/v1/rooms/?ordering=price
GET /api/v1/rooms/?ordering=-price
GET /api/v1/rooms/?ordering=created_at
GET /api/v1/rooms/?ordering=-created_at
```

#### Удалить комнату
```http
DELETE /api/v1/rooms/<room_id>
```

### Брони

#### Создать бронь
```http
POST /api/v1/bookings/
```

Пример тела запроса:

```json
{
  "room_id": 1,
  "start_date": "2026-05-10",
  "end_date": "2026-05-12"
}
```

Пример ответа:

```json
{
  "booking_id": 1
}
```

#### Получить список броней комнаты
```http
GET /api/v1/bookings/list?room_id=1
```

Сортировка:

```http
GET /api/v1/bookings/list?room_id=1&ordering=start_date
GET /api/v1/bookings/list?room_id=1&ordering=-start_date
```

#### Удалить бронь
```http
DELETE /api/v1/bookings/<booking_id>
```

### Логирование
Приложение пишет логи в `stdout`, а контейнерные логи собираются через Promtail, Loki и Grafana.

Grafana доступна по адресу:

```text
http://localhost:3000
```

Стандартный вход:
- login: `admin`
- password: `admin`

Примеры запросов в Grafana Explore:

```text
{compose_service="web"}
{compose_service="web"} |= "Room created"
{compose_service="web"} |= "Booking created"
{compose_service="web"} |= "Room deleted"
{compose_service="web"} |= "Booking deleted"
```
