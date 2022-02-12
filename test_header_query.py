import requests


class TestHeaderQuery:
    def test_header_query(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        assert "x-secret-homework-header" in response.headers, \
            "Cannot find header 'x-secret-homework-header' in headers"

        assert response.headers["x-secret-homework-header"] == "Some secret value", \
            "header value does not match 'Some secret value'"
