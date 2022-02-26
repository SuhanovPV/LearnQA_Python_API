from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestDeleteUser(BaseCase):
    def test_delete_protected_user(self):
        # LOGIN
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        auth_data = self.login_user("/user/login", data)

        # DELETE
        response = MyRequests.delete("/user/2", **auth_data)
        Assertions.asser_code_status(response, 400)
        Assertions.assert_content(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        # CHECK
        response_get = MyRequests.get(f"/user/2", **auth_data)
        Assertions.asser_code_status(response_get, 200)
        Assertions.assert_json_value_by_name(response_get, "email", data["email"], f"Unexpected value of 'email'")

    def test_delete_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.register_user("/user/", data=register_data)

        # LOGIN
        login_data = {"email": email, "password": password}
        auth_data = self.login_user("/user/login", login_data)

        # DELETE
        response_delete = MyRequests.delete(f"/user/{user_id}", **auth_data)
        Assertions.asser_code_status(response_delete, 200)

        # GET
        response_get = MyRequests.get(f"/user/{user_id}")
        Assertions.asser_code_status(response_get, 404)
        Assertions.assert_content(response_get, "User not found")

    def test_delete_user_auth_as_another_user(self):
        # REGISTER USER FOR DELETE
        register_data_del = self.prepare_registration_data()
        print("\n####################################")
        print(register_data_del)
        print("\n####################################")
        user_id_del = self.register_user("/user/", data=register_data_del)

        # REGISTER USER FOR AUTH
        register_data_auth = self.prepare_registration_data()
        print("\n####################################")
        print(register_data_auth)
        print("\n####################################")
        email_auth = register_data_auth["email"]
        password_auth = register_data_auth["password"]
        user_id_auth = self.register_user("/user/", data=register_data_auth)

        # LOGIN
        login_data = {"email": email_auth, "password": password_auth}
        auth_data = self.login_user("/user/login", login_data)

        # DELETE
        response_delete = MyRequests.delete("/user/2", **auth_data)

        # GET USER FOR DELETE
        response_get_del = MyRequests.get(f"/user/{user_id_del}")
        Assertions.asser_code_status(response_get_del, 200)

        # GET
        response_get_auth = MyRequests.get(f"/user/{user_id_auth}")
        Assertions.asser_code_status(response_get_auth, 200)










