import json.decoder
import random
import string
from requests import Response
from datetime import datetime


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, respose: Response, headers_name):
        assert headers_name in respose.headers, f"Cannot find header with name {headers_name} in the last response"
        return respose.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Rsponse JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def generate_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        return f"{base_part}{random_part}@{domain}"

    def generate_username(self, length: int):
        char_list = [random.choice(string.ascii_letters) for i in range(length)]
        return "".join(char_list)

    def prepare_registration_data(self, username_length=-1, email=None):
        if email is None:
            email = self.generate_email()
        username = "learnqa" if username_length < 0 else self.generate_username(username_length)

        return {
            "password": "123",
            "username": username,
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }
