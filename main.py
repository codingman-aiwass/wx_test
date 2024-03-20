import time

from selenium.webdriver.common.by import By

from utils.DriverConfig import Driver, check_status
from utils.pre_main_checker import PreMainDealerXML, PreMainDealerWebview, get_login_popup_xpath

import logging

logger = logging.getLogger("my_app")
my_driver = Driver()

if __name__ == '__main__':
    # 检查微信目前是否只有NATIVE_APP模式
    logger.info("execute check_status()")
    check_status()
    # 跳转到小程序-最近使用页面，但是UIAutomator有时候会崩溃，这个方法不稳定，干脆手动点进去好了
    # logger.info("execute to_recent_used_page()")
    # my_driver.to_recent_used_page()

    # 开始跳转小程序
    app_id = 'wx795bd500b21f8fee'
    logger.info("准备进入指定小程序")
    my_driver.to_configured_mini_program(app_id)
    # 等待5s，等广告跳过
    time.sleep(10)
    # 判断是否有隐私政策页面
    # 先获取当前页面xml
    logger.info("准备获取xml源码")
    my_driver.refresh_driver()
    my_driver.switch_context_to_default()
    logger.info(my_driver.get_driver().current_context)
    xml_dealer = PreMainDealerXML(my_driver.get_driver().page_source[:].encode('utf-8'))
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
        html_content = my_driver.driver.page_source[:]
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
    xml_content = my_driver.driver.page_source[:]
    xml_dealer = PreMainDealerXML(xml_content.encode('utf-8'))
    location_agree_button_to_click = xml_dealer.find_location_request_1()
    if location_agree_button_to_click is not None:
        logger.info("在xml找到位置权限请求")
        my_driver.click_xpath(location_agree_button_to_click)
    time.sleep(1)
    # 接下来需要判断是否有弹窗，如果没有弹窗，就说明进入了主页面
    my_driver.switch_context_to_hybrid()
    html_dealer = PreMainDealerWebview(my_driver.driver.page_source[:])
    close_icon_info = []
    html_dealer.get_component_by_class_name(['close'],html_dealer.tree,close_icon_info)
    close_icon_xpath_list = html_dealer.deal_with_close_icon(close_icon_info)
    if len(close_icon_xpath_list) > 0:
        logger.info('发现该界面有广告弹窗，准备点击')
        for xpath in close_icon_xpath_list:
            my_driver.click_xpath(xpath)
    else:
        logger.info("未发现该界面有广告弹窗")
    # 进入主页面以后，但是此时仍然是未登录状态，还需要查找页面上是否有登录按钮，有的话点击
    html_dealer = PreMainDealerWebview(my_driver.driver.page_source[:])
    # to_login_button_info = []
    # html_dealer.get_to_login_button_info_in_main_page(html_dealer.tree,to_login_button_info)
    # to_login_buttons = html_dealer.deal_with_agree_button_info(to_login_button_info)
    to_login_buttons = html_dealer.get_to_login_button_xpath()
    if len(to_login_buttons) > 0:
        logger.info('在小程序主页找到登录按钮')
        for xpath in to_login_buttons:
            my_driver.click_xpath(xpath)
            time.sleep(3)
            # 此时必须调用switch_context_to_hybrid(),因为登录界面是一个新的webview，不切换的话driver还在上一个webview里
            my_driver.switch_context_to_hybrid()
            logger.info(my_driver.driver.title)
            html_dealer = PreMainDealerWebview(my_driver.driver.page_source[:])
            # 处理登录界面，此时点击了checkbox和快速登录按钮
            login_buttons = html_dealer.get_login_button_xpath()
            logger.info(f'login_buttons: {login_buttons}')
            for xpath_ in login_buttons:
                my_driver.click_xpath(xpath_)
                time.sleep(0.1)
            time.sleep(3)
            if False:
                pass
                # TODO 在这里，有可能弹出来登录请求框要求点击 使用微信绑定手机号登录，也有可能进入手机验证登录页面，需要做一个判断
                # 可以通过这个页面有没有 获取验证码 发送验证码 接受验证码 来进行初步判断（xpath） //android.widget.TextView
                # 有的话进行下三步操作
                # 然后通过 手机号 定位 class="android.widget.EditText" text 含有 手机号，长按粘贴手机号
                # 然后通过 验证码 定位 class="android.widget.EditText" text 含有 验证码
                # 然后点击登录 或者 注册登录 按钮
                # print(driver.find_element(By.XPATH, "//android.widget.EditText[contains(@text, '手机号')]").location)
                # print(driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, '验证码')]").location)
                # print(driver.find_element(By.XPATH, "//android.widget.EditText[contains(@text, '验证码')]").location)
                # 然后点击登录按钮即可登录。
                # TODO 但是这里有一个问题，有些小程序在手机验证登录页面上的的选择框的底层实现不是用的checkbox，目前不知该如何定位这个组件
            else:
                pass
                # 如果不是上面那种情况，就直接处理弹出来登录请求框,要求点击 使用微信绑定手机号登录 ,这个需要在NATIVE_APP模式下进行
                my_driver.switch_context_to_default()
                login_popup_xpath_list = get_login_popup_xpath()
                for popup_xpath in login_popup_xpath_list:
                    my_driver.click_xpath(popup_xpath)
                # TODO 在这里还要检查一下会不会出现隐私政策，因为有的小程序的隐私政策是在登录的时候出现
    else:
        logger.info('在小程序主页没有找到登录按钮')
    # 进入小程序首页，如果没有进入登录页面，先点击我的，尝试触发找到登录相关字样。并进行登录
    # 如果已经登录过了，也先点击一下我的，尝试触发 消息发送权限请求弹窗并处理掉

    # 然后再开始进行正常的首页点击











