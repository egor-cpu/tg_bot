from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router()

@router.message(F.text == '/game')
async def cmd_game(message: Message):
    try:
        logger.debug(f"/game command from {message.from_user.id}")
        
        game_button = KeyboardButton(
            text="🎮 Начать игру",
            web_app=WebAppInfo(url="https://192.168.1.13:5000/")
        )
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[game_button]],
            resize_keyboard=True,
            one_time_keyboard=True  
        )
        
        await message.answer(
            "Добро пожаловать в игру!",
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"Game error: {e}")
        await message.answer("Произошла ошибка при запуске игры")