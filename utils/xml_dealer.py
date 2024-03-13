from lxml import etree


class xml_dealer:
    def __init__(self, xml_content):
        # self.xml_file = xml_content
        # self.tree = etree.parse(xml_content,parser=etree.XMLParser())
        self.tree = etree.fromstring(text=xml_content,parser=etree.XMLParser())
        self.root = self.tree.getroot()

    def fuzzy_xpath_match(self, root, xpath):
        namespaces = {'android': 'http://schemas.android.com/apk/res/android'}
        return root.xpath(xpath, namespaces=namespaces)

    def process_view_element(self, element, xpath, xpath_set):
        if 'content-desc' in element.attrib:
            text_content = element.attrib['content-desc']
            if text_content == 'content-desc' or text_content == '更多':
                print('skip close or more button')
        # if 'text' in element.attrib:
        #     text_content = element.attrib['text']
        #     if text_content in ['我的','福利','查快递','首页']:
        #         print(text_content)
        else:
            xpath_set.add(f'{xpath}')
        for child in element:
            self.process_view_element(child, self.tree.getpath(element), xpath_set)

    def main(self) -> set:
        matches = self.fuzzy_xpath_match(self.root, "/hierarchy")
        res = set()
        # Process the matched elements
        for element in matches:
            self.process_view_element(element, self.tree.getpath(element), res)
        # print(res)
        return res
