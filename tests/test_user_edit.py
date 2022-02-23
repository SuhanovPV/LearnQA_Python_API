from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.register_user("/user/", data=register_data)

        # LOGIN
        login_data = {"email": email, "password": password}
        auth_data = self.login_user("/user/login", login_data)

        # EDIT
        new_name = "Changed Name"

        response_edit = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name}, **auth_data)

        Assertions.asser_code_status(response_edit, 200)

        # GET
        response_get = MyRequests.get(f"/user/{user_id}", **auth_data)

        Assertions.assert_json_value_by_name(response_get, "firstName", new_name, "Wrong name of user after edit")

    def test_edit_created_user_without_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        email = register_data["email"]
        name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.register_user("/user/", data=register_data)

        # EDIT
        new_name = "NewName"
        response_edit = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})

        Assertions.asser_code_status(response_edit, 400)
        Assertions.assert_content(response_edit, "Auth token not supplied")

        # LOGIN
        login_data = {"email": email, "password": password}
        auth_data = self.login_user("/user/login", login_data)

        # GET
        response_get = MyRequests.get(f"/user/{user_id}", **auth_data)
        Assertions.assert_json_value_by_name(response_get, "firstName", name, "Name was changed without authorization")

    def test_edit_created_user_auth_as_another_user(self):
        # REGISTER USER WHICH WILL BE CHANGE
        register_data_for_change = self.prepare_registration_data()
        email_for_change = register_data_for_change["email"]
        first_name_for_change = register_data_for_change["firstName"]
        password_for_change = register_data_for_change["password"]
        user_id_for_change = self.register_user("/user/", data=register_data_for_change)

        # REGISTER USER FOR LOGIN
        register_data_for_login = self.prepare_registration_data()
        email_for_login = register_data_for_login["email"]
        first_name_for_login = register_data_for_login["firstName"]
        password_for_login = register_data_for_login["password"]
        user_id_for_login = self.register_user("/user/", data=register_data_for_login)

        # LOGIN
        login_data = {"email": email_for_login, "password": password_for_login}
        auth_dta = self.login_user("/user/login/", login_data)

        # EDIT
        new_name = "NewName"

        response_edit = MyRequests.put(f"/user/{user_id_for_change}", data={"firstName": new_name}, **auth_dta)

        # LOGIN FOR CHECK DATA 'USER FOR CHECK'
        login_data = {"email": email_for_change, "password": password_for_change}
        auth_dta_for_check = self.login_user("/user/login/", login_data)

        # GET DATA 'USER FOR CHECK'
        response_get = MyRequests.get(f"/user/{user_id_for_change}", **auth_dta_for_check)

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            first_name_for_change,
            "Parameter 'firstName' was modified with authorization as another user"
        )

        # LOGIN FOR CHECK DATA 'USER FOR LOGIN'
        login_data = {"email": email_for_login, "password": password_for_login}
        auth_dta_for_login = self.login_user("/user/login/", login_data)

        # GET DATA 'USER FOR CHECK'
        response_get = MyRequests.get(f"/user/{user_id_for_login}", **auth_dta_for_login)

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            first_name_for_login,
            "Parameter 'firstName' was modified for user which was logged"
        )

    def test_edit_email_to_incorrect(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.register_user("/user/", data=register_data)

        # LOGIN
        login_data = {"email": email, "password": password}
        auth_data = self.login_user("/user/login", login_data)

        # EDIT
        new_email = "incorrectemail.com"
        response_edit = MyRequests.put(f"/user/{user_id}", data={"email": new_email}, **auth_data)
        Assertions.asser_code_status(response_edit, 400)
        Assertions.assert_content(response_edit, "Invalid email format")

        # GET
        response_get = MyRequests.get(f"/user/{user_id}", **auth_data)

        Assertions.assert_json_value_by_name(response_get, "email", email, "Email was change to incorrect")

    def test_edit_first_name_to_short(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.register_user("/user/", data=register_data)

        # LOGIN
        login_data = {"email": email, "password": password}
        auth_data = self.login_user("/user/login", login_data)

        # EDIT
        new_name = "a"
        response_edit = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name}, **auth_data)
        Assertions.asser_code_status(response_edit, 400)

        # GET
        response_get = MyRequests.get(f"/user/{user_id}", **auth_data)

        Assertions.assert_json_value_by_name(response_get, "firstName", first_name, "'firstName' was change to short")
