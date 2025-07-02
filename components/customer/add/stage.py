import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def fillBasicInfo(driver, stageName):
    """
    填充基本信息
    """

    # 客户名称
    opportunityName = driver.find_element_by_xpath("//input[@id= 'opportunityName']")
    opportunityName.send_keys("测试公司")

    # 客户阶段
    stageIdDropdown = driver.find_element_by_xpath("//div[@id='stageId']")
    stageIdDropdownControl = stageIdDropdown.find_element_by_css_selector(
        ".ant-select-selection,.ant-select-selection--single")
    stageIdControlValue = stageIdDropdownControl.get_attribute("aria-controls")
    stageIdDropdown.click()
    time.sleep(1)

    stageIdDropdownListContainer = driver.find_element_by_id(stageIdControlValue)

    stageIdDropdownList = stageIdDropdownListContainer.find_elements_by_tag_name("li")

    # 在客户阶段下拉菜单中选择传入的阶段
    # random.choice(stageIdDropdownList).click()
    for k in stageIdDropdownList:
        if (k.get_attribute("title") == stageName):
            k.click()

    return opportunityName


