def getCurrentBrowserInfo(driver):
    """
    获取浏览器信息
    :param driver: 传入的浏览器对象
    """
    # print ("测试package及module")
    getCurrentBrowserInfo = "return window.navigator.appVersion"
    browserInfoValue = driver.execute_script(getCurrentBrowserInfo)
    return browserInfoValue