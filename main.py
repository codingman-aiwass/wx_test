import time

from utils.DriverConfig import Driver, check_status
from utils.pre_main_checker import PreMainDealerXML, PreMainDealerWebview

import logging

logger = logging.getLogger("my_app")

if __name__ == '__main__':
    logger.info("execute check_status()")
    check_status()
    my_driver = Driver()
    logger.info("execute to_recent_used_page()")
    my_driver.to_recent_used_page()
    # 开始跳转小程序
    app_id = 'wx08ee7f7d36a2eff8'
    logger.info("准备进入指定小程序")
    my_driver.to_configured_mini_program(app_id)
    # 等待5s，等广告跳过
    time.sleep(9)
    # 判断是否有隐私政策页面
    # 先获取当前页面xml
    logger.info("准备获取xml源码")
    my_driver.refresh_driver()
    my_driver.switch_context_to_default()
    logger.info(my_driver.get_driver().current_context)
    xml_content = my_driver.get_page_source()
    xml_dealer = PreMainDealerXML(xml_content.encode('utf-8'))
    pp_to_click_xpath = xml_dealer.get_pp_checkbox_agreebutton_xpath()
    if len(pp_to_click_xpath) > 0:
        logger.info("在xml找到隐私政策页面以及同意按钮")
        for xpath in pp_to_click_xpath:
            my_driver.click_xpath(xpath)
    else:
        logger.info("未在xml找到隐私政策页面以及同意按钮")
        # 再获取webview页面查看隐私政策是否存放在webview里
        logger.info("准备获取html源码")
        my_driver.switch_context_to_hybrid()
        html_content = my_driver.get_page_source()
        # print(html_content)
        html_dealer = PreMainDealerWebview(html_content.encode('utf-8'))
        pp_to_click_xpath = html_dealer.get_agree_button_xpath()
        if len(pp_to_click_xpath) > 0:
            logger.info("在webview中找到隐私政策页面以及同意按钮")
            for xpath in pp_to_click_xpath:
                # Driver.get_instance().click_xpath(xpath)
                my_driver.click_xpath(xpath)
        else:
            logger.info("未在webview找到隐私政策页面以及同意按钮")
    # 防止进入小程序一会儿以后，位置权限请求框才出现。这样的话获取到的XML里就会没有位置权限请求信息
    time.sleep(4)
    # 判断是否有位置信息请求
    my_driver.switch_context_to_default()
    xml_content = my_driver.get_page_source()
    xml_dealer = PreMainDealerXML(xml_content.encode('utf-8'))
    location_agree_button_to_click = xml_dealer.find_location_request_1()
    if location_agree_button_to_click is not None:
        logger.info("在xml找到位置权限请求")
        my_driver.click_xpath(location_agree_button_to_click)










