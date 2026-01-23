from datetime import date, datetime
from typing import List, Any
from asgiref.sync import sync_to_async
from backend.models import  Task, TelegramUser
from datetime import date, timedelta

@sync_to_async
def create_task(user_id, title, due_date):
    user, _ = TelegramUser.objects.get_or_create(telegram_id=user_id)
    return Task.objects.create(user=user, title=title, due_date=due_date)

@sync_to_async
def get_today_tasks(user_id):
    return list(
        Task.objects.filter(
            user__telegram_id=user_id,
            done=False,
            due_date__lte=date.today()
        )
    )

@sync_to_async
def mark_task_done(task_id):
    task = Task.objects.get(id=task_id)
    task.done = True
    task.save()
    return task

@sync_to_async
def delay_task(task_id):
    task = Task.objects.get(id=task_id)
    task.due_date += timedelta(days=1)
    task.delay_count += 1
    task.save()
