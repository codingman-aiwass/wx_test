from utils.InitConfig import Driver

driver = Driver.get_instance().get_driver()
print(driver.contexts)