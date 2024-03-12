# 测试通过位置信息权限申请页面
# 特点：只需要点击允许

# 查看url 为 /pages/recent/recent

from utils.DriverConfig import Driver
from appium.webdriver.common.touch_action import TouchAction

from utils.pre_main_checker import PreMainDealerXML
from utils.xpath2location import convert

# Driver.get_instance().switch_context_to_hybrid()
# driver = Driver.get_instance().get_driver()
# info = driver.execute_script(
#                 'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
# print(info)


dealer = PreMainDealerXML('../肯德基位置信息获取申请.xml')

pos = dealer.find_location_request_1()
print('pos', pos)
if pos is not None:
    driver = Driver.get_instance().get_driver()
    # 点击允许
    xpath_list = convert([pos], driver)
    for xpath in xpath_list:
        TouchAction(driver).tap(x=xpath[0], y=xpath[1]).perform()
