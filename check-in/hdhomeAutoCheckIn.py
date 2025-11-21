import requests
import re
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operateQLEnv import QL

ql = QL(
  address="http://101.43.54.73:15700",
  id="9UA_I484iUVl",
  secret="RzT9GaB3IiF7v50AavMAsQ_1"
)

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
print("登录页跳转", response.text)

checkIn_response = session.get(urlCheckIn)

print("第二个请求状态码:", checkIn_response.status_code)
print("响应内容类型:", type(checkIn_response.text))
print("响应内容", checkIn_response.text)

# 如果你想查看Cookies，应该这样：
print("Session Cookies:", session.cookies.get_dict())

match = re.search("本次签到获得", checkIn_response.text)

if match:
  print(f"存在于{match.start()}到{match.end()}")

  target_name = "hdhome_checkin_success"
  target_id = 1  # 请替换为你要更新的环境变量的实际ID
  new_value = "true"

  # 执行更新
  if ql.update_env(env_id=target_id, name=target_name, value=new_value, remarks="通过OpenAPI更新"):
    print("操作成功！")
  else:
    print("操作失败。")

# 或者查看响应头中的Cookies：
# print("响应头中的Cookies:", checkIn_response.cookies)

