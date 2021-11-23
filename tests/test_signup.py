#~/cypress/beta1/backend/tests/test_signup.py


import json

from tests.BaseCase import BaseCase

class TestUserSignup(BaseCase):

    def test_successful_signup(self):
        # Given
        first = "john"
        last = "doe"
        email = "paurakh011@gmail.com"
        role = "woooo"
        company = "thisplace"
        password = "mycoolpassword"
        payload = json.dumps({
            "first": first,
            "last": last,
            "email": email,
            "role": role,
            "company": company,
            "password": password
        })

        # When
        response = self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_signup_with_non_existing_field(self):
        #Given
        first = "john"
        last = "doe"
        email = "paurakh011@gmail.com"
        role = "woooo"
        company = "thisplace"
        password = "mycoolpassword"
        payload = json.dumps({
            "username": "username",
            "first": first,
            "last": last,
            "email": email,
            "role": role,
            "company": company,
            "password": password
        })

        #When
        response = self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Request is missing required fields', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_signup_without_email(self):
        #Given
        payload = json.dumps({
            "password": "pswddddd",
        })

        #When
        response = self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Something went wrong', response.json['message'])
        self.assertEqual(500, response.status_code)

    def test_signup_without_password(self):
        #Given
        payload = json.dumps({
            "email": "paurakh011@gmail.com",
        })

        #When
        response = self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Something went wrong', response.json['message'])
        self.assertEqual(500, response.status_code)

    def test_creating_already_existing_user(self):
        #Given
        first = "john"
        last = "doe"
        email = "paurakh011@gmail.com"
        role = "woooo"
        company = "thisplace"
        password = "mycoolpassword"
        payload = json.dumps({
            "username": "username",
            "first": first,
            "last": last,
            "email": email,
            "role": role,
            "company": company,
            "password": password
        })
        response = self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/api/auth/newuser', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('User with given email address already exists', response.json['message'])
        self.assertEqual(400, response.status_code)