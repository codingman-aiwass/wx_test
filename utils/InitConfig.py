from appium import webdriver
from appium.options.common.base import AppiumOptions


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
            'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'},
        })
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=self.options)

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

    def switch_context_to_hybrid(self):
        self.driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')

    def switch_context_to_default(self):
        self.driver.switch_to.context('NATIVE_APP')

    def switch_window_handler_to_visible(self):
        window_handlers = self.driver.window_handles
        for handler in window_handlers:
            print('cur handler', handler)
            driver_title = self.driver.title
            print(driver_title)
            self.driver.switch_to.window(handler)
            if driver_title.endswith('html:VISIBLE'):
                info = self.driver.execute_script(
                    'return window.__route__+".html" + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
                print(info)
                break

    def save_page_source_to_file(self,file_name):
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(self.driver.page_source)
