import asyncio
from utils.db_api.database import get_today_tasks
from keyboards.inline.tasks import task_keyboard

async def task_scheduler(bot):
    while True:
        # bu yerda userlarni aylantirasiz (adminlar yoki barcha userlar)
        for user_id in await get_all_user_ids():
            tasks = await get_today_tasks(user_id)
            for task in tasks:
                await bot.send_message(
                    chat_id=user_id,
                    text=f"📝 Vazifa:\n{task.title}",
                    reply_markup=task_keyboard(task.id)
                )
        await asyncio.sleep(60 * 60 * 2)  # 2 soat
