#~/cypress/beta1/backend/tests/test_create_movie.py

import json

from tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):

    def test_successful_login(self):
        # Given
        first = "john"
        last = "doe"
        email = "paurakh011@gmail.com"
        role = "woooo"
        company = "thisplace"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "first": first,
            "last": last,
            "email": email,
            "role": role,
            "company": company,
            "password": password
        })

        self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=user_payload)
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json['token']

        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"]
        }
        # When
        response = self.app.post('/api/movies',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
            data=json.dumps(movie_payload))

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

