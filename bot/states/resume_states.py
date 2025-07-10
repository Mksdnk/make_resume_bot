from aiogram.fsm.state import StatesGroup, State

class ResumeStates(StatesGroup):
    FULL_NAME = State()
    CONTACTS = State()
    EDUCATION = State()
    EXPERIENCE = State()
    SKILLS = State()
    ADDITIONAL = State()
    WAITING_GENERATION = State()
    REVIEW = State()
    WAITING_PDF = State()
