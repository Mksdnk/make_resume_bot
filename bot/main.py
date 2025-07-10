import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.config_reader import config
from bot.handlers import common, resume, review
from bot.services.cache import cache_service


async def main():
    try:
        bot = Bot(token=config.BOT_TOKEN.get_secret_value())
        storage = RedisStorage(redis=cache_service.redis_db)
        dp = Dispatcher(storage=storage)
        
        dp.include_router(common.router)
        dp.include_router(resume.router)
        dp.include_router(review.router)
        
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        await cache_service.close()
if __name__ == "__main__":
    asyncio.run(main())

