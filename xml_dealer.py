from lxml import etree
# 这个# Requirement 1 2 只适用于菜鸟，不够通用。

class xml_dealer:
    def __init__(self, xml_name):
        self.xml_file = xml_name
        self.tree = etree.parse(xml_name)
        self.root = self.tree.getroot()

    def fuzzy_xpath_match(self, root, xpath):
        namespaces = {'android': 'http://schemas.android.com/apk/res/android'}
        return root.xpath(xpath, namespaces=namespaces)

    def process_view_element(self, element, xpath, xpath_list):
        for child in element:
            if 'text' in child.attrib:
                text_content = child.attrib['text']
                if len(text_content) >= 2:
                    # Requirement 1: Print children with text content > 2
                    print(child.tag, child.attrib['text'])
                    print(f'{xpath}/{child.tag}[@text="{child.attrib["text"]}"]')  # Print the XPath of the element
                    print(f'//{child.tag}[@text="{child.attrib["text"]}"]')  # Print the XPath of the element
                    xpath_list.append(f'//{child.tag}[@text="{child.attrib["text"]}"]')

                elif len(text_content) < 2:
                    # Requirement 2: Recursively process children with text content < 2
                    self.process_view_element(child, self.tree.getpath(child), xpath_list)

    def main(self) -> list:
        matches = self.fuzzy_xpath_match(self.root, "//android.webkit.WebView")
        res = []
        # Process the matched elements
        for element in matches:
            self.process_view_element(element, self.tree.getpath(element), res)
        print(res)
        return res