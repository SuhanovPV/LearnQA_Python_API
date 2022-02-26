import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Edit a created user")
    @allure.description("Test checks editing just created user")
    def test_edit_just_created_user(self):
        with allure.step("Creating a new user for editing"):
            register_data = self.prepare_registration_data()
            email = register_data["email"]
            password = register_data["password"]
            user_id = self.register_user("/user/", data=register_data)

        with allure.step("Logining as created user"):
            login_data = {"email": email, "password": password}
            auth_data = self.login_user("/user/login", login_data)

        with allure.step("Editing user"):
            allure.dynamic.description(f"Test checks editing 'firstName' for just created user")

            new_name = "Changed Name"

            response_edit = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name}, **auth_data)

            Assertions.asser_code_status(response_edit, 200)

        with allure.step("Check that user has been modified"):
            response_get = MyRequests.get(f"/user/{user_id}", **auth_data)
            Assertions.assert_json_value_by_name(response_get, "firstName", new_name, "Wrong name of user after edit")

    @allure.title("Edit a created user w/o auth")
    @allure.description("Test checks just created user without authorization")
    def test_edit_created_user_without_auth(self):
        with allure.step("Creating a new user for editing"):
            register_data = self.prepare_registration_data()
            email = register_data["email"]
            name = register_data["firstName"]
            password = register_data["password"]
            user_id = self.register_user("/user/", data=register_data)

        with allure.step("Editing user"):
            allure.dynamic.description(f"Test checks editing 'firstName' of user without authorization")

            new_name = "NewName"

            response_edit = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})

            Assertions.asser_code_status(response_edit, 400)
            Assertions.assert_content(response_edit, "Auth token not supplied")

        with allure.step("Logining as created user"):
            login_data = {"email": email, "password": password}
            auth_data = self.login_user("/user/login", login_data)

        with allure.step("Check that user has not been modified"):
            response_get = MyRequests.get(f"/user/{user_id}", **auth_data)
            Assertions.assert_json_value_by_name(
                response_get,
                "firstName",
                name,
                "Name was changed without authorization"
            )

    @allure.title("Edit a created user auth with another")
    @allure.description("This test checks possibility to edit user, when auth with another")
    def test_edit_created_user_auth_as_another_user(self):
        with allure.step("Creating a new user #1 for editing"):
            register_data_for_change = self.prepare_registration_data()
            email_for_change = register_data_for_change["email"]
            first_name_for_change = register_data_for_change["firstName"]
            password_for_change = register_data_for_change["password"]
            user_id_for_change = self.register_user("/user/", data=register_data_for_change)

        with allure.step("Creating a new user #2 for authorization"):
            register_data_for_login = self.prepare_registration_data()
            email_for_login = register_data_for_login["email"]
            first_name_for_login = register_data_for_login["firstName"]
            password_for_login = register_data_for_login["password"]
            user_id_for_login = self.register_user("/user/", data=register_data_for_login)

        with allure.step("Logining as user #2"):
            login_data = {"email": email_for_login, "password": password_for_login}
            auth_dta = self.login_user("/user/login/", login_data)

        with allure.step("Editing user"):
            allure.dynamic.description(f"Test checks editing 'firstName' of user, when auth with another")
        new_name = "NewName"

        response_edit = MyRequests.put(f"/user/{user_id_for_change}", data={"firstName": new_name}, **auth_dta)

        with allure.step("Logining as created user #1"):
            login_data = {"email": email_for_change, "password": password_for_change}
            auth_dta_for_check = self.login_user("/user/login/", login_data)

        with allure.step("Check that user #1 has not been modified"):
            response_get = MyRequests.get(f"/user/{user_id_for_change}", **auth_dta_for_check)

            Assertions.assert_json_value_by_name(
                response_get,
                "firstName",
                first_name_for_change,
                "Parameter 'firstName' was modified with authorization as another user"
            )

        with allure.step("Logining as created user #2"):
            login_data = {"email": email_for_login, "password": password_for_login}
            auth_dta_for_login = self.login_user("/user/login/", login_data)

        with allure.step("Check that user #2 has not been modified"):
            response_get = MyRequests.get(f"/user/{user_id_for_login}", **auth_dta_for_login)

            Assertions.assert_json_value_by_name(
                response_get,
                "firstName",
                first_name_for_login,
                "Parameter 'firstName' was modified for user which was logged"
            )

    @allure.title("Edit email for user to incorrect")
    @allure.description("This test checks possibility to edit 'email' for user to incorrect value")
    def test_edit_email_to_incorrect(self):
        with allure.step("Creating a new user for editing"):
            register_data = self.prepare_registration_data()
            email = register_data["email"]
            password = register_data["password"]
            user_id = self.register_user("/user/", data=register_data)

        with allure.step("Logining as created user"):
            login_data = {"email": email, "password": password}
            auth_data = self.login_user("/user/login", login_data)

        with allure.step("Editing user"):
            new_email = "incorrectemail.com"
            allure.dynamic.description(
                f"This test checks possibility to edit 'email' for user to incorrect value '{new_email}'"
            )
            response_edit = MyRequests.put(f"/user/{user_id}", data={"email": new_email}, **auth_data)
            Assertions.asser_code_status(response_edit, 400)
            Assertions.assert_content(response_edit, "Invalid email format")

        with allure.step("Check that user has not been modified"):
            response_get = MyRequests.get(f"/user/{user_id}", **auth_data)

            Assertions.assert_json_value_by_name(response_get, "email", email, "Email was change to incorrect")

    @allure.title("Edit firstName for user to short")
    @allure.description("This test checks possibility to edit 'firstName' for user to short value")
    def test_edit_first_name_to_short(self):
        with allure.step("Creating a new user for editing"):
            register_data = self.prepare_registration_data()
            email = register_data["email"]
            first_name = register_data["firstName"]
            password = register_data["password"]
            user_id = self.register_user("/user/", data=register_data)

        with allure.step("Logining as created user"):
            login_data = {"email": email, "password": password}
            auth_data = self.login_user("/user/login", login_data)

        with allure.step("Editing user"):
            new_name = "a"
            allure.dynamic.description(
                f"This test checks possibility to edit 'firstName' for user to short value '{new_name}'"
            )
            response_edit = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name}, **auth_data)
            Assertions.asser_code_status(response_edit, 400)

        with allure.step("Check that user has not been modified"):
            response_get = MyRequests.get(f"/user/{user_id}", **auth_data)

            Assertions.assert_json_value_by_name(response_get, "firstName", first_name, "'firstName' was change to short")
