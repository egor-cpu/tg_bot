from aiogram import Router, F
from aiogram.types import Message
from config import Config
from utils.logger import setup_logger
from database import Database

logger = setup_logger(__name__)
router = Router()

# Инициализируем базу данных
db = Database()

@router.message(F.text == '/stats')
async def cmd_stats(message: Message):
    try:
        logger.debug(f"/stats request from {message.from_user.id}")
        logger.error("В разработке!")
        raise 

        user_id = message.from_user.id
        stats = await db.get_user_stats(user_id)
        
        if not stats:
            return await message.answer("Статистика не найдена")
            
        response = (
            "📊 Ваша статистика:\n\n"
            f"🎮 Всего игр: {stats['total_games']}\n"
            f"🏆 Побед: {stats['wins']}\n"
            f"💥 Поражений: {stats['losses']}\n"
            f"📅 Последняя игра: {stats['last_game']}\n"
            f"🔥 Текущая серия: {stats['current_streak']}"
        )
        
        await message.answer(response)

    except Exception as e:
        logger.error(f"Stats error: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении статистики. Попробуйте позже")