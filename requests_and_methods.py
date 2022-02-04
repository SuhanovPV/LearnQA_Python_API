import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
METHODS = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]
METHODS_FUNC = [requests.get, requests.post, requests.put, requests.delete]

# Requests without parameters
print("Requests without parameters")
for meth in METHODS_FUNC:
    response = meth(url)
    print(f"{meth.__name__}: {response.text}")

# Request HEAD
print("\nRequest HEAD")
response = requests.head(url, data={"method": "HEAD"})
print(response)

# Correct requests
print("\nCorrect requests")
response = requests.get(url, params={"method": "GET"})
print("GET: " + response.text)
response = requests.post(url, params={"method": "POST"})
print("POST: " + response.text)
response = requests.put(url, data={"method": "PUT"})
print("PUT: " + response.text)
response = requests.delete(url, data={"method": "DELETE"})
print("DELETE: " + response.text)

# Parameter substitution
print("\nParameter substitution")
for meth in METHODS_FUNC:
    if meth.__name__ == "get":
        for param in METHODS:
            response = meth(url, params=param)
            print(f"{meth.__name__}, method: {param['method']}: {response.text}")
        print()
    else:
        for param in METHODS:
            response = meth(url, params=param)
            print(f"{meth.__name__}, method: {param['method']}: {response.text}")
        print()
