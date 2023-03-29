from aiogram.fsm.state import State, StatesGroup


class BotStatesGroup(StatesGroup):
    main = State()
    message = State()
    recipient = State()
