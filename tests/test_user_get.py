from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, unexpected_keys)

    def test_get_user_details_auth_as_same_user(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response_auth = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_auth, "user_id")

        response_get_user = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.asser_json_has_keys(response_get_user, expected_fields)

    def test_get_user_detail_auth_as_another_user(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response_auth = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")

        response_get_user = MyRequests.get(
            f"/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response_get_user, "username")
        Assertions.assert_json_has_not_keys(response_get_user, unexpected_keys)

    def test_get_user_detail_register_and_login_another_user(self):
        registration_data = self.prepare_registration_data(username_length=12)
        login_data = {
            "email": registration_data["email"],
            "password": registration_data["password"]
        }
        response_registration = MyRequests.post("/user/", data=registration_data)
        Assertions.asser_code_status(response_registration, 200)

        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_get_user = MyRequests.get(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response_get_user, "username")
        Assertions.assert_json_has_not_keys(response_get_user, unexpected_keys)









