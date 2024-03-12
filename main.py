import time

from utils.DriverConfig import Driver, check_status

Driver.get_instance().switch_context_to_default()
driver = Driver.get_instance().get_driver()
import logging

logger = logging.getLogger("my_app")

if __name__ == '__main__':
    logger.info("execute check_status()")
    check_status()
    logger.info("execute to_recent_used_page()")
    Driver.get_instance().to_recent_used_page()
    # 开始跳转小程序
    app_id = 'wx795bd500b21f8fee'
    Driver.get_instance().to_configured_mini_program(app_id)
    # 等待5s，等广告跳过
    time.sleep(5)
    #








