from celery import Celery
from bot.config_reader import config
from bot.services.deepseek import deepseek_service
from bot.services.pdf import pdf_service


broker_url = config.CLERY_BROKER_URL.unicode_string()
backend_url = config.CLERY_RESULT_BACKEND.unicode_string()

celery = Celery('resume_task', broker=broker_url, backend=backend_url)

@celery.task
def genrate_ai_task(data: dict):
    return deepseek_service.generate_resume(data)

@celery.task
def generate_pdf_task(data: str):
    return pdf_service.make_pdf(data)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    worker_max_tasks_per_child=100,
    task_time_limit=300
    )
