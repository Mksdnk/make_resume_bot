import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.cache import cache_service
from bot.tasks import generate_resume_task
from bot.states.resume_states import ResumeStates

router = Router()

@router.message(ResumeStates.FULL_NAME)
async def full_name_process(message: Message, state: FSMContext):
    user_id = message.from_user.id 
    await cache_service.save_user_data(user_id, {'full_name': message.text})
    await message.answer("Отлично! Теперь введите ваши контактные данные(номер телефона, электронная почта, через пробел)")
    await state.set_state(ResumeStates.CONTACTS)

@router.message(ResumeStates.CONTACTS)
async def contacts_process(message: Message, state: FSMContext):
    user_id = message.from_user.id 
    await cache_service.save_user_data(user_id, {'contacts': message.text})
    await message.answer("Хорошо! Теперь введите сведения о вашем обращовании(ВУЗ, специальность)")
    await state.set_state(ResumeStates.EDUCATION)

@router.message(ResumeStates.EDUCATION)
async def education_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'education': message.text})
    await message.answer("Ввведите опыт работы (места работы, должности, обязанности):")
    await state.set_state(ResumeStates.EXPERIENCE)

@router.message(ResumeStates.EXPERIENCE)
async def experience_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'experience': message.text})
    await message.answer("Введите навыки (профессиональные и soft skills):")
    await state.set_state(ResumeStates.SKILLS)

@router.message(ResumeStates.SKILLS)
async def skills_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'skills': message.text})
    await message.answer("Введите дополнительную информацию (курсы, сертификаты, хобби):")
    await state.set_state(ResumeStates.ADDITIONAL)

@router.message(ResumeStates.ADDITIONAL)
async def additional_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'additional': message.text})
    await message.answer("✅ Нейросеть уже генерирует ваше резюме")
    
    user_data = await cache_service.get_user_data(user_id)
    task = generate_resume_task.genrate_ai_task.delay(user_data)
    await cache_service.save_task_id(user_id, task.id)
    await state.set_state(ResumeStates.WAITING_GENERATION)








