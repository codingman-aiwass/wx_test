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
    # 'chromedriverExecutableDir': 'D:/python/wx_test',
    'chromedriverExecutableDir': '~/czf_files/wx_test',
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

# 第一次尝试，先获取页面xml并判断是否有隐私政策界面/权限请求页面/弹窗/首页广告
# 如果有的话，就要先想办法点击掉这些，然后再获取一次首页
# 弹窗检测：检测到特定的class或者出现了指定关键词直接关闭弹窗（菜鸟：点击关注）或者 根据bounds的坐标或者z-index，发现是否有组件覆盖到其他组件上，有的话说明这个组件是弹窗
# TODO 在NATIVE APP模式，可能没法检测到弹窗的存在。在appium inspector中是通过切换了hybrid模式以后再获取xml源码才拿到带弹窗的xml。不知如何在代码中实现
# 权限请求页面：属于平台自身。信息申请、跳转、提示框等类型，在官方手册都会有说明
# 首页广告：应该会有一个跳过按钮，点击即可
# 隐私政策界面：应该会有 隐私 字样或者同意按钮，点击即可.根据是否存在android.widget.TextView并且其text属性含有隐私xx字样。同意的属性为android.view.View，含有子属性 android.widget.TextView。通过点击同意跳过

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
    # TODO 菜鸟的最底下几个组件的坐标消失了，没能点击到。但是麦当劳的可以点击到，有些页面比较长，按照目前的策略无法点击到
    # TODO 有两种弹窗需要处理，一种是微信平台的弹窗，比如权限弹窗，通知弹窗，原生弹窗；另一种是小程序的广告弹窗
    # TODO 需要处理最开始进入小程序时，同意隐私政策的情况
    # TODO 在批量遍历小程序时，需要考虑如何自动化进入需要遍历的小程序。通过wx.nativateToMiniProgram还需要我们手动点击确认，
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
        # 但是也有可能是进入了某个页面，这个页面也只有INVISIBLE，和相机表现一致，但是不是相机
        print('press_keycode to exit camera.')
        driver.press_keycode(keycode=4)
        print('current activity after press keycode',driver.current_activity)
        if not driver.current_activity[:].startswith('.plugin.appbrand.ui.AppBrandUI0'):
            # 需要回到刚才的小程序,有两种方法，一种通过xpath点击，一种通过wx.navigateToMiniProgram()跳转,但是效果不好
            print('go back to miniapp!')
            print('current activity',driver.current_activity)
            # 方法1，xpath
            back_xpath_location = '//android.webkit.WebView[@text="wxb6d22f922f37b35a:pages/recent/recent.html:VISIBLE"]/android.view.View/android.view.View[4]/android.view.View/android.view.View/android.view.View[1]'
            driver.switch_to.context('NATIVE_APP')
            driver.find_element(By.XPATH, back_xpath_location).click()
            driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
            # 方法2，wx.navigateToMiniProgram()
            # driver.execute_script("wx.navigateToMiniProgram({appId:'wx25f982a55e60a540'})")  # 麦

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
