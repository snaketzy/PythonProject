#encoding =utf-8
import random
import ssl
import time
import urllib.request
import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 导入封装工具package
import tools.browserInfo as browserInfo
import tools.cookies as cookies
import tools.windowInfo as windowInfo
import tools.colors as colors

# 导入业务子模块测试用例
import components.customer.add as addOpportunity

driver = webdriver.Chrome()

driver.set_window_size(1400, 1000)

driver.get('http://devlogin.viphrm.com/')
elem_user = driver.find_element_by_name("userName")
elem_user.send_keys("15821996168")
elem_pwd = driver.find_element_by_name("password")
elem_pwd.send_keys("123456")
driver.find_element_by_xpath("//button[@class='btn btn-block btn-primary']").click() #登陆按钮

chooseLoginNamespace = WebDriverWait(driver,2,0.3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".popup,.popup-confirm")))
# 选择登陆空间
platformTradeIDDropdown = Select(driver.find_element_by_tag_name("select"))
platformTradeIDDropdown.select_by_value("288572")

time.sleep(1)

chooseLoginNamespace.find_elements_by_css_selector(".btn,.btn-primary")[0].click()

# driver.close()



cookiesDict = {}

for item in cookies.getCurrentCookies(driver).split(";"):
    if item.split("=").__len__() > 1:
        cookiesDict[str.lstrip(item.split("=")[0])] = str.lstrip(item.split("=")[1].__str__())

print("\n" + colors.HEADER + "当前系统环境如下" + colors.ENDC)
print("浏览器版本:" + browserInfo.getCurrentBrowserInfo(driver))
print("\n" + colors.HEADER + "当前浏览器环境如下" + colors.ENDC)
print("浏览器窗口大小:" + windowInfo.getCurrentWindowInfoValue(driver))
print("\n" + colors.HEADER + "当前数据环境如下" + colors.ENDC)
print("ms_cid:" + cookiesDict["ms_cid"])
print("ms_member_token:" + cookiesDict["ms_member_token"])
print("\n" + colors.HEADER + "当前页面地址\n" + driver.current_url + colors.ENDC)

# if driver.window_handles.__len__() > 1:
#     driver.switch_to_window(driver.window_handles[1])
time.sleep(2)

driver.get("http://localhost:20019/")

try:
    # 进入【客户管理】模块
    userManager = WebDriverWait(driver, 2, 0.3).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "客户管理")))
    driver.find_element_by_link_text("客户管理").click()

    time.sleep(2)
    # 进入[添加商机]模块
    userManager = WebDriverWait(driver, 2, 0.3).until(
        EC.element_to_be_clickable((By.XPATH,"//button[@class='ant-btn ant-btn-primary ant-btn-round']/span[contains(text(),'添加商机')]/..")))
    userManager.click()

    # 测试添加商机模块
    # addOpportunity.stage.fillBasicInfo(driver,"C")
    addOpportunity.pipeAdd(driver,"C")

    time.sleep(2)

    # driver.find_elements_by_xpath(
    #     "//button[@class='ant-btn ant-btn-primary ant-btn-round']/span[contains(text(),'添加商机')]")
    # driver.quit()


except NoSuchElementException:
    print('NoSuchElementException 找不到元素')
    driver.quit()


# driver.quit()