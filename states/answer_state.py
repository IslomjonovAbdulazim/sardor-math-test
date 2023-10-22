from aiogram.dispatcher.filters.state import StatesGroup, State


class AnswersState(StatesGroup):
    waiting = State()

