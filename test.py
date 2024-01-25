import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.touch_action import TouchAction

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
change_to_visible = False
# 原有策略
# for handler in window_handlers:
#     print('cur handler',handler)
#     driver_title = driver.title
#     info = driver.execute_script(
#         'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
#     print('driver title ',driver_title)
#     print('info ',info)
#     print('----------------------')
#     if driver_title.endswith(':VISIBLE') or driver_title.endswith(':VISIBLE(PAUSED)'):
#         change_to_visible = True
#         break
#     driver.switch_to.window(handler)
#     time.sleep(0.1)

# 新策略
for handler in window_handlers:
    print('cur handler',handler)
    info = driver.execute_script(
        'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
    print('info ',info)
    if 'undefined' in info:
        driver.switch_to.window(handler)
        time.sleep(0.1)
    else:
        driver_title = driver.title
        print('driver title ',driver_title)
        print('----------------------')
        if driver_title.endswith(':VISIBLE') or driver_title.endswith(':VISIBLE(PAUSED)'):
            change_to_visible = True
            break
        driver.switch_to.window(handler)


if not change_to_visible:
    print('find no visible handler, find invisible one.')
    for handler in window_handlers:
        print('cur handler', handler)
        driver_title = driver.title
        info = driver.execute_script(
            'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
        print('driver title ', driver_title)
        print('info ', info)
        print('----------------------')
        if(info[1:] in driver_title):
            print('find invisible html window handler')
            break
        driver.switch_to.window(handler)
        time.sleep(0.1)

# Close the driver
#
# 首页菜鸟 pages/wechat-portal/index.html
# 菜鸟订单页面 pages/wechat-portal/index.html
# driver.execute_script('wx.navigateBack()')
# driver.execute_script("wx.reLaunch({url:'/pages/wechat-portal/index'})")
# driver.execute_script("wx.navigateTo({url:'/pages/index/index?activeMenu=2&source=wechat_portal'})")
# Perform swipe gesture
# start_x = 0  # starting x-coordinate
# start_y = 1000  # starting y-coordinate
# end_x = 200  # ending x-coordinate
# end_y = 1000  # ending y-coordinate
# duration_ms = 100  # duration of the swipe in milliseconds
# touch_action = TouchAction(driver)
# touch_action.press(x=start_x, y=start_y) \
#     .wait(100) \
#     .move_to(x=end_x, y=end_y) \
#     .release() \
#     .perform()
# driver.execute_script('wx.reLaunch("/pages/wechat-portal/index")')
# 小程序的相机界面应该都是类似的，可以通过xpath找到关闭按钮，//android.widget.ImageView[@content-desc="关闭"]
# 也可以直接press_keycode
# driver.press_keycode(keycode=4)
driver.quit()
