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

# 打印当前上下文
print('上下文')
print(driver.contexts)

# 如果从安卓原生切换到小程序or小程序切换回来, 需要做用switch指令
# ['NATIVE_APP', 'WEBVIEW_com.tencent.mm', 'WEBVIEW_com.tencent.mm:appbrand0']
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
xpath_list = utils.xpath2location.convert(xpath_list,driver)
driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
# Perform swipe gesture
start_x = 0  # starting x-coordinate
start_y = 1000  # starting y-coordinate
end_x = 200  # ending x-coordinate
end_y = 1000  # ending y-coordinate
duration_ms = 100  # duration of the swipe in milliseconds
# 在NATIVE_APP模式下获取所有的XPATH的坐标，并记录。

# 在判断是否点到了一个新界面，利用界面的hash判断是否前后两个页面一致
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
    time.sleep(2)
    # 适配目前页面合适的handler
    # TODO 进入相机界面后无法跳出
    # TODO 在菜鸟裹裹的寄件抽奖活动页面使用js注入失败
    # TODO 在某些页面遍历 driver.window_handles时，可能会在执行 new_driver_title = driver.title 的时候抛出selenium.common.exceptions.NoSuchWindowException: Message: no such window: target window already closed from unknown error: web view not found
    for handler in driver.window_handles:
        print('cur handler in new page', handler)
        try:
            new_driver_title = driver.title
        except selenium.common.exceptions.NoSuchWindowException:
            # 直接跳回上一界面
            print('jump to last UI directly')
            go_pre_page = True

        if go_pre_page:
            script = "wx.reLaunch({url:'" + pre_page + "'})"
            # TODO 进入相机界面后可能跳到这里，出现的报错信息为 selenium.common.exceptions.NoSuchWindowException: Message: no such window: target window already closed
            driver.execute_script(script)
            driver.switch_to.window(pre_page_handler)
            continue

        new_info = driver.execute_script(
            'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
        print('new page driver_title',new_driver_title)
        print('new page url',new_info)
        print('----------------------')
        if new_driver_title.endswith(':VISIBLE') or new_driver_title.endswith(':VISIBLE(PAUSED)'):
            pre_page_handler = handler
            camera_page = False
            break
        try:
            driver.switch_to.window(handler)
            time.sleep(0.1)
        except selenium.common.exceptions.NoSuchWindowException:
            print('Message: no such window,skip..')
    # 如果遍历了所有的window handler也没有找到合适的，说明可能在相机界面
    # 使用原先的滑动方式回到上个界面
    # TODO 滑动退出在hybrid模式下会出现报错
    if camera_page:
        print('swipe to go back!')
        driver.switch_to.context('NATIVE_APP')
        driver.swipe(start_x, start_y, end_x, end_y, duration_ms)
        driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
        # touch_action = TouchAction(driver)
        # touch_action.tap(x=start_x, y=start_y) \
        #     .wait(100) \
        #     .move_to(x=end_x, y=end_y) \
        #     .release() \
        #     .perform()
        continue

    if go_pre_page:
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
    # except Exception as e:
    #     print(e.args)
    #     print(f'skip {xpath_location}')
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
