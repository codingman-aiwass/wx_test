from utils.xml_dealer import xml_dealer
from utils.xpath2location import convert
from utils.DriverConfig import Driver

if __name__ == '__main__':
    my_xml_dealer = xml_dealer('../main_page.xml')
    xpath_set = my_xml_dealer.main()
    location_set = convert(xpath_set, Driver.get_instance().get_driver())
    for location in location_set:
        print(location)
