from aiogram import Router, F
from aiogram.types import Message
from database import db 
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router()

@router.message(F.text == '/start')
async def cmd_start(message: Message):
    try:
        user = message.from_user
        user_id = user.id
        username = user.username or "unknown"
        full_name = user.full_name or user.first_name or "Гость"

        logger.info(f"Обработка команды /start от пользователя {user_id} (@{username}, {full_name})")

        db.add_user(user_id, username, full_name)

        welcome_text = (
            f"Привет, {full_name}! {Config.EMOJI_MAP.get('fire', '🔥')}\n"
            "Я бот для игры '3 в ряд'!\n"
            "Вот что ты можешь сделать:\n"
            f"• /game — начать игру\n"
            f"• /stats — посмотреть свою статистику"
        )
        await message.answer(welcome_text)

    except Exception as e:
        logger.exception("Ошибка при выполнении команды /start")
        await message.answer("Произошла ошибка при запуске. Попробуй снова позже.")
