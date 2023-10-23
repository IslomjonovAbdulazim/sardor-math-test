from aiogram.dispatcher.filters.state import StatesGroup, State


class ConfirmState(StatesGroup):
    waiting = State()

