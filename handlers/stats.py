from aiogram import Router, F
from aiogram.types import Message
from config import Config
from utils.logger import setup_logger
from database import db  
logger = setup_logger(__name__)
router = Router()


@router.message(F.text == '/stats')
async def cmd_stats(message: Message):
    user_id = message.from_user.id
    try:
        logger.debug(f"Получен запрос /stats от пользователя {user_id}")

        stats = db.get_stats(user_id) 

        if not stats:
            await message.answer("😕 Статистика не найдена. Сыграй хотя бы одну игру!")
            return

        total_score = sum(stats['scores'])
        recent_scores = stats['scores'][:5]
        recent_str = ', '.join(str(s) for s in recent_scores) if recent_scores else '—'

        response = (
            "📊 Ваша статистика:\n\n"
            f"🎮 Сыграно игр: {stats['games_played']}\n"
            f"✅ Правильных ходов: {stats['correct_count']}\n"
            f"❌ Ошибок: {stats['incorrect_count']}\n"
            f"🏅 Суммарный счёт: {total_score}\n"
            f"🕹 Последние игры: {recent_str}"
        )
        await message.answer(response)

    except Exception as e:
        logger.exception(f"Ошибка при получении статистики пользователя {user_id}")
        await message.answer("❌ Ошибка при получении статистики. Попробуйте позже.")
