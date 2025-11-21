import requests

url = 'http://hdhome.org/'
urlLogin = 'https://hdhome.org/takelogin.php'
urlCheckIn = 'https://hdhome.org/attendance.php'

headers = {
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-User': '?1',
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    'Accept': '*/*',
    'Host': 'hdhome.org',
    'Connection': 'keep-alive'
}
#
# cookies = {
#     'c_secure_uid': 'MTE3NjU1',
#     'c_secure_pass': '5129cbefb04fc68e862ac1fc0cb1dc3b',
#     'c_secure_ssl': 'bm9wZQ%3D%3D',
#     'c_secure_tracker_ssl': 'bm9wZQ%3D%3D',
#     'c_secure_login': 'bm9wZQ%3D%3D'
# }

data = {
    'username': 'snaketzy',
    'password': 'snaketzy123$',
    'scode': ''
}

session = requests.Session()

response = session.post(
    urlLogin,
    headers=headers,
    # cookies=cookies,
    data=data
)


print("登录结果", response.status_code)
print("登录结果", response.status_code)
print("登录页跳转", response.text)

checkIn_response = session.get(urlCheckIn)

print("第二个请求状态码:", checkIn_response.status_code)
print("响应内容类型:", type(checkIn_response.text))
print("响应内容", checkIn_response.text)

# 如果你想查看Cookies，应该这样：
print("Session Cookies:", session.cookies.get_dict())

# 或者查看响应头中的Cookies：
print("响应头中的Cookies:", checkIn_response.cookies)

