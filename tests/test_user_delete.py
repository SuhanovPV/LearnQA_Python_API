import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.title("Deletion protected user test")
    @allure.description("This test checks if protected user cannot be deleted")
    def test_delete_protected_user(self):
        with allure.step("Logining as protected user"):
            data = {'email': 'vinkotov@example.com', 'password': '1234'}
            auth_data = self.login_user("/user/login", data)

        with allure.step("Delete user"):
            response = MyRequests.delete("/user/2", **auth_data)
            Assertions.asser_code_status(response, 400)
            Assertions.assert_content(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        with allure.step("Check that protected user has not be deleted"):
            response_get = MyRequests.get(f"/user/2", **auth_data)
            Assertions.asser_code_status(response_get, 200)
            Assertions.assert_json_value_by_name(response_get, "email", data["email"], f"Unexpected value of 'email'")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Deletion created user")
    @allure.description("This test successfully delete just created user")
    def test_delete_user(self):
        with allure.step("Creating a new user for deletion"):
            register_data = self.prepare_registration_data()
            email = register_data["email"]
            password = register_data["password"]
            user_id = self.register_user("/user/", data=register_data)

        with allure.step("Logining as created user"):
            login_data = {"email": email, "password": password}
            auth_data = self.login_user("/user/login", login_data)

        with allure.step("Delete user"):
            response_delete = MyRequests.delete(f"/user/{user_id}", **auth_data)

            Assertions.asser_code_status(response_delete, 200)

        with allure.step("Check that protected user has been deleted"):
            response_get = MyRequests.get(f"/user/{user_id}")

            Assertions.asser_code_status(response_get, 404)
            Assertions.assert_content(response_get, "User not found")

    @allure.title("Deletion created user auth with another")
    @allure.description("This test checks possibility to delete user, when auth with another")
    def test_delete_user_auth_as_another_user(self):
        with allure.step("Creating a new user #1 for deletion"):
            register_data_del = self.prepare_registration_data()
            user_id_del = self.register_user("/user/", data=register_data_del)

        with allure.step("Creating a new user #2 for authorization"):
            register_data_auth = self.prepare_registration_data()
            email_auth = register_data_auth["email"]
            password_auth = register_data_auth["password"]
            user_id_auth = self.register_user("/user/", data=register_data_auth)

        with allure.step("Logining as user #2"):
            login_data = {"email": email_auth, "password": password_auth}
            auth_data = self.login_user("/user/login", login_data)

        with allure.step("Delete user"):
            response_delete = MyRequests.delete("/user/2", **auth_data)

        with allure.step("Check that user #1 has not be deleted"):
            response_get_del = MyRequests.get(f"/user/{user_id_del}")

            Assertions.asser_code_status(response_get_del, 200)

        with allure.step("Check that user #1 has not be deleted"):
            response_get_auth = MyRequests.get(f"/user/{user_id_auth}")

            Assertions.asser_code_status(response_get_auth, 200)
