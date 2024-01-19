import json
import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from xml_dealer import xml_dealer

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
    'chromedriverExecutableDir': 'D:/python/wx_miniapp01/',
    'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'},
})

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)

# 打印当前界面的xml(小程序或者原生app) or html(小程序)
# print('xml')
# print(driver.page_source)

# 打印当前上下文
print('上下文')
print(driver.contexts)

# 如果从安卓原生切换到小程序or小程序切换回来, 需要做用switch指令
# ['NATIVE_APP', 'WEBVIEW_com.tencent.mm', 'WEBVIEW_com.tencent.mm:appbrand0']
# driver.switch_to.context(u'WEBVIEW_com.tencent.mm:appbrand0')
# print('after switch')

print('driver.contexts', driver.contexts)
print('driver.current_activity', driver.current_activity)
# print(driver.page_source)
# 点击
# driver.find_element("xpath", '//android.view.View[@resource-id="search_result"]/android.view.View[2]/android.view.View[2]').click()
# driver.implicitly_wait(3)

# Find all clickable elements on the screen
# clickable_elements = driver.find_elements("new UiSelector().clickable(true)")
# elements = driver.find_elements(By.XPATH, "//*[@bindTap]")
# elements = driver.find_elements(By.
# print(driver.current_url)
# 获取当前页面所有函数的源代码
# all_source_code = driver.execute_script("var dic = {}; for (var prop in wx) { if (typeof wx[prop] === 'function') { dic[prop]=wx[prop].toString(); } } return dic;")
# with open('source_code.json','w',encoding='utf8') as f:
#     json.dump(all_source_code,f,indent=4)
# ret_content = driver.execute_script("var dic = {}; for (var prop in wx) { if (typeof wx[prop] === 'function') { dic[prop]=wx[prop].bind().toString(); } } return dic;")
# callers = driver.execute_script("var dic = {}; for (var prop in wx) { if (typeof wx[prop] === 'function') { dic[prop]=wx[prop].caller.toString(); } } return dic;")
# print(all_source_code)
# print(driver.page_source)
with open('main_page.xml','w',encoding='utf8') as f:
    f.write(driver.page_source)
my_xml_dealer = xml_dealer('main_page.xml')
xpath_list = my_xml_dealer.main()
# Perform swipe gesture
start_x = 0  # starting x-coordinate
start_y = 1000  # starting y-coordinate
end_x = 200  # ending x-coordinate
end_y = 1000  # ending y-coordinate
duration_ms = 100  # duration of the swipe in milliseconds
# 在NATIVE_APP模式下获取所有的XPATH的坐标，并记录。

# 在判断是否点到了一个新界面，利用界面的hash判断是否前后两个页面一致
pre_page_hash = hash(driver.page_source[:])
print('pre_page_hash',pre_page_hash)

for xpath_location in xpath_list:
    driver.find_element(By.XPATH,xpath_location).click()
    time.sleep(1)
    this_page_hash = hash(driver.page_source[:])
    print('this_page_hash',this_page_hash,'xpath_location',xpath_location)
    if pre_page_hash != this_page_hash:
        driver.swipe(start_x,start_y,end_x,end_y,duration_ms)
# bounds = driver.find_element(By.XPATH,'//android.view.View[@text="可横向滚动"]').get_attribute("bounds")
# print(bounds)
# print(type(bounds))
# driver.switch_to.context(u'WEBVIEW_com.tencent.mm:appbrand0')
# print(driver.current_url)
# driver.tap([(100,100)],duration=10) # work in NATIVE_APP
# action = TouchAction(driver)
# action.tap(x=800, y=1500).perform()
# time.sleep(2)
# print(driver.current_url)
# https://servicewechat.com/wxb6d22f922f37b35a/297/page-frame.html 首页

# Native App模式下，
# 有个//android.webkit.WebView[@text="wx795bd500b21f8fee:pages/index/index.html:VISIBLE"]，是页面的最顶端
# 然后就是代表root 结点的xpath (//android.view.View[@resource-id="root"])[1]
# 再接下来就是<android.view.View> 最底层的<android.view.View>里面应该会有实际可点击的组件。一般真正可点击的这类组件，他们的下面都可能还有多个子组件，但是这些子组件不会再有子组件了
# 带有字的组件的xpath //android.widget.TextView[@text="订单"]
# 一个思路，寻找所有带有android.widget.TextView[@text=""]，且@text里的内容长度不多于多少。

# 在混合模式下，看不到xml了。如果想要结合使用xml和wxml，可能需要在NATIVE APP模式和hybrid模式下来回切换
# 尝试通过xpath点击小程序
# location = driver.find_element(By.XPATH,'//android.view.View[@resource-id="root"]/android.view.View/android.view.View/android.view.View[2]/android.view.View[10]')
# driver.find_element(By.XPATH,'//android.view.View[@resource-id="root"]/android.view.View/android.view.View/android.view.View[2]/android.view.View[10]').click()

# print(f'location{location}')
# driver.tap(x = location['x'])
# print(callers)
# Close the session


driver.quit()
