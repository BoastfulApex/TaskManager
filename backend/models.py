from django.db import models
from django.utils import timezone

from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or str(self.telegram_id)


from django.db import models
from django.utils import timezone
from datetime import timedelta

class Task(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()  # faqat sana
    done = models.BooleanField(default=False)
    delay_count = models.PositiveIntegerField(default=0)  # necha marta kechiktirilgan

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "✅" if self.done else "❌"
        return f"{self.title} {status}"

    # 🔹 Taskni kechiktirish funksiyasi
    def delay_task(self):
        if not self.done:
            self.due_date += timedelta(days=1)
            self.delay_count += 1
            self.save()
