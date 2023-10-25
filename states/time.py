from aiogram.dispatcher.filters.state import StatesGroup, State


class TimeState(StatesGroup):
    waiting = State()

