import logging

from utils.DriverConfig import Driver

driver = Driver.get_instance().get_driver()
logging.info(driver.contexts)