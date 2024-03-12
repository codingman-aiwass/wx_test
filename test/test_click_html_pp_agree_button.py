from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.xpath2location import convert
from utils.DriverConfig import Driver
from utils.xml_dealer import xml_dealer
driver = Driver.get_instance().get_driver()

print(driver.contexts)
Driver.get_instance().switch_context_to_hybrid()
# print(driver.find_element(By.XPATH,"//wx-button[normalize-space(text())='我同意']"))
# Find all elements in the page

script = """
var elements = document.querySelectorAll('*');
var privacyElements = [];
for (var i = 0; i < elements.length; i++) {
    if (elements[i].innerText.includes('隐私')) {
        privacyElements.push(elements[i].outerHTML);
    }
}
return privacyElements;
"""

# Execute the JavaScript
elements_containing_privacy = driver.execute_script(script)

# Print the elements (or outer HTML) containing "privacy"
for element_html in elements_containing_privacy:
    print(element_html)