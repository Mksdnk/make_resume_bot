from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Text
from bot.states.resume_states import ResumeStates

router = Router()

@router.message(CommandStart())
async def greeting(message: Message):
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}! Этот бот предназначен для генерации резюме с помощью популярной нейросети Deepseek.\nДля начала работы пропишите комманду /resume.\n Доступные комманды можно посмотреть через комманду /help")

@router.message(Command("help"))
async def help(message: Message):
    await message.answer("/start - запуск бота \n/resume-начало генерации резюме\n/cancel-отмена")

@router.message(Command("resume"))
async def resume(message: Message, state: FSMContext):
    await message.answer("<b>Создание начато</b>, введите своё ФИО", parse_mode="HTML")
    await state.set_state(ResumeStates.FULL_NAME)

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    if (state.get_state() in [ResumeStates.WAITING_GENERATION, ResumeStates.WAITING_PDF, ResumeStates.REVIEW]):
        await message.answer("🛑 Действие отклонено, генерация уже идёт.")
    else:
        await message.answer("<b>Создание сброшено</b>. Для того, чтобы начать заново, введите комманду /resume", parse_mode="HTML")
        await state.clear()