import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from bot.services.cache import cache_service
from bot.tasks import generate_resume_task
from bot.states.resume_states import ResumeStates
from celery.result import AsyncResult

router = Router()

@router.message(ResumeStates.WAITING_GENERATION)
async def generation_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    task_id = await cache_service.get_task_id(user_id)

    task: AsyncResult = AsyncResult(task_id)

    if (task.status == "PENDING"):
        await message.answer('▶️ Генерация идёт, пожалуйста подождите')
    if (task.status == "SUCCESS"):
        resume_text = task.result
        await cache_service.save_user_data(user_id, {'resume': resume_text})

        preview = resume_text[:1500] + "..." if len(resume_text) > 1500 else resume_text
        await message.answer(f'✅Ваше резюме готово! Прдедпросмотр:\n{preview}\n Если все верно, то напишете "да", иначе в следующем сообщении отредактируйте резюме, внимание, сохраняйте разметку markdown для корректной генерации pdf с правильными заголовками')
        await state.set_state(ResumeStates.REVIEW)
    else:
        await message.answer(f'⛔️ Ошибка генерации {task.status}')
        state.clear()

@router.message(ResumeStates.REVIEW)
async def review_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await cache_service.get_user_data(user_id)
    resume_text: str
    if (message.text.lower() == 'да'):
        resume_text = user_data.get('resume', '')

    else:
        resume_text=message.text
        await cache_service.save_user_data(user_id, {'resume': resume_text})

    task = generate_resume_task.generate_pdf_task.delay(resume_text)
    await cache_service.save_task_id(user_id, task.id)

    await state.set_state(ResumeStates.WAITING_PDF)
    await message.answer('📝 Приступаю к генерации PDF')
    
@router.message(ResumeStates.WAITING_PDF)
async def pdf_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    task_id = await cache_service.get_task_id(user_id)
    task: AsyncResult = AsyncResult(task_id)

    if(task.status == "PENDING"):
        await message.answer("🔄 PDF все еще создается, пожалуйста, подождите...")
    elif(task.status == "SUCCESS"):
        await message.answer_document(BufferedInputFile(file=task.result, filename='resume.pdf'), caption="✅ Ваше резюме готово!")
        await state.clear()
    else:
        await message.answer(f"❌ Ошибка создания PDF: {task.status}")
        await state.clear()
    


    

    