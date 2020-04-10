#encoding =utf-8
import random
import ssl
import time
import urllib.request
import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

driver = webdriver.Chrome()
# driver.maximize_window()
driver.set_window_size(1400, 800)

driver.get('http://testlogin.viphrm.com/')
# driver.fullscreen_window()
elem_user = driver.find_element_by_name("userName")
elem_user.send_keys("11657892036")
elem_pwd = driver.find_element_by_name("password")
elem_pwd.send_keys("wz123456")
driver.find_element_by_xpath("//button[@class='btn btn-block btn-primary']").click() #登陆按钮
time.sleep(1)


appList = driver.find_elements_by_class_name("ant-col-4")
if appList:
    # print("按钮文本:" + appList[6].text + "\n")
    appList[6].click()  #选择工薪记应用

driver.get('https://pregongxj.viphrm.com/maker/project/list')
# context = ssl._create_unverified_context()
# res = urllib.request.urlopen('https://pregongxj.viphrm.com/maker/project/list', context = context)
# response = requests.get("https://pregongxj.viphrm.com/maker/project/list")

time.sleep(1)

# 通过JS直接获取系统cookie
getCurrentCookies = "return document.cookie"
getCurrentBrowserInfo = "return window.navigator.appVersion"
getCurrentWindowInfo = "return document.body.offsetWidth + ' * ' + document.body.offsetHeight "
cookiesValue = driver.execute_script(getCurrentCookies)
browserInfoValue = driver.execute_script(getCurrentBrowserInfo)
getCurrentWindowInfoValue = driver.execute_script(getCurrentWindowInfo)

cookiesDict = {}

for item in cookiesValue.split(";"):
    if item.split("=").__len__() > 1:
        cookiesDict[str.lstrip(item.split("=")[0])] = str.lstrip(item.split("=")[1].__str__())

print("\n" +colors.HEADER+ "当前系统环境如下" +colors.ENDC)
print("浏览器版本:" + browserInfoValue)
print("\n" +colors.HEADER+ "当前浏览器环境如下" +colors.ENDC)
print("浏览器窗口大小:" + getCurrentWindowInfoValue)
print("\n" +colors.HEADER+ "当前数据环境如下" +colors.ENDC)
print("ms_cid:" + cookiesDict["ms_cid"])
print("ms_member_token:" + cookiesDict["ms_member_token"])
print("\n" +colors.HEADER+ "当前页面地址\n" +driver.current_url +colors.ENDC)

try:
    # button = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((driver.find_element_by_css_selector(".ant-btn,.ant-btn-primary,.ant-btn-round"))))
    clickableButton = driver.find_element_by_css_selector(".ant-btn,.ant-btn-primary,.ant-btn-round > span")

    driver.switch_to_window(driver.window_handles[0])
    time.sleep(1)
    # print("按钮文本:" + clickableButton.text)
    clickableButton.click()
    time.sleep(1)

    step1ProjectName = driver.find_element_by_xpath("//span[@data-offset-key]")
    step1ProjectName.send_keys("测试数据")

    # 触发blur事件实现对input的规则校验
    ActionChains(driver).context_click(driver.find_element_by_css_selector(".ant-btn,.ant-btn-primary,.ant-btn-round > span")).perform()

    # 项目类型
    platformTradeIDDropdown = driver.find_element_by_id("platformTradeID")
    platformTradeIDDropdownControl = platformTradeIDDropdown.find_element_by_css_selector(".ant-select-selection,.ant-select-selection--single")
    platformTradeIDDropdownControlValue = platformTradeIDDropdownControl.get_attribute("aria-controls")

    platformTradeIDDropdown.click()
    time.sleep(1)

    # 项目类型下拉菜单列表
    platformTradeIDDropdownListContainer = driver.find_element_by_id(platformTradeIDDropdownControlValue)

    platformTradeIDDropdownList = platformTradeIDDropdownListContainer.find_elements_by_tag_name("li")
    # 在项目类型下拉菜单中随机选择一个项
    random.choice(platformTradeIDDropdownList).click()

    # 类型职位
    platformPositionIDDropdown = driver.find_element_by_id("platformTradeID")

    time.sleep(1)
    driver.quit()


except NoSuchElementException:
    print('NoSuchElementException 找不到元素')
    time.sleep(2)
    driver.quit()


# driver.quit()