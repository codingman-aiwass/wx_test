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
    # driver = Driver.get_instance().get_driver()
    driver = Driver().get_driver()
    driver.activate_app("com.tencent.mm")
    while len(driver.contexts) == 1:
        logger.info("There is only one context in wechat now,need to restart!")
        execute_cmd_with_timeout("adb shell am force-stop com.tencent.mm")
        # driver.terminate_app("com.tencent.mm")
        time.sleep(2)
        # driver = Driver.get_instance().get_driver()
        driver = Driver().get_driver()
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
        # 记录那些既没有VISIBLE页面也没有INVISIBLE(PAUSED)的界面
        self.undefined_pages = []
        # 记录当前页面的上一个界面的的URL和请求参数
        self.pre_page = None
        # 记录当前界面的上一个界面的driver.tile
        self.pre_driver_title = None
        # 保存页面队列，存放待点击页面的URL
        self.pages_to_be_traverse_future = set()


    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(Driver, "_instance"):
    #         Driver._instance = object.__new__(cls)
    #     return Driver._instance
    #
    # @classmethod
    # def get_instance(cls, *args, **kwargs):
    #     if not hasattr(Driver, '_instance'):
    #         Driver._instance = Driver(*args, **kwargs)
    #     return Driver._instance

    def get_driver(self):
        return self.driver

    def get_page_source(self):
        return self.driver.page_source[:]

    def switch_context_to_hybrid(self):
        self.driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
        # 切换到正确的handler
        if self.switch_window_handler_to_visible():
            logger.info("成功切换到正确handler")

    def switch_context_to_default(self):
        self.driver.switch_to.context('NATIVE_APP')

    def switch_window_handler_to_visible(self):
        cur_title = self.driver.title[:]
        logger.info(f"cur_title:{cur_title}")
        logger.info("current visible_url2handler")
        logger.info(self.visible_url2handler)
        if cur_title in self.visible_url2handler.keys():
            # 说明缓存中有合适的handler,直接切换
            self.driver.switch_to.window(self.visible_url2handler[cur_title])
            return True
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            title = self.driver.title
            cur_handle = self.driver.current_window_handle
            logger.info(f'title {title}')
            logger.info(f'cur_handle{cur_handle}')
            if title.endswith(':VISIBLE'):
                self.visible_url2handler[title[:]] = cur_handle[:]
                logger.info(f"{title},{cur_handle}")
                return True
        # 说明没有找到VISIBLE页面，这个页面是一个h5页面，不是webview
        # 那就切换到INVISIBLE(PAUSED)
        # 寻找INVISIBLE
        # 到缓存中查看
        logger.info('fail to find a visible handler')
        logger.info(f"cur_title:{cur_title}")
        if cur_title in self.invisible_url2handler.keys():
            # 说明缓存中有合适的handler,直接切换
            self.driver.switch_to.window(self.invisible_url2handler[cur_title])
            return True
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            title = self.driver.title
            cur_handle = self.driver.current_window_handle
            logger.info(f'title {title}')
            logger.info(f'cur_handle{cur_handle}')
            if title.endswith(':INVISIBLE(PAUSED)'):
                self.invisible_url2handler[cur_title[:]] = cur_handle[:]
                logger.info(f"{title},{cur_handle}")
                return True
        # 说明连invisible handler都找不到
        # TODO 记录这类页面
        return False
    def get_current_url_and_parameter(self):
        # 只能在切换成功window_handler以后才能通过获取js注入获取当前url和请求参数
        if self.switch_window_handler_to_visible():
            info = self.driver.execute_script(
            'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
            return info
        # 没有url
        return None

    def save_page_source_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(self.driver.page_source)

    # 检查当前所处界面和点击前的界面是否相同
    def check_if_same_to_page_before_click(self):
        # 通过判断点击前后界面的URL是否一致来判断
        cur_url = self.get_current_url_and_parameter()
        if cur_url is not None:
            return cur_url == self.pre_page
        # 当前界面不是webview界面,判断driver_title
        return self.pre_driver_title == self.driver.title[:]

    def click_xpath(self,xpath):
        try:
            logger.info(f'xpath to click: {xpath}')
            self.driver.find_element(By.XPATH,xpath).click()
        except Exception as e:
            logger.info('error occurred in click_xpath()')
            logger.exception(e)
    def refresh_driver(self):
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=self.options)


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
        logger.info("to_recent_used_page() done..")

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
        self.switch_context_to_hybrid()

        # 根据指定小程序ID跳转
        logger.info("wx.navigateToMiniProgram({appId:'" + app_id + "'})")
        self.driver.execute_script("wx.navigateToMiniProgram({appId:'" + app_id + "'})")

    # 测试下一个小程序之前，清除上一个小程序的缓存记录。
    def refresh_dic(self):
        self.visible_url2handler = {}



