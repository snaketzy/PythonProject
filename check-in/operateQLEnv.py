import requests
from json import dumps as jsonDumps
import sys


class QL:
  def __init__(self, address: str, id: str, secret: str) -> None:
    self.address = address  # 例如: "http://127.0.0.1:5700"
    self.id = id
    self.secret = secret
    self.auth = ""  # 初始化认证token
    self.login()  # 实例化时自动登录

  def login(self) -> None:
    """登录并获取认证token"""
    url = f"{self.address}/open/auth/token?client_id={self.id}&client_secret={self.secret}"
    try:
      rjson = requests.get(url).json()
      if rjson['code'] == 200:
        self.auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
        print("登录成功")
      else:
        print(f"登录失败：{rjson['message']}")
    except Exception as e:
      print(f"登录过程异常：{str(e)}")

  def update_env(self, env_id: int, name: str, value: str, remarks: str = "") -> bool:
    """
    更新一个已存在的环境变量
    :param env_id: 环境变量的ID（可通过get_envs方法获取）
    :param name: 变量名
    :param value: 变量值
    :param remarks: 备注信息（可选）
    :return: 成功返回True，失败返回False
    """

    real_env_id = env_id
    real_name = name
    real_value = value
    real_remarks = "通过OpenAPI更新"

    if len(sys.argv) > 1:
      first_arg = sys.argv[1]
      second_arg = sys.argv[2]
      third_arg = sys.argv[3] if len(sys.argv) > 3 else "默认值"
      print(f"第一个参数: {first_arg}")
      real_env_id = first_arg
      print(f"第二个参数: {second_arg}")
      real_name = second_arg
      print(f"第三个参数: {third_arg}")
      real_value = third_arg
    else:
      print("命令后无参数。")

    if not self.auth:
      print("错误：请先登录")
      return False

    url = f"{self.address}/open/envs"
    headers = {
      "Authorization": self.auth,
      "content-type": "application/json"
    }
    # 构造要更新的环境变量数据
    env_data = {
      "id": real_env_id,
      "name": f"{real_name}_checkin_success",
      "value": real_value,
      "remarks": real_remarks  # 根据API实际字段名调整，可能是"remarks"或"remark"
    }

    try:
      response = requests.put(url, headers=headers, data=jsonDumps(env_data), timeout=10)
      response.raise_for_status()
      rjson = response.json()

      if rjson['code'] == 200:
        print(f"环境变量 '{real_name}' (ID: {env_id}) 更新成功")
        return True
      else:
        print(f"更新失败（API返回错误）：{rjson['message']}")
        # 如果是token过期，可以尝试重新登录
        if rjson['code'] in [401, 403]:  # 具体的错误码需根据青龙面板API文档调整
          print("Token可能已过期，尝试重新登录...")
          if self.login():
            # 重新登录成功后，递归调用自身重试一次（注意控制递归深度）
            return self.update_env(env_id, name, value, remarks)
        return False
    except requests.exceptions.RequestException as e:
      print(f"更新环境变量请求异常：{str(e)}")
      return False

  def get_envs(self) -> list:
    """获取所有环境变量"""
    url = f"{self.address}/open/envs"
    headers = {"Authorization": self.auth}
    try:
      rjson = requests.get(url, headers=headers).json()
      if rjson['code'] == 200:
        return rjson['data']
      else:
        print(f"获取失败：{rjson['message']}")
        return []
    except Exception as e:
      print(f"获取过程异常：{str(e)}")
      return []


# 使用示例
if __name__ == "__main__":
  # 初始化，替换为你的实际地址、ID和Secret
  ql = QL("http://101.43.54.73:15700", "-9Kv1wOZrlbz", "MDcNL1_pOSHH7MslVNSDwbjU")

  # 获取所有现有环境变量
  all_envs = ql.get_envs()
  print(f"当前共有 {len(all_envs)} 个环境变量")

  for env in all_envs:
    print(f"ID: {env['id']}, 名称: {env['name']}, 值: {env['value']}")

  target_name = "hdhome"
  target_id = 1  # 请替换为你要更新的环境变量的实际ID
  new_value = "false"

  # 执行更新
  if ql.update_env(env_id=target_id, name=target_name, value=new_value, remarks="通过OpenAPI更新"):
    print("操作成功！")
  else:
    print("操作失败。")