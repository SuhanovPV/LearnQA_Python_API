import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    exclude_parameters = [("password"), ("username"), ("firstName"), ("lastName"), ("email")]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user/", data=data)
        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    def test_create_user_with_incorrect_email(self):
        email = "incorrectemail.org"
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "Invalid email format")

    @pytest.mark.parametrize("exclude_parameter", exclude_parameters)
    def test_create_user_with_missing_parameter(self, exclude_parameter):
        data = self.prepare_registration_data()
        data.pop(exclude_parameter, None)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, f"The following required params are missed: {exclude_parameter}")

    def test_create_user_with_short_username(self):
        username_length = 1
        data = self.prepare_registration_data(username_length=username_length)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too short")

    def test_create_user_with_long_username(self):
        username_length = 252
        data = self.prepare_registration_data(username_length=username_length)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too long")