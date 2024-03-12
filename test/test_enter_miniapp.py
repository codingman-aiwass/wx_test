from selenium.webdriver.common.by import By

from utils.DriverConfig import Driver

driver = Driver.get_instance().get_driver()
print(driver.contexts)
print('activity before back',driver.current_activity)
driver.back()
print('activity after back',driver.current_activity)

xpath_location = '//android.webkit.WebView[@text="wxb6d22f922f37b35a:pages/recent/recent.html:VISIBLE"]/android.view.View/android.view.View[4]/android.view.View/android.view.View/android.view.View[1]'
driver.find_element(By.XPATH,xpath_location).click()
