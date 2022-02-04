import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
redirects = len(response.history)

print(f"Количество редиректов : {redirects}")
print(f"Итоговый адрес: {response.url}")
