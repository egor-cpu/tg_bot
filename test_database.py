import unittest
import sqlite3
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.conn = sqlite3.connect(':memory:')
        self.db.conn.row_factory = sqlite3.Row
        self.db.create_tables()

    def tearDown(self):
        self.db.close()

    def test_add_user(self):
        self.db.add_user(1, 'testuser', 'Test User')
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = 1")
        user = cur.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')

    def test_add_duplicate_user(self):
        self.db.add_user(1, 'testuser', 'Test User')
        self.db.add_user(1, 'testuser', 'Test User')
        cur = self.db.conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM users WHERE user_id = 1")
        count = cur.fetchone()['cnt']
        self.assertEqual(count, 1)

    def test_update_stats_correct(self):
        self.db.add_user(1, 'player', 'Player One')
        self.db.update_stats(1, is_correct=True, score=10)
        stats = self.db.get_stats(1)
        self.assertEqual(stats['games_played'], 1)
        self.assertEqual(stats['correct_count'], 1)
        self.assertEqual(stats['incorrect_count'], 0)
        self.assertEqual(stats['scores'], [10])

    def test_update_stats_incorrect(self):
        self.db.add_user(2, 'noob', 'Player Two')
        self.db.update_stats(2, is_correct=False, score=3)
        stats = self.db.get_stats(2)
        self.assertEqual(stats['games_played'], 1)
        self.assertEqual(stats['correct_count'], 0)
        self.assertEqual(stats['incorrect_count'], 1)
        self.assertEqual(stats['scores'], [3])

    def test_get_stats_no_user(self):
        stats = self.db.get_stats(999)
        self.assertIsNone(stats)

if __name__ == '__main__':
    unittest.main()
