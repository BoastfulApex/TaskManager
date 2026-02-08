from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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



def task_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add task")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add task")],
            [KeyboardButton(text="📋 My tasks")]
        ],
        resize_keyboard=True
    )
    

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def tasks_list_keyboard(tasks, selected_task_id=None):
    """
    Tasks ro'yxati inline keyboardda.
    Agar selected_task_id berilsa, shu task ostida action buttons qo'shiladi.
    """
    keyboard = []

    for task in tasks:
        status = "✅" if task.done else "❌"
        text = f"{status} {task.title}"
        if task.id == selected_task_id:
            text = f"👉 {text}"

        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"task:{task.id}")])

        # Tanlangan task ostiga action buttons
        if task.id == selected_task_id:
            keyboard.append([
                InlineKeyboardButton(text="✅ Bajarildi", callback_data=f"done:{task.id}"),
                InlineKeyboardButton(text="⏭ Keyinga qoldirish", callback_data=f"delay:{task.id}")
            ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
