import time
import requests
from json.decoder import JSONDecodeError

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
obj = {}
try:
    obj = response.json()
except JSONDecodeError:
    print("Response is not in JSON format")

if ("token" in obj) and ("seconds" in obj):
    token = obj["token"]
    timeout = obj["seconds"]

    # Request before completing
    response = requests.get(url, params={"token": token})
    print(response.text)

    # Request after completing
    time.sleep(timeout)
    response = requests.get(url, params={"token": token})
    print(response.text)
