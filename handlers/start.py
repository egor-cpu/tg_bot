from aiogram import Router, F
from aiogram.types import Message
from database import Database
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router()

@router.message(F.text == '/start')
async def cmd_start(message: Message):
    try:
        user = message.from_user
        logger.info(f"New user: {user.id} @{user.username} {user.full_name}")
        
        db = Database()
        db.add_user(user.id, user.username, user.full_name)
        
        welcome_text = (
            f"Привет, {user.full_name}! {Config.EMOJI_MAP['fire']}\n"
            "Я бот для игры '3 в ряд'!\n"
            "Используй /game чтобы начать игру\n"
            "/stats чтобы посмотреть статистику"
        )
        await message.answer(welcome_text)
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.answer("Произошла ошибка, попробуйте позже")