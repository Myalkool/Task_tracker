import asyncio
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Ошибка: не найден BOT_TOKEN в .env или dotenv.env")


API_URL = os.getenv("API_URL", "http://localhost:8000/tasks/")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я помогу тебе следить за задачами.\n\n"
        "Доступные команды:\n"
        "/mytasks — получить список твоих задач\n"
        "/done <task_id> — пометить задачу как выполненную\n"
        "/getid — получить свой ID\n"
    )


@dp.message(Command("mytasks"))
async def cmd_mytasks(message: Message):
    user_id = message.from_user.id
    print(f"DEBUG: /mytasks от пользователя {user_id}")
    try:
        resp = requests.get(API_URL, params={"telegram_user_id": user_id}, timeout=10)
        print("DEBUG: Запрос к API:", resp.url, "Status code:", resp.status_code)
        resp.raise_for_status()
    except requests.RequestException as e:
        print("DEBUG: Ошибка при запросе к API:", e)
        return await message.answer("❌ Не удалось получить список задач. Попробуйте позже.")
    tasks = resp.json()
    print("DEBUG: Получены задачи:", tasks)
    if not tasks:
        return await message.answer("У тебя нет активных задач.")
    lines = [f"{t['id']}: {t['title']} ({t['status']})" for t in tasks]
    text = "Твои задачи:\n" + "\n".join(lines)
    await message.answer(text)


@dp.message(Command("done"))
async def cmd_done(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("Используй: /done <task_id>")

    task_id = parts[1]
    url = f"{API_URL}{task_id}/"
    try:
        r = requests.patch(url, json={"status": "done"}, timeout=10)
    except requests.RequestException:
        return await message.answer("❌ Не удалось обновить задачу. Попробуйте позже.")

    if r.status_code == 200:
        await message.answer(f"✅ Задача {task_id} помечена как выполненной.")
    elif r.status_code == 404:
        await message.answer("❌ Задача с таким ID не найдена.")
    else:
        await message.answer("❌ Не удалось обновить задачу.")


@dp.message(Command("getid"))
async def cmd_getid(message: Message):
    """
    Эта команда просто отвечает: "Ваш Telegram ID: <число>"
    """
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")


async def check_deadlines():
    print("Фоновая проверка дедлайнов запущена...")
    while True:
        try:
            resp = requests.get(API_URL, timeout=10)
            resp.raise_for_status()
            tasks = resp.json()
            now = datetime.now(timezone.utc)

            for task in tasks:
                deadline_str = task.get("deadline")
                if not deadline_str or not task.get("telegram_user_id"):
                    continue

                try:
                    deadline = datetime.fromisoformat(deadline_str)
                except ValueError:
                    continue

                seconds_left = (deadline - now).total_seconds()
                if 0 < seconds_left <= 600 and not task.get("notified", False):
                    text = f"⏰ Напоминание! Через 10 минут дедлайн по задаче: «{task['title']}»"
                    await bot.send_message(chat_id=task['telegram_user_id'], text=text)


                    try:
                        notify_url = f"{API_URL}{task['id']}/"
                        requests.patch(notify_url, json={"notified": True}, timeout=5)
                    except requests.RequestException as e:
                        print("Не удалось отметить задачу как notified:", e)

        except requests.RequestException as e:
            print("Ошибка при запросе к API:", e)

        await asyncio.sleep(60)


if __name__ == "__main__":
    async def main():
        asyncio.create_task(check_deadlines())
        await dp.start_polling(bot, skip_updates=True)

    asyncio.run(main())

