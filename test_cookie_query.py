import requests


class TestCookieQuery:
    def test_cookie_query(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

        print(dict(response.cookies))
        assert "HomeWork" in response.cookies, "Cannot find cookie wit name 'HomeWork'"
        cookie = response.cookies

        assert response.cookies["HomeWork"] == "hw_value", "Value of cookie 'HomeWork' is not 'hw_value'"
