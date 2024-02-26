from lxml import etree


class PreMainDealer:
    def __init__(self, xml_name):
        self.xml_file = xml_name
        self.tree = etree.parse(xml_name)
        self.root = self.tree.getroot()

    def fuzzy_xpath_match(self, root, xpath):
        namespaces = {'android': 'http://schemas.android.com/apk/res/android'}
        return root.xpath(xpath, namespaces=namespaces)

    def find_pp_element(self, element):
        if 'text' in element.attrib:
            text_content = element.attrib['text']
            if '隐私' in text_content:
                print(text_content)
        for child in element:
            self.find_pp_element(child)

    def find_agree_button(self, element):
        if 'text' in element.attrib:
            text_content = element.attrib['text']
            if '不同意' in text_content:
                print(text_content)
        for child in element:
            self.find_pp_element(child)

    def main(self) -> set:
        matches = self.fuzzy_xpath_match(self.root, "/hierarchy")
        # Process the matched elements
        for element in matches:
            self.find_pp_element(element)
            print()
            # self.find_agree_button(element)
