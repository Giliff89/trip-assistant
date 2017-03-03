import unittest
import server


class ServerTests(unittest.TestCase):
    """Tests for my app server functions"""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn("Take the stress out of travel", result.data)

    def test_registration_page(self):
        result = self.client.get('/register')
        self.assertIn("Choose a username:", result.data)

    def test_login_page(self):
        result = self.client.get('/login')
        self.assertIn("Enter your username:", result.data)

    def test_login(self):
        result = self.client.post('/login',
                                  data={"username": "LunaLiterally",
                                        "password": "isBestDog"},
                                  follow_redirects=True)
        self.assertIn("Logged in", result.data)


if __name__ == '__main__':
    unittest.main()
