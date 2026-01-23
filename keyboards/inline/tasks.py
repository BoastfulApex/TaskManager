from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def task_keyboard(task_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bajarildi",
                    callback_data=f"task_done:{task_id}"
                )
            ]
        ]
    )
