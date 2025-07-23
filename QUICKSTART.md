# TRON Wallet Service - Quick Start

## What's been created

✅ **Микросервис TRON Wallet Service** с полной функциональностью:

### 🎯 Основные возможности:
- **POST /api/v1/wallet/info** - получение информации о TRON кошельке (баланс, bandwidth, energy)
- **GET /api/v1/wallet/requests** - получение истории запросов с пагинацией
- Автоматическое сохранение всех запросов в SQLite базу данных

### 🏗️ Архитектура:
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **Pydantic v2** - валидация и сериализация данных
- **TronPy** - интеграция с блокчейном TRON
- **Clean Architecture** - разделение на слои (API, Service, Database)
- **SOLID принципы** и **DRY**
- **Dependency Injection**

### 🧪 Тестирование:
- **Unit тесты** - тестирование бизнес-логики и работы с БД
- **Integration тесты** - тестирование API endpoints
- **Pytest** с поддержкой async/await
- Покрытие тестами всех основных сценариев

### 🐳 DevOps:
- **Docker** и **Docker Compose** для контейнеризации
- **Makefile** для автоматизации задач
- **Git** с историей коммитов
- Правильные **.gitignore** и **.dockerignore**

## 🚀 Быстрый запуск

### Вариант 1: Локальная разработка
```bash
# 1. Установить зависимости
make install

# 2. Инициализировать базу данных
make init-db

# 3. Запустить сервер
make run
```

### Вариант 2: Docker
```bash
# 1. Собрать и запустить через Docker Compose
make docker-build
make docker-run

# 2. Посмотреть логи
make docker-logs
```

## 📋 Тестирование

```bash
# Запустить все тесты
make test

# Тесты с покрытием
make test-coverage

# Только unit тесты
pytest tests/unit/

# Только integration тесты
pytest tests/integration/
```

## 📖 API Documentation

После запуска сервиса:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Полезные команды

```bash
# Показать все доступные команды
make help

# Форматирование кода
make format

# Линтинг
make lint

# Очистка кэша
make clean

# Остановить Docker контейнеры
make docker-stop
```

## 📁 Структура проекта

```
tron-wallet-service/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Конфигурация и исключения
│   ├── db/             # База данных
│   ├── models/         # SQLAlchemy модели
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # Бизнес-логика
│   └── main.py         # FastAPI приложение
├── tests/
│   ├── unit/           # Unit тесты
│   └── integration/    # Integration тесты
├── data/               # База данных SQLite
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── requirements.txt
```

## 🎉 Готово!

Проект полностью готов к использованию и соответствует всем требованиям:
- ✅ Современные версии Pydantic v2 и SQLAlchemy v2
- ✅ Следование принципам SOLID и DRY
- ✅ Dependency Injection и Clean Architecture
- ✅ Полное покрытие тестами
- ✅ Docker и автоматизация
- ✅ Документация и README
