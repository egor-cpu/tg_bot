from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from database import Database
from utils.logger import setup_logger
import asyncio
import handlers
from handlers.start import router as start_router
from handlers.game import router as game_router
from handlers.stats import router as stats_router

logger = setup_logger(__name__)

db = Database()
storage = MemoryStorage()
bot = Bot(token=Config.API_TOKEN)
dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(start_router)
    dp.include_router(game_router)
    dp.include_router(stats_router)

    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")