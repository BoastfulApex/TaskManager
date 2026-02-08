from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from datetime import datetime
from utils.db_api.database import create_task, get_today_tasks, mark_task_done, Task, TelegramUser
from keyboards.inline.tasks import task_keyboard, main_menu_keyboard, tasks_list_keyboard
from loader import dp, bot
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from datetime import datetime, date
from asgiref.sync import sync_to_async

from states.users import AddTaskState

router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Bu — shaxsiy task botingiz.\n"
        "Pastdagi menyudan foydalaning 👇",
        reply_markup=main_menu_keyboard()
    )
    
    
@router.message(F.text == "➕ Add task")
async def add_task(message: Message, state: FSMContext):
    await state.set_state(AddTaskState.waiting_for_date)
    await message.answer(
        "🗓 Task sanasini kiriting\n\n"
        "Format: YYYY-MM-DD\n"
        "Masalan: 2026-02-05",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(AddTaskState.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
    try:
        due_date = datetime.strptime(message.text, "%Y-%m-%d").date()

        if due_date < date.today():
            await message.answer("❌ Sana bugundan oldin bo‘lishi mumkin emas")
            return

        await state.update_data(due_date=due_date)
        await state.set_state(AddTaskState.waiting_for_title)

        await message.answer("📝 Task sarlavhasini kiriting (title):")

    except ValueError:
        await message.answer("❌ Sana noto‘g‘ri formatda. YYYY-MM-DD")


@router.message(AddTaskState.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTaskState.waiting_for_description)

    await message.answer(
        "📄 Task tavsifini kiriting (ixtiyoriy).\n"
        "Agar bo‘sh qoldirmoqchi bo‘lsangiz, `-` yuboring."
    )
    

@router.message(AddTaskState.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    data = await state.get_data()

    description = "" if message.text == "-" else message.text

    # 🔹 TelegramUser ni olish yoki yaratish
    telegram_user, _ = await sync_to_async(TelegramUser.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        }
    )

    # 🔹 Task yaratish
    await sync_to_async(Task.objects.create)(
        user=telegram_user,
        title=data["title"],
        description=description,
        due_date=data["due_date"]
    )

    await state.clear()

    await message.answer(
        "✅ Task muvaffaqiyatli saqlandi!",
        reply_markup=main_menu_keyboard()
    )
@router.message(F.text == "📋 My tasks")
async def my_tasks(message: Message):
    today = date.today()

    try:
        telegram_user = await sync_to_async(TelegramUser.objects.get)(telegram_id=message.from_user.id)
    except TelegramUser.DoesNotExist:
        await message.answer("📭 Sizda hali tasklar yo‘q")
        return

    tasks = await sync_to_async(list)(
        Task.objects.filter(user=telegram_user, due_date=today).order_by("done", "created_at")
    )

    if not tasks:
        await message.answer("📭 Bugun uchun tasklar yo‘q")
        return

    await message.answer(
        "📋 <b>Bugungi tasklaringiz:</b>\n\nTaskni tanlang 👇",
        reply_markup=tasks_list_keyboard(tasks),
        parse_mode="HTML"
    )
    

@router.callback_query(F.data.startswith("task:"))
async def select_task(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    task = await sync_to_async(Task.objects.get)(id=task_id)

    # Bugungi tasklar
    tasks = await sync_to_async(list)(
        Task.objects.filter(user=task.user, due_date=task.due_date).order_by("done", "created_at")
    )


    # Inline keyboard edit qiladi, pastga action buttons qo‘shiladi
    await callback.message.edit_reply_markup(
        reply_markup=tasks_list_keyboard(tasks, selected_task_id=task_id)
    )


@router.callback_query(F.data.startswith("done:"))
async def mark_done(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    task = await sync_to_async(Task.objects.get)(id=task_id)
    task.done = True
    await sync_to_async(task.save)()

    # Bugungi tasklar
    tasks = await sync_to_async(list)(
        Task.objects.filter(user=task.user, due_date=task.due_date).order_by("done", "created_at")
    )

    await callback.answer("✅ Task bajarildi", show_alert=True)

    # Inline keyboardni yangilash
    await callback.message.edit_reply_markup(reply_markup=tasks_list_keyboard(tasks))

@router.callback_query(F.data.startswith("delay:"))
async def delay_task(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    task = await sync_to_async(Task.objects.get)(id=task_id)
    task.delay_task()  # sizning model methodingiz
    await sync_to_async(task.save)()

    # Bugungi tasklar
    tasks = await sync_to_async(list)(
        Task.objects.filter(user=task.user, due_date=date.today()).order_by("done", "created_at")
    )

    await callback.answer("⏭ Task keyingi kunga qoldirildi", show_alert=True)

    # Inline keyboardni yangilash
    await callback.message.edit_reply_markup(reply_markup=tasks_list_keyboard(tasks))
