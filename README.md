# 📋 Task Tracker + Telegram Bot

Проект "Task Tracker" — это веб-приложение на Django с REST API для управления задачами и Telegram-ботом для уведомлений о дедлайнах.

---

## 🚀 Возможности

### Веб-приложение (Django):
- Создание, просмотр и редактирование задач
- API для получения задач
- Фильтрация задач по Telegram ID
- Обновление статуса задач

### Telegram-бот (Aiogram):
- `/start` — стартовое приветствие и помощь
- `/mytasks` — список задач пользователя
- `/done <task_id>` — отметить задачу как выполненную
- `/getid` — узнать свой Telegram ID
- Автоматическое уведомление за 10 минут до дедлайна

---

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Myalkool/Task_tracker.git
cd Task_tracker
```

### 2. Создать файл .env (рядом с docker-compose.yml):

```dotenv
BOT_TOKEN=ваш_токен_бота
```

### 3. Запустить все сервисы

```bash
docker compose down
docker compose up -d --build
```
