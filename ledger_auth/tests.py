from django.urls import reverse
from django.test import Client, TestCase
import json


class TokenTest(TestCase):
    fixtures = ['user.yaml']

    def test_request_token_success(self):
        c = Client()
        response = c.post(
            reverse('get_token'), {'username': 'tony', 'password': '123'}, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    # def test_request_token_fail(self):
    #     c = Client()
    #     response = c.post(
    #         reverse('exchange_for_token'), {'username': 'tony1', 'password': '123'}, content_type='application/json')

    #     self.assertEqual(response.status_code, 400)

    def test_revoke_token(self):
        c = Client()
        token_response = c.post(
            reverse('get_token'), {'username': 'tony', 'password': '123'}, content_type='application/json')

        token = json.loads(token_response.content.decode('utf-8'))['token']

        revoke_response = c.post(
            reverse('revoke_token'), content_type='application/json', authorization=token)

        self.assertEqual(revoke_response.status_code, 200)


# Create your tests here.
