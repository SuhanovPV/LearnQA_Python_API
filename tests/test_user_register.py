import pytest
import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Create user cases")
class TestUserRegister(BaseCase):

    exclude_parameters = [("password"), ("username"), ("firstName"), ("lastName"), ("email")]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Create new user")
    @allure.description("Test checks successfully creation of new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Create new user with existing email")
    @allure.description("Test checks creation user with already registered email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"

        allure.dynamic.description(f"Test checks creation user with already registered email '{email}'")

        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user/", data=data)
        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    @allure.title("Create new user with incorrect email")
    @allure.description("Test checks creation user with already incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = "incorrectemail.org"
        allure.description(f"Test checks creation user with already incorrect email '{email}'")
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "Invalid email format")

    @allure.title("Create new user with missing {exclude_parameter}")
    @allure.description("Test checks creation user with missing parameter")
    @pytest.mark.parametrize("exclude_parameter", exclude_parameters)
    def test_create_user_with_missing_parameter(self, exclude_parameter):
        allure.dynamic.description(f"Test checks creation user with missing parameter '{exclude_parameter}'")
        data = self.prepare_registration_data()
        data.pop(exclude_parameter, None)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, f"The following required params are missed: {exclude_parameter}")

    @allure.title("Create new user with too short 'firstName'")
    @allure.description("Test checks creation user with lengths of parameter 'firstName' = 1")
    def test_create_user_with_short_username(self):
        username_length = 1
        data = self.prepare_registration_data(username_length=username_length)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too short")

    @allure.title("Create new user with too large 'firstName'")
    @allure.description("Test checks creation user with lengths of parameter 'firstName' > 250")
    def test_create_user_with_long_username(self):
        username_length = 252
        data = self.prepare_registration_data(username_length=username_length)

        response = MyRequests.post("/user/", data=data)

        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too long")
