import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from utils.xpath2location import convert
from utils.pre_main_checker import PreMainDealerXML
from utils.DriverConfig import Driver
dealer = PreMainDealerXML('顺丰招聘隐私政策.xml')

pp_pass_xpath = dealer.get_pp_checkbox_agreebutton_xpath()
Driver.get_instance().switch_context_to_default()
driver = Driver.get_instance().get_driver()
# 点击掉隐私政策界面
# xpath_list = convert(pp_pass_xpath,driver)
print(pp_pass_xpath)
for xpath in pp_pass_xpath:
    # TouchAction(driver).tap(x=xpath[0], y=xpath[1]).perform()
    driver.find_element(by=By.XPATH, value=xpath).click()
    time.sleep(0.4)
