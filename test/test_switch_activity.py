import time

from utils.InitConfig import Driver
# 尝试通过appid进入一个没有进入过的小程序
Driver.get_instance().switch_context_to_hybrid()
driver = Driver.get_instance().get_driver()
print(driver.contexts)

# driver.execute_script("wx.navigateToMiniProgram({appId:'wx33fd6cdc62520063'})") # 腾讯会议
driver.press_keycode(keycode=4)
time.sleep(0.05)
driver.execute_script("wx.navigateToMiniProgram({appId:'wx25f982a55e60a540'})") # 麦

# driver.start_activity('.plugin.appbrand.ui.AppBrandUI01')
