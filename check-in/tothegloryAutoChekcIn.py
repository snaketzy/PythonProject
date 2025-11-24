from playwright.sync_api import sync_playwright
import re
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operateQLEnv import QL

ql = QL(
  address="http://101.43.54.73:15700",
  id="-9Kv1wOZrlbz",
  secret="MDcNL1_pOSHH7MslVNSDwbjU"
)


def login_with_headless_browser(url, username, password):
  """
    使用无头浏览器进行网站登录
    Chromium 141.0.7390.37 (playwright build v1194)

    参数:
        url: 登录页面地址
        username: 用户名
        password: 密码
  """
  with sync_playwright() as playwright:

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    browser = playwright.chromium.launch(
    #   headless=False,
      headless=True,
      slow_mo=2000
    )
    context = browser.new_context(user_agent=user_agent)
    page = context.new_page()

    try:
      # 导航到指定页
      page.goto(url)
      print(f"已访问：{url}")

      # 等待页面加载元素@ref
      page.wait_for_load_state("networkidle")

      # 填写登录表单
      if page.wait_for_selector("#login-name"):
        print(f"找到：login-name")
        page.fill("#login-name", username)
      if page.wait_for_selector("#login-pass"):
        print(f"找到：login-pass")
        page.fill("#login-pass", password)
      if page.wait_for_selector("div.chn  input[type='submit']"):
        print(f"找到：div.chn  input[type='submit']")
        page.click("div.chn  input[type='submit']")

      # 等待页面加载元素@ref
      page.wait_for_load_state("networkidle")

      if page.get_by_text("欢迎回来"):
        print(f"找到：欢迎回来")
        print(context.cookies())
        print("登录完成")

      if page.get_by_text("已签到").is_visible():
        print("已签过")

        target_name = "ttg"
        target_id = 2  # 请替换为你要更新的环境变量的实际ID
        new_value = "false"
        # 执行更新
        if ql.update_env(env_id=target_id, name=target_name, value=new_value, remarks="通过OpenAPI更新"):
          print("操作成功！")
        else:
          print("操作失败。")

        browser.close()
      elif page.wait_for_selector("#sp_signed #signed"):
        print(f"找到：签到")
        page.click("#sp_signed #signed")
        print("签到完成")

        target_name = "ttg"
        target_id = 2  # 请替换为你要更新的环境变量的实际ID
        new_value = "true"

        # 执行更新
        if ql.update_env(env_id=target_id, name=target_name, value=new_value, remarks="通过OpenAPI更新"):
          print("操作成功！")
        else:
          print("操作失败。")

        browser.close()
      else:
        print("没有操作")
        browser.close()

    except Exception as e:
      print(f"签到过程中出现错误: {e}")
      # 截图用于调试[6](@ref)
      page.screenshot(path="login_error.png")
    finally:
      # 关闭浏览器[1](@ref)
      browser.close()


if __name__ == "__main__":
  urlLogin = 'https://totheglory.im/login.php'
  urlCheckIn = 'https://hdhome.org/attendance.php'
  username = "snaketzy"
  password = "Snaketzy123$"

  login_with_headless_browser(urlLogin, username, password)
