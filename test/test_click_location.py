from utils.xpath2location import convert
from utils.InitConfig import Driver
from utils.xml_dealer import xml_dealer
driver = Driver.get_instance().get_driver()
# driver.save_page_source_to_file('main.xml')
# xml_dealer_1 = xml_dealer('main.xml')
print(driver.contexts)
Driver.get_instance().switch_context_to_hybrid()
# locations = convert(xml_dealer_1.main())
# for location in locations:
#     print(f'current position:{location}')
#     driver.tap(location)