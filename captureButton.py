#encoding =utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
time.sleep(2)
appList = driver.find_elements_by_class_name("ant-col-4")
if appList:
    print("按钮文本:" + appList[6].text)
    appList[6].click()  #选择工薪记应用

driver.get('https://pregongxj.viphrm.com/maker/project/list')

try:
    # button = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((driver.find_element_by_css_selector(".ant-btn,.ant-btn-primary,.ant-btn-round"))))
    clickableButton = driver.find_element_by_css_selector(".ant-btn,.ant-btn-primary,.ant-btn-round > span")

    driver.switch_to_window(driver.window_handles[0])
    time.sleep(1)
    print("按钮文本:" + clickableButton.text)
    clickableButton.click()
    time.sleep(3)
    driver.quit()
except NoSuchElementException:
    print('NoSuchElementException')


# driver.quit()