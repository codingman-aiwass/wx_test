# convert xpath to location in screen
import selenium.common.exceptions
from selenium.webdriver.common.by import By


def convert(xpath_set, driver) -> list:
    # 参数为xpath集合和driver
    # driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
    location_set = set()
    for xpath_location in xpath_set:
        # print('xpath_location',xpath_location)
        try:
            location = driver.find_element(By.XPATH, xpath_location).location
            location_set.add(tuple((location['x'], location['y'])))
        except selenium.common.exceptions.NoSuchElementException:
            print('skip ',xpath_location)
    return location_set
