#encoding =utf-8
import random
import time
from selenium import webdriver

driver = webdriver.Chrome()

driver.set_window_size(1400, 800)

driver.get('http://testlogin.viphrm.com/')

print("loading finished")

# driver.quit()