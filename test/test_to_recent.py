# 第一个要点击的 xpath //android.widget.TextView[@resource-id="com.tencent.mm:id/icon_tv" and @text="发现"]
# 第二个要点击的 xpath //android.widget.TextView[@resource-id="android:id/title" and @text="小程序"]
# 第三个要点击的 xpath //android.view.View[@content-desc="最近使用"]
# 第三个页面为webview，无法获取到xpath
import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from utils.DriverConfig import Driver

Driver.get_instance().switch_context_to_default()
driver = Driver.get_instance().get_driver()
driver.find_element(By.XPATH,
                    '//android.widget.TextView[@resource-id="com.tencent.mm:id/icon_tv" and @text="发现"]').click()
time.sleep(0.05)
driver.find_element(By.XPATH, '//android.widget.TextView[@resource-id="android:id/title" and @text="小程序"]').click()
time.sleep(1)
# 暂时使用bounds来点击 [66,294][231,352] ，更通用的CV方法以后再说
action = TouchAction(driver)
action.tap(x=(66 + 231) // 2, y=(294 + 352) // 2).perform()
