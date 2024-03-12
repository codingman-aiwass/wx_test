# 测试输出当前界面拥有的所有context，URL 以及请求参数
# 想要输出正确的page_source或者执行js注入，需要处于正确的contexts以及window_handler
import time

from selenium.webdriver.common.by import By

# 需要优先切换到driver_title中含有VISIBLE的window_handler,没有的话再考虑切换到含有INVISIBLE的window_handler.
# 如果有多个含有INVISIBLE的window_handler，也就只有一个是正确的。需要尝试对一个进行分析，分析不出来东西以后考虑分析其他的
from utils.DriverConfig import Driver

Driver.get_instance().switch_context_to_hybrid()
driver = Driver.get_instance().get_driver()
print(driver.contexts)
print(driver.current_context)
info = driver.execute_script(
    'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
print('current url', info)
print('driver title', driver.title)
print(driver.window_handles)
print(driver.current_window_handle)
# dic的键为
dic = {}
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    title = driver.title
    cur_handle = driver.current_window_handle
    cur_url = driver.execute_script(
        'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
    print('title', title)
    print('cur_url', cur_url)
    print('cur_handle', cur_handle)
    if cur_url[1:] in title and title.endswith(':VISIBLE'):
        dic[cur_url[:]] = cur_handle[:]
        print(title, cur_url, cur_handle)
        break
print(dic)
if len(dic) == 0:
    # 寻找INVISIBLE
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        title = driver.title
        cur_handle = driver.current_window_handle
        cur_url = driver.execute_script(
            'return "/" + window.__route__  + (window.__queryString__ ? "?"+window.__queryString__ : ''"")')
        print('title', title)
        print('cur_url', cur_url)
        print('cur_handle', cur_handle)
        if cur_url[1:] in title and title.endswith(':INVISIBLE(PAUSED)'):
            dic[cur_url[:]] = cur_handle[:]
            print(title, cur_url, cur_handle)
            break
print(dic)
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
print(driver.title)

# Element containing 'privacy': wx-button, Attributes: id='481b619f--agree-btn', class='btn privacy--btn confirm-btn privacy--confirm-btn data-v-5bb8db51 privacy--data-v-5bb8db51', name='N/A', data-custom='N/A', Text: 我同意
# open-type="agreePrivacyAuthorization"
# 不知道为什么输入open-type才找到
# xpath_selector = "//wx-button[@open-type='agreePrivacyAuthorization']"
# xpath_selector = "//wx-button[@role='button' and @open-type='agreePrivacyAuthorization' and contains(text(),'我同意')]"
# element = driver.find_element(By.XPATH,xpath_selector)
# print(element.location)
# element.click()

from utils.pre_main_checker import PreMainDealerWebview

dealer = PreMainDealerWebview('D:\\python\\wx_test\\test\\掌上公交隐私政策页面.html')
xpath_list = dealer.get_agree_button_xpath()
for xpath in xpath_list:
    element = driver.find_element(By.XPATH,xpath)
    print(element)
    print(element.location)
    element.click()