from utils.html_dealer import HtmlDealer
from utils.xpath2location import convert
from utils.DriverConfig import Driver
from utils.pre_main_checker import PreMainDealerWebview

if __name__ == '__main__':
    # my_html_dealer = HtmlDealer('掌上公交隐私政策页面.html')
    # button_info = my_html_dealer.main()
    # print(button_info)
    # location_set = convert(xpath_set, Driver.get_instance().get_driver())
    # for location in location_set:
    #     print(location)

    dealer = PreMainDealerWebview('D:\\python\\wx_test\\test\\掌上公交隐私政策页面.html')
    dealer.get_agree_button_xpath()
