import sqlite3
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Database:
    def __init__(self):
        # Подключаемся к БД и настраиваем получение строк как словарей
        self.conn = sqlite3.connect(Config.DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """
        Создает таблицы users, stats и game_scores:
        - users: хранит информацию о пользователях
        - stats: хранит общую статистику по играм каждого пользователя
        - game_scores: хранит информацию о счете в каждой отдельной игре
        """
        cur = self.conn.cursor()
        # Таблица пользователей
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        # Таблица статистики
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS stats (
                user_id INTEGER PRIMARY KEY,
                games_played INTEGER NOT NULL DEFAULT 0,
                correct_count INTEGER NOT NULL DEFAULT 0,
                incorrect_count INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            """
        )
        # Таблица счетов за игры
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS game_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            """
        )
        self.conn.commit()
        logger.info("Таблицы users, stats и game_scores готовы к работе")

    def add_user(self, user_id: int, username: str, full_name: str = None):
        """
        Добавляет нового пользователя в таблицу users и инициализирует его stats.
        Если пользователь уже есть, ничего не делает.
        """
        try:
            cur = self.conn.cursor()
            # Вставляем или игнорируем, если пользователь уже существует
            cur.execute(
                """
                INSERT OR IGNORE INTO users (user_id, username, full_name)
                VALUES (?, ?, ?)
                """,
                (user_id, username, full_name)
            )
            # Инициализируем статистику
            cur.execute(
                """
                INSERT OR IGNORE INTO stats (user_id)
                VALUES (?)
                """,
                (user_id,)
            )
            self.conn.commit()
            logger.info(f"Пользователь {user_id} - {username} добавлен или уже существует")
        except Exception as e:
            logger.exception(f"Ошибка при добавлении пользователя {user_id}: {e}")

    def update_stats(self, user_id: int, is_correct: bool, score: int):
        """
        Обновляет статистику пользователя:
        - увеличивает games_played
        - увеличивает correct_count или incorrect_count
        - добавляет запись о счете в таблицу game_scores
        """
        try:
            cur = self.conn.cursor()
            # Обновляем агрегированную статистику
            cur.execute(
                """
                UPDATE stats
                SET games_played = games_played + 1,
                    correct_count = correct_count + CASE WHEN ? THEN 1 ELSE 0 END,
                    incorrect_count = incorrect_count + CASE WHEN ? THEN 0 ELSE 1 END
                WHERE user_id = ?
                """,
                (is_correct, is_correct, user_id)
            )
            # Добавляем запись о счете
            cur.execute(
                """
                INSERT INTO game_scores (user_id, score)
                VALUES (?, ?)
                """,
                (user_id, score)
            )
            self.conn.commit()
            logger.info(f"Статистика и счет пользователя {user_id} обновлены: is_correct={is_correct}, score={score}")
        except Exception as e:
            logger.exception(f"Ошибка при обновлении статистики для {user_id}: {e}")

    def get_stats(self, user_id: int) -> dict:
        """
        Возвращает статистику пользователя в виде словаря:
        { games_played, correct_count, incorrect_count, scores: [список всех счетов] }
        Если пользователя нет, возвращает None.
        """
        cur = self.conn.cursor()
        # Получаем агрегированную статистику
        cur.execute(
            """
            SELECT s.games_played, s.correct_count, s.incorrect_count
            FROM stats s
            JOIN users u ON u.user_id = s.user_id
            WHERE s.user_id = ?
            """,
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            logger.warning(f"Статистика для пользователя {user_id} не найдена")
            return None

        # Получаем список всех счетов
        cur.execute(
            """
            SELECT score FROM game_scores
            WHERE user_id = ?
            ORDER BY played_at DESC
            """,
            (user_id,)
        )
        scores = [r['score'] for r in cur.fetchall()]

        return {
            'games_played': row['games_played'],
            'correct_count': row['correct_count'],
            'incorrect_count': row['incorrect_count'],
            'scores': scores
        }

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()
        logger.info("Соединение с БД закрыто")

db = Database()
