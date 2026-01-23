from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from datetime import datetime
from utils.db_api.database import create_task, get_today_tasks, mark_task_done
from keyboards.inline.tasks import task_keyboard
from loader import dp, bot


router = Router()
dp.include_router(router)


@router.message(F.text.startswith("task "))
async def add_task_handler(message: Message):
    """
    Format:
    task 2026-01-25 Excel o'rganish
    """
    try:
        _, date_str, title = message.text.split(" ", 2)
        due_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        await create_task(message.from_user.id, title, due_date)
        await message.answer("✅ Task qo‘shildi")
    except:
        await message.answer("❌ Format: task YYYY-MM-DD Matn")

@router.callback_query(F.data.startswith("task_done:"))
async def task_done_handler(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    task = await mark_task_done(task_id)

    await callback.message.edit_text(
        f"✅ <s>{task.title}</s>",
        parse_mode="HTML"
    )
    await callback.answer("Bajarildi!")
