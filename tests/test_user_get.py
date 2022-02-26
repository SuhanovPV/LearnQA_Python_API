import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Get user info cases")
class TestUserGet(BaseCase):
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Get user info w/o auth")
    @allure.description("Test checks getting user information without authorization")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, unexpected_keys)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Get user info with auth")
    @allure.description("Test checks getting user information with authorization")
    def test_get_user_details_auth_as_same_user(self):
        with allure.step("User authorization"):
            data = {'email': 'vinkotov@example.com', 'password': '1234'}
            response_auth = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response_auth, "auth_sid")
            token = self.get_header(response_auth, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response_auth, "user_id")

        with allure.step("Get user info"):
            response_get_user = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.asser_json_has_keys(response_get_user, expected_fields)

    @allure.title("Get user info with auth as another")
    @allure.description("Test checks getting user information with authorization as another user")
    def test_get_user_detail_auth_as_another_user(self):
        with allure.step("Authorize as user id=2"):
            data = {'email': 'vinkotov@example.com', 'password': '1234'}
            response_auth = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response_auth, "auth_sid")
            token = self.get_header(response_auth, "x-csrf-token")

        with allure.step("Get info for user id=1"):
            response_get_user = MyRequests.get(
                f"/user/1",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            unexpected_keys = ["email", "firstName", "lastName"]
            Assertions.assert_json_has_key(response_get_user, "username")
            Assertions.assert_json_has_not_keys(response_get_user, unexpected_keys)

    @allure.title("Get user info with auth as another")
    @allure.description("Test checks getting user information with authorization as another just created user")
    def test_get_user_detail_register_and_login_another_user(self):
        with allure.step("Create new user"):
            registration_data = self.prepare_registration_data(username_length=12)
            login_data = {
                "email": registration_data["email"],
                "password": registration_data["password"]
            }
            response_registration = MyRequests.post("/user/", data=registration_data)
            Assertions.asser_code_status(response_registration, 200)

        with allure.step("Logging as created user"):
            response_login = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        with allure.step("Get info for user id=1"):
            response_get_user = MyRequests.get(
                f"/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            unexpected_keys = ["email", "firstName", "lastName"]
            Assertions.assert_json_has_key(response_get_user, "username")
            Assertions.assert_json_has_not_keys(response_get_user, unexpected_keys)
