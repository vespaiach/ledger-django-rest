from django.test import Client
import json

from ledger_core.utils import APITestCase


class TokenTest(APITestCase):
    fixtures = ['user.yaml']

    def test_request_token_success(self):
        c = Client()
        response = c.post(
            '/api/token', {'username': 'tony', 'password': '123'}, content_type='application/json')

        self.is_status_200(response)
        self.is_json_content(response)

        data = self.to_dict(response)

        self.assertTrue('token' in data)

    def test_request_token_fail(self):
        c = Client()
        response = c.post(
            '/api/token', {'username': 'tony1', 'password': '123'}, content_type='application/json')

        self.is_status_400(response)
        self.is_json_content(response)

    def test_request_token_with_missing_fields(self):
        c = Client()
        response = c.post(
            '/api/token', {'password': '123'}, content_type='application/json')

        self.is_status_400(response)
        self.is_json_content(response)

    def test_revoke_token(self):
        c = Client()
        token_response = c.post(
            '/api/token', {'username': 'tony', 'password': '123'}, content_type='application/json')

        token = json.loads(token_response.content.decode('utf-8'))['token']

        revoke_response = c.delete(
            '/api/token', content_type='application/json', authorization=token)

        self.assertEqual(revoke_response.status_code, 204)
