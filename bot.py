import asyncio
import subprocess
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from database import db
from utils.logger import setup_logger

from handlers.start import router as start_router
from handlers.game import router as game_router
from handlers.stats import router as stats_router

logger = setup_logger(__name__)
storage = MemoryStorage()
bot = Bot(token=Config.API_TOKEN)
dp = Dispatcher(storage=storage)

@dp.startup()
async def on_startup():
    logger.info("Бот запущен и БД подключена")

@dp.shutdown()
async def on_shutdown():
    db.close()
    logger.info("Соединение с БД закрыто")

async def main():
    dp.include_router(start_router)
    dp.include_router(game_router)
    dp.include_router(stats_router)

    # subprocess.Popen(['python', 'app/main.py'], cwd='.')
    logger.info("Запуск polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановлен пользователем")
