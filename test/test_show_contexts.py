# 测试输出当前界面拥有的所有context，URL 以及请求参数
# 想要输出正确的page_source或者执行js注入，需要处于正确的contexts以及window_handler
import re
import time

from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By

# 需要优先切换到driver_title中含有VISIBLE的window_handler,没有的话再考虑切换到含有INVISIBLE的window_handler.
# 如果有多个含有INVISIBLE的window_handler，也就只有一个是正确的。需要尝试对一个进行分析，分析不出来东西以后考虑分析其他的
from utils.DriverConfig import Driver
from utils.pre_main_checker import PreMainDealerWebview, PreMainDealerXML

import logging

logger = logging.getLogger("my_app")
# driver = Driver.get_instance().get_driver()
my_driver = Driver()
# my_driver.switch_context_to_hybrid()
driver = my_driver.get_driver()

print(driver.contexts)
print(driver.current_context)
# info = driver.execute_script(
#     'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
# print('current url', info)
# print('driver title', driver.title)
# print(driver.window_handles)
# print(driver.current_window_handle)
# dic的键为
# dic = {}
# for handle in driver.window_handles:
#     driver.switch_to.window(handle)
#     title = driver.title
#     cur_handle = driver.current_window_handle
#     # cur_url = driver.execute_script(
#     #     'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
#     print('title', title)
#     # print('cur_url', cur_url)
#     print('cur_handle', cur_handle)
#     if title.endswith(':VISIBLE'):
#         dic[title[:]] = cur_handle[:]
#         print(title,cur_handle)
#         break
# print(dic)
# with open('麦xml首页.html','w',encoding='utf8') as f:
#     f.write(driver.page_source[:])
# print(driver.page_source[:])
# if len(dic) == 0:
#     # 寻找INVISIBLE
#     for handle in driver.window_handles:
#         driver.switch_to.window(handle)
#         title = driver.title
#         cur_handle = driver.current_window_handle
#         cur_url = driver.execute_script(
#             'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
#         print('title', title)
#         print('cur_url', cur_url)
#         print('cur_handle', cur_handle)
#         if cur_url[1:] in title and title.endswith(':INVISIBLE(PAUSED)'):
#             dic[cur_url[:]] = cur_handle[:]
#             print(title, cur_url, cur_handle)
#             break
# print(dic)
# with open('麦弹窗.html','w',encoding='utf8') as f:
#     f.write(driver.page_source)
# script = "wx.reLaunch({url:'" + '/pages/recent/recent' + "'})"
# driver.execute_script(script)
print(driver.current_activity)
# 在小程序里的activity：.plugin.appbrand.ui.AppBrandUI01
# 在最近程序页面的activity .plugin.appbrand.ui.AppBrandPluginUI

# driver.execute_script("wx.navigateToMiniProgram({appId:'wx25f982a55e60a540'})")
# driver.press_keycode(keycode=4)
# time.sleep(2)
# driver.execute_script("wx.navigateToMiniProgram({appId:'wx795bd500b21f8fee'})")
# driver.execute_script("wx.navigateToMiniProgram({appId:'wx3265fbb010daacc5'})")
# driver.switch_to.context("NATIVE_APP")
# driver.find_element(By.XPATH, '//android.view.View/android.view.View[4]/android.view.View/android.view.View/android.view.View[1]').click()
# print(driver.page_source)
# with open('掌上公交隐私政策页面.html', 'w', encoding='utf8') as f:
#     f.write(driver.page_source[:])
# driver.switch_to.context('NATIVE_APP')
# print(driver.page_source)
print(driver.current_context)
# driver.find_element(By.ID,)
# print(driver.title)

# Element containing 'privacy': wx-button, Attributes: id='481b619f--agree-btn', class='btn privacy--btn confirm-btn privacy--confirm-btn data-v-5bb8db51 privacy--data-v-5bb8db51', name='N/A', data-custom='N/A', Text: 我同意
# open-type="agreePrivacyAuthorization"
# 不知道为什么输入open-type才找到
# xpath_selector = "//wx-button[@open-type='agreePrivacyAuthorization']"
# xpath_selector = "//wx-button[@role='button' and @open-type='agreePrivacyAuthorization' and contains(text(),'我同意')]"
# element = driver.find_element(By.XPATH,xpath_selector)
# print(element.location)
# element.click()

