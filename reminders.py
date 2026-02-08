import asyncio
from datetime import date
from asgiref.sync import sync_to_async
from loader import bot
from keyboards.inline.tasks import tasks_list_keyboard

async def send_hourly_task_reminders():
    from utils.db_api.database import Task, TelegramUser

    user_messages = {}  # user_id -> message_id (edit qilish uchun)

    while True:
        today = date.today()
        users = await sync_to_async(list)(TelegramUser.objects.all())
        print("Reminders tekshirilmoqda...")
        for user in users:
            # 🔹 Faqat bugungi tasklar
            tasks = await sync_to_async(list)(
                Task.objects.filter(user=user, due_date=today).order_by("done", "created_at")
            )

            if tasks:
                text = "⏰ <b>Bugungi tasklaringiz:</b>\n\nTaskni tanlang 👇"

                if user.telegram_id in user_messages:
                    # oldingi xabarni edit qilish
                    try:
                        await bot.edit_message_text(
                            chat_id=user.telegram_id,
                            message_id=user_messages[user.telegram_id],
                            text=text,
                            reply_markup=tasks_list_keyboard(tasks),
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        print(f"Edit xabar xato {user.telegram_id}: {e}")
                        # agar xato bo'lsa yangi xabar yuborish
                        msg = await bot.send_message(
                            chat_id=user.telegram_id,
                            text=text,
                            reply_markup=tasks_list_keyboard(tasks),
                            parse_mode="HTML"
                        )
                        user_messages[user.telegram_id] = msg.message_id
                else:
                    # yangi xabar
                    msg = await bot.send_message(
                        chat_id=user.telegram_id,
                        text=text,
                        reply_markup=tasks_list_keyboard(tasks),
                        parse_mode="HTML"
                    )
                    user_messages[user.telegram_id] = msg.message_id

        await asyncio.sleep(3600)  # 1 soat
