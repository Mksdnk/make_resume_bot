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
    await message.answer("Отлично! Теперь введите ваш возраст")
    await state.set_state(ResumeStates.AGE)

@router.message(ResumeStates.AGE)
async def age_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'age': message.text})
    await message.answer("📱 Введите ваши контактные данные (номер телефона, электронная почта и т.д)")
    await state.set_state(ResumeStates.CONTACTS)

@router.message(ResumeStates.CONTACTS)
async def contacts_process(message: Message, state: FSMContext):
    user_id = message.from_user.id 
    await cache_service.save_user_data(user_id, {'contacts': message.text})
    await message.answer("🌆 Введите ваше место проживания")
    await state.set_state(ResumeStates.PLACE_OF_RESIDENCE)

@router.message(ResumeStates.PLACE_OF_RESIDENCE)
async def place_of_residence_process(message: Message, state: FSMContext):
    user_id = message.from_user.id 
    await cache_service.save_user_data(user_id, {'place_of_residence': message.text})
    await message.answer("🪪 Введите какое у вас гражданство")
    await state.set_state(ResumeStates.CITIZENSHIP)

@router.message(ResumeStates.CITIZENSHIP)
async def citienship_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'citizenship': message.text})
    await message.answer("💼 Готовы ли вы к переезду или коммандировкам?")
    await state.set_state(ResumeStates.REMOVAL)

@router.message(ResumeStates.REMOVAL)
async def removal_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'removal': message.text})
    await message.answer("📑 Введите должность, на которую претендуете, вашу специализацию. Занятость, график работы")
    await state.set_state(ResumeStates.DESIRED_POSITION)

@router.message(ResumeStates.DESIRED_POSITION)
async def desired_position_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'desired_position': message.text})
    await message.answer("👨🏻‍💻 Ввведите опыт работы (места работы, должности, обязанности):")
    await state.set_state(ResumeStates.EXPERIENCE)

@router.message(ResumeStates.EXPERIENCE)
async def experience_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'experience': message.text})
    await message.answer("🎓 Введите ваше образование")
    await state.set_state(ResumeStates.EDUCATION)

@router.message(ResumeStates.EDUCATION)
async def education_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'education': message.text})
    await message.answer("🛠️ Введите ваши навыки(профессиональные и soft skills)")
    await state.set_state(ResumeStates.SKILLS)

@router.message(ResumeStates.SKILLS)
async def skills_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'skills': message.text})
    await message.answer("🚗 Введите ваш опыт вождения")
    await state.set_state(ResumeStates.DRIVING_EXP)

@router.message(ResumeStates.DRIVING_EXP)
async def skills_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await cache_service.save_user_data(user_id, {'driving_exp': message.text})
    await message.answer("Введите дополнительную информацию (например хобби)")
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








