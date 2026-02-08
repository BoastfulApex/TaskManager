from aiogram.fsm.state import State, StatesGroup

class AddTaskState(StatesGroup):
    waiting_for_date = State()
    waiting_for_title = State()
    waiting_for_description = State()