# from utils.pre_main_checker import PreMainDealerWebview
#
# dealer = PreMainDealerWebview('D:\\python\\wx_test\\test\\掌上公交隐私政策页面.html')
# xpath_list = dealer.get_agree_button_xpath()
# for xpath in xpath_list:
#     element = driver.find_element(By.XPATH,xpath)
#     print(element)
#     print(element.location)
#     element.click()


print(driver.page_source[:])
# com.tencent.mm:id/m7g 申请框的resource-id com.tencent.mm:id/m7g
# com.tencent.mm:id/nsy 优惠券发放通知 同意按钮 resource-id
# com.tencent.mm:id/sn  总是保持以上选择 打勾按钮 resource-id
# android.widget.Button 允许 允许按钮 resource-id com.tencent.mm:id/czm 拒绝按钮 com.tencent.mm:id/cz6

xml_dealer = PreMainDealerXML(driver.page_source[:].encode('utf8'))

xpaths = xml_dealer.find_element_and_parent_xpath_by_text('隐私')
for xpath in xpaths:
    driver.find_element(By.XPATH,xpath).click()
# xpath = xml_dealer.find_message_send_request_1()
# if xpath:
#     driver.find_element(By.XPATH,xpath).click()

# HTMLdealer = PreMainDealerWebview(driver.page_source[:])

# xpath_list = HTMLdealer.get_login_button_xpath()


# HTMLdealer = PreMainDealerWebview(driver.page_source[:])
#
# checkbox_info = []
# HTMLdealer.get_checkbox_info(HTMLdealer.tree,checkbox_info)
# print(checkbox_info)
# xpath = HTMLdealer.deal_with_checkbox_info(checkbox_info)
# print(xpath)
#
# # print(driver.find_element(By.XPATH,xpath[0]).location)
# driver.find_element(By.XPATH,xpath[0]).click()
#
# login_button_info = []
# HTMLdealer.get_login_button_info(HTMLdealer.tree,login_button_info)
# xpath = HTMLdealer.deal_with_agree_button_info(login_button_info)
# print(xpath)
# driver.find_element(By.XPATH,xpath[0]).click()

# print(driver.page_source[:])
# print(driver.find_element(By.XPATH,'//android.widget.TextView[@text="微信绑定号码"]').location)
# driver.find_element(By.XPATH,'//android.widget.TextView[@text="微信绑定号码"]').click()
# 通过等待7s，获取验证码
# print(driver.page_source[:])
# xml_dealer = PreMainDealerXML(driver.page_source[:].encode('utf-8'))
# xpath_list = xml_dealer.get_pp_checkbox_agreebutton_xpath()
# print(xpath_list)
# for xpath in xpath_list:
#     driver.find_element(By.XPATH,xpath).click()
# HTML_dealer = PreMainDealerWebview(driver.page_source[:])
# info = []
# # ['close','close-icon','ad_close']
# HTML_dealer.get_component_by_class_name(['close'],HTML_dealer.tree,info)
# # print(info)
# xpaths = HTML_dealer.deal_with_close_icon(info)
# print(xpaths)
# for xpath in xpaths:
#     try:
#         driver.find_element(By.XPATH,xpath).click()
#     except Exception as e:
#         logger.exception(e)

# 测试点击手机号和验证码输入框
# driver.find_element(By.XPATH, "//android.widget.EditText[contains(@text, '手机号')]").click()
# phone = '13431940163'
# for s in phone:
#     driver.find_element(By.XPATH, f'//android.widget.Button[@content-desc="{s}"]').click()
# time.sleep(0.1)
# driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, '验证码')]").click()
# time.sleep(6)
# notification = driver.execute_script("mobile: getNotifications")
# sms_text = notification['statusBarNotifications'][0]['notification']['text']
# print('sms_text',sms_text)
# match = re.search(r'\d{3,}', sms_text)
# # Extract the SMS code
# sms_code = match.group(0) if match else None
# print(sms_code)
# driver.find_element(By.XPATH, "//android.widget.EditText[contains(@text, '验证码')]").click()
# for s in sms_code:
#     driver.find_element(By.XPATH, f'//android.widget.Button[@content-desc="{s}"]').click()

# buttons_to_click = xml_dealer.get_checkbox_login_button_xpath()
# for xpath in buttons_to_click:
#     driver.find_element(By.XPATH,xpath)
