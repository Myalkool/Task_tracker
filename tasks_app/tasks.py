import os
import logging
import requests
from celery import shared_task
from django.utils import timezone
from .models import Task

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8066710790:AAH3uQ3t0qG3G1X3Agce0i_ZOwLtYi9XM5M")


@shared_task
def notify_upcoming():
    now = timezone.now()
    soon = now + timezone.timedelta(minutes=10)

    tasks_to_notify = Task.objects.filter(
        status='undone',
        notified=False,
        deadline__range=(now, soon)
    )

    for task in tasks_to_notify:
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                params={
                    "chat_id": task.telegram_user_id,
                    "text": (
                        f"⏰ Задача «{task.title}» должна быть выполнена до "
                        f"{task.deadline.strftime('%Y-%m-%d %H:%M')}."
                    )
                },
                timeout=5,
            )

            if response.ok:
                task.notified = True
                task.save()
                logger.info("Уведомление отправлено для задачи %s", task.id)
            else:
                logger.error(
                    "Ошибка отправки уведомления для задачи %s: [%s] %s",
                    task.id, response.status_code, response.text
                )

        except requests.RequestException as e:
            logger.exception("Сетевая ошибка при отправке уведомления для задачи %s: %s", task.id, e)
