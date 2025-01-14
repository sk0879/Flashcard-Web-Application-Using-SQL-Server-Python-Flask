import unittest
import json
from app import app, db, User, Flashcard, History

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up the test client and database
        self.app = app.test_client()
        self.app.testing = True

        # Create the tables in the test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_view_history_not_authenticated(self):
        response = self.app.get('/view_history')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'User not authenticated')

    def test_save_history_no_email(self):
        response = self.app.post('/save_history', json={'score_percentage': 90})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Email or score_percentage missing.')

if __name__ == '__main__':
    unittest.main()
