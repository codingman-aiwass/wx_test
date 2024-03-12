import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import logging
from utils import log_config
from utils.utils import execute_cmd_with_timeout

logger = logging.getLogger("my_app")


def check_status():
    # execute_cmd_with_timeout("adb shell am start -n com.tencent.mm/.ui.LauncherUI")
    driver = Driver.get_instance().get_driver()
    driver.activate_app("com.tencent.mm")
    while len(driver.contexts) == 1:
        logger.info("There is only one context in wechat now,need to restart!")
        execute_cmd_with_timeout("adb shell am force-stop com.tencent.mm")
        # driver.terminate_app("com.tencent.mm")
        time.sleep(2)
        driver = Driver.get_instance().get_driver()
        driver.activate_app("com.tencent.mm")
        # execute_cmd_with_timeout("adb shell am start -n com.tencent.mm/.ui.LauncherUI")
    logger.info("No need to restart wechat now.")


class Driver:
    def __init__(self):
        self.options = AppiumOptions()
        self.options.load_capabilities({
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
            # 'chromedriverExecutableDir': '~/czf_files/wx_test',
            'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'},
        })
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=self.options)
        # 记录当前小程序下visible页面的url和window_handler对应关系
        self.visible_url2handler = {}
        # 记录当前小程序invisible页面的url和window_handler对应关系
        self.invisible_url2handler = {}
        # 记录当前页面的上一个界面的的URL和请求参数
        self.pre_page = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(Driver, "_instance"):
            Driver._instance = object.__new__(cls)
        return Driver._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Driver, '_instance'):
            Driver._instance = Driver(*args, **kwargs)
        return Driver._instance

    def get_driver(self):
        return self.driver

    def refresh_driver(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=self.options)

    def switch_context_to_hybrid(self):
        self.driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')

    def switch_context_to_default(self):
        self.driver.switch_to.context('NATIVE_APP')

    def switch_window_handler_to_visible(self):
        window_handlers = self.driver.window_handles
        for handler in window_handlers:
            logger.info('cur handler', handler)
            driver_title = self.driver.title
            logger.info(driver_title)
            self.driver.switch_to.window(handler)
            if driver_title.endswith('html:VISIBLE') or driver_title.endswith(':VISIBLE(PAUSED)'):
                info = self.driver.execute_script(
                    'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
                logger.info(info)
                self.visible_url2handler[info[:]] = handler[:]
                return handler
        # 运行到此即为该页面没有visible handler，不是一个webview页面
        return None

    def save_page_source_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(self.driver.page_source)

    def to_recent_used_page(self):
        self.switch_context_to_default()
        self.driver.find_element(By.XPATH,
                                 '//android.widget.TextView[@resource-id="com.tencent.mm:id/icon_tv" and @text="发现"]').click()
        time.sleep(0.05)
        self.driver.find_element(By.XPATH,
                                 '//android.widget.TextView[@resource-id="android:id/title" and @text="小程序"]').click()
        time.sleep(3)
        # 点击完这一步以后，有可能已经直接进入了最近使用的界面，这个时候再通过bounds点击则会进入第一个小程序
        # 暂时使用bounds来点击 [66,294][231,352] ，更通用的CV方法以后再说
        action = TouchAction(self.driver)
        action.tap(x=(66 + 231) // 2, y=(294 + 352) // 2).perform()
        time.sleep(3)
        # 通过检查当前activity判断是否在小程序中
        if self.driver.current_activity[:] != '.plugin.appbrand.ui.AppBrandPluginUI':
            self.driver.back()

    def perform_swipe_operation(self,start_x,start_y,end_x,end_y,duration_ms):
        TouchAction(self.driver).press(x=start_x, y=start_y).wait(duration_ms).move_to(x=end_x, y=end_y).release().perform()
    def perform_swipe_from_left_to_center(self):
        # 从屏幕边缘往中间滑
        start_x = 0  # starting x-coordinate
        start_y = 1000  # starting y-coordinate
        end_x = 200  # ending x-coordinate
        end_y = 1000  # ending y-coordinate
        duration_ms = 100  # duration of the swipe in milliseconds
        TouchAction(self.driver).press(x=start_x, y=start_y).wait(duration_ms).move_to(x=end_x, y=end_y).release().perform()


    def to_configured_mini_program(self, app_id):
        # 根据指定小程序ID跳转
        self.driver.execute_script("wx.navigateToMiniProgram({appId:'" + app_id + "'})")



