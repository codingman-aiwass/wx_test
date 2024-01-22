import json
import time
import traceback

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from xml_dealer import xml_dealer
import re
from urllib.parse import urlparse, parse_qs
options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:platformVersion": '12',
    "appium:deviceName": "xxx",
    "appium:appPackage": "com.tencent.mm",
    "appium:appActivity": ".ui.LauncherUI",
    "appium:unicodeKeyboard": True,
    "appium:resetKeyboard": True,
    "appium:noReset": True,
    "appium:newCommandTimeout": 6000,
    "appium:automationName": "uiautomator2",
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:connectHardwareKeyboard": True,
    "appium:printPageSourceOnFindFailure": True,
    'chromedriverExecutableDir': 'D:/python/wx_test/',
    'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'},
})

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)


# 打印当前上下文
print('上下文')
print(driver.contexts)
# window handler
# 如果从安卓原生切换到小程序or小程序切换回来, 需要做用switch指令
# ['NATIVE_APP', 'WEBVIEW_com.tencent.mm', 'WEBVIEW_com.tencent.mm:appbrand0']
driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
# print('after switch')
# product/pages/mccafe/index.html
# product/pages/list/index.html
window_handlers = driver.window_handles
print(window_handlers)
for handler in window_handlers:
    print('cur handler',handler)
    driver_title = driver.title
    print(driver_title)
    driver.switch_to.window(handler)
    if driver_title.endswith('html:VISIBLE'):
        info = driver.execute_script('return window.__route__+".html" + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
        print(info)
        break
# Close the driver
# pages/wechat-portal/index.html
# 首页菜鸟 pages/user/index.html
driver.execute_script('wx.navigateBack()')
# ret = driver.execute_script('wx.navigateTo({url:"/pages/user/index"},success(){return "success"},fail(){return "fail"});')
# print(ret)
# driver.execute_script('wx.navigateBack()')
driver.quit()