def getCurrentWindowInfoValue(driver):
    """
    获取页面信息
    :param driver: 传入的浏览器对象
    """
    getCurrentWindowInfo = "return document.body.offsetWidth + ' * ' + document.body.offsetHeight "
    getCurrentWindowInfoValue = driver.execute_script(getCurrentWindowInfo)
    return getCurrentWindowInfoValue