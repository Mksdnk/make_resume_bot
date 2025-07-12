from aiogram.fsm.state import StatesGroup, State

class ResumeStates(StatesGroup):
    FULL_NAME = State()
    AGE = State()
    CONTACTS = State()
    PLACE_OF_RESIDENCE = State()
    CITIZENSHIP = State()
    REMOVAL = State()
    DESIRED_POSITION = State()
    EXPERIENCE = State()
    EDUCATION = State()
    SKILLS = State()
    DRIVING_EXP = State()
    ADDITIONAL = State()
    WAITING_GENERATION = State()
    REVIEW = State()
    WAITING_PDF = State()
