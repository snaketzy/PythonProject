def getCurrentCookies(driver):
    """
    获取站点信息
    :param driver: 传入的浏览器对象
    """
    getCurrentCookies = "return document.cookie"
    cookiesValue = driver.execute_script(getCurrentCookies)
    return cookiesValue