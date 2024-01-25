import time

import selenium
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

import utils.xpath2location
from utils.xml_dealer import xml_dealer

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
    'chromedriverExecutableDir': 'D:/python/wx_test',
    'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'},
})

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)

# 打印当前界面的xml(小程序或者原生app) or html(小程序)
# print('xml')
# print(driver.page_source)


# 如果从安卓原生切换到小程序or小程序切换回来, 需要做用switch指令
# ['NATIVE_APP', 'WEBVIEW_com.tencent.mm', 'WEBVIEW_com.tencent.mm:appbrand0']
# print('after switch')

print('driver.contexts', driver.contexts)
print('driver.current_activity', driver.current_activity)
# 获取当前页面所有函数的源代码
# all_source_code = driver.execute_script("var dic = {}; for (var prop in wx) { if (typeof wx[prop] === 'function') { dic[prop]=wx[prop].toString(); } } return dic;")
# with open('source_code.json','w',encoding='utf8') as f:
#     json.dump(all_source_code,f,indent=4)
# ret_content = driver.execute_script("var dic = {}; for (var prop in wx) { if (typeof wx[prop] === 'function') { dic[prop]=wx[prop].bind().toString(); } } return dic;")
# callers = driver.execute_script("var dic = {}; for (var prop in wx) { if (typeof wx[prop] === 'function') { dic[prop]=wx[prop].caller.toString(); } } return dic;")
with open('main_page.xml','w',encoding='utf8') as f:
    f.write(driver.page_source)
my_xml_dealer = xml_dealer('main_page.xml')
xpath_list = my_xml_dealer.main()
xpath_list = utils.xpath2location.convert(xpath_list,driver)
driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
# Perform swipe gesture
start_x = 0  # starting x-coordinate
start_y = 1000  # starting y-coordinate
end_x = 200  # ending x-coordinate
end_y = 1000  # ending y-coordinate
duration_ms = 100  # duration of the swipe in milliseconds
# 在NATIVE_APP模式下获取所有的XPATH的坐标，并记录。

window_handlers = driver.window_handles
pre_page_handler = ''
for handler in window_handlers:
    print('cur handler',handler)
    driver_title = driver.title
    info = driver.execute_script(
        'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
    print(driver_title)
    print(info)
    print('----------------------')
    if driver_title.endswith(':VISIBLE') or driver_title.endswith(':VISIBLE(PAUSED)'):
        pre_page_handler = handler
        break
    driver.switch_to.window(handler)

    time.sleep(0.1)
pre_page = info
# print('pre_page',pre_page)
# print('pre_page_hash',pre_page)
# driver.find_element(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]').location
print('prepare to click!')
for xpath_location in xpath_list:
    print(xpath_location)
    go_pre_page = False
    camera_page = True
    # driver.tap([xpath_location])
    TouchAction(driver).tap(x=xpath_location[0], y=xpath_location[1]).perform()
    time.sleep(1)
    # 适配目前页面合适的handler
    # TODO 需要找到一个更合适的方法切换handler
    # TODO 有一些组件消失了
    change_to_visible = False
    for handler in driver.window_handles:
        print('cur handler', handler)
        try:
            info = driver.execute_script(
                'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
            print('info ', info)
        except selenium.common.exceptions.NoSuchWindowException:
            print('invalid target window')
            driver.switch_to.window(handler)
            time.sleep(0.1)
            continue
        if 'undefined' in info:
            driver.switch_to.window(handler)
            time.sleep(0.1)
            continue
        # else:
        driver_title = driver.title
        print('driver title ', driver_title)
        print('----------------------')
        if driver_title.endswith(':VISIBLE') or driver_title.endswith(':VISIBLE(PAUSED)'):
            change_to_visible = True
            break
        driver.switch_to.window(handler)
        time.sleep(0.1)
    if not change_to_visible:
        # 说明可能进入了相机页面
        print('press_keycode to exit camera.')
        driver.press_keycode(keycode=4)
        continue
    this_page = driver.execute_script(
        'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
    print('this page',this_page,' pre_page',pre_page)
    time.sleep(0.1)
    # print(f'pre_page{pre_page},this_page{this_page}')
    if pre_page != this_page:
        # driver.swipe(start_x,start_y,end_x,end_y,duration_ms)
        script = "wx.reLaunch({url:'" + pre_page + "'})"
        print('script to execute:' + script)
        print('--------------------------------------')
        driver.execute_script(script)
        driver.switch_to.window(pre_page_handler)
        time.sleep(1)
# 在混合模式下，看不到xml了。如果想要结合使用xml和wxml，可能需要在NATIVE APP模式和hybrid模式下来回切换
# 尝试通过xpath点击小程序
# location = driver.find_element(By.XPATH,'//android.view.View[@resource-id="root"]/android.view.View/android.view.View/android.view.View[2]/android.view.View[10]')
# driver.find_element(By.XPATH,'//android.view.View[@resource-id="root"]/android.view.View/android.view.View/android.view.View[2]/android.view.View[10]').click()

# print(f'location{location}')
# driver.tap(x = location['x'])
# print(callers)
# Close the session


driver.quit()
