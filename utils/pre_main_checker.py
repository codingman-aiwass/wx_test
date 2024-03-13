from lxml import etree, html
import logging

logger = logging.getLogger("my_app")


# 在对主界面进行点击之前，判断是否有 隐私政策界面/权限请求界面/广告界面（含有跳过按钮）/被广告弹窗覆盖的主界面（不点击掉弹窗就无法进行下一步遍历）
# 通过xml文件进行判断
class PreMainDealerXML:
    def __init__(self, xml_content):
        # self.xml_file = xml_content
        # self.tree = etree.parse(xml_content, etree.XMLParser())
        self.xml_content = xml_content
        self.root = etree.fromstring(text=xml_content, parser=etree.XMLParser())
        self.tree = etree.ElementTree(self.root)
        # self.root = self.tree.getroot()
        self.contains_pp_element = False
        self.agree_pp_button = None

    def fuzzy_xpath_match(self, root, xpath):
        namespaces = {'android': 'http://schemas.android.com/apk/res/android'}
        return root.xpath(xpath, namespaces=namespaces)

    # 检查该页面是否为隐私政策同意页面
    def find_pp_element(self, element):
        if 'text' in element.attrib:
            text_content = element.attrib['text']
            if '隐私' in text_content:
                print(text_content)
                self.contains_pp_element = True
        for child in element:
            self.find_pp_element(child)

    # 通过text内容是否包含同意 我同意 同意并继续判断是否为隐私政策同意按钮
    def find_agree_button_by_text_content(self, element):
        if 'text' in element.attrib:
            text_content = element.attrib['text']
            if '同意' in text_content:
                # if text_content == '同意' or text_content == '我同意':
                if text_content in ['同意', '我同意', '同意并继续']:
                    self.agree_pp_button = self.tree.getpath(element)
        for child in element:
            self.find_agree_button_by_text_content(child)

    # 通过class寻找同意按钮。但是因为有的隐私政策同意页面都是android.widget.TextView，所以会出现漏报。暂时废弃
    # def find_agree_button_by_class(self):
    #     # 寻找xml中class为android.widget.Button的组件，要求其内容中含有同意且不含不或者拒绝字样
    #     class_name = 'android.widget.Button'
    #     found,elements = self.find_elements_by_class(self.xml_file,class_name)
    #     res = []
    #     if found:
    #         print(f"Components with class '{class_name}' found in the XML.")
    #         for i in range(len(elements)):
    #             print(f"//{class_name}[{i + 1}]")
    #             res.append(f"//{class_name}[{i + 1}]")
    #     else:
    #         print(f"Components with class '{class_name}' not found in the XML.")
    #     return res

    # 根据class寻找xml文件中的组件

    # 通过class在xml中寻找指定元素
    def find_elements_by_class(self, xml_content, class_name):
        # Parse the XML file
        # with open(file_path, 'rb') as file:  # Use binary mode for lxml
        #     tree = etree.parse(file)
        try:
            tree = etree.fromstring(xml_content)
        except etree.XMLSyntaxError as e:
            print(f"Error parsing XML: {e}")
            return False, []

        # XPath query to find elements with a specific class attribute
        query = f"//*[@class='{class_name}']"
        # query = f"//android.widget.CheckBox"

        # Execute the XPath query
        elements = tree.xpath(query)

        # Check if any elements were found
        if elements:
            return True, elements
        else:
            return False, []

    # 返回界面中所有的多选框的xpath，方便后续进行打勾操作
    def get_checkbox_xpath(self):
        class_name = 'android.widget.CheckBox'
        # found, elements = self.find_elements_by_class(self.xml_file, class_name)
        found, elements = self.find_elements_by_class(self.xml_content, class_name)
        res = []
        if found:
            logger.info(f"Components with class '{class_name}' found in the XML.")
            for i in range(len(elements)):
                logger.info(f"//android.widget.CheckBox[{i + 1}]")
                res.append(f"//android.widget.CheckBox[{i + 1}]")
        else:
            logger.info(f"Components with class '{class_name}' not found in the XML.")
        return res

    # 在判定该界面为隐私政策页面以后，获取多选框和同意按钮的xpath list，方便后续进行点击
    def get_pp_checkbox_agreebutton_xpath(self):
        res = []
        # 先检查有没有多选框需要勾选
        checkbox_list = self.get_checkbox_xpath()
        if len(checkbox_list) > 0:
            res.extend(checkbox_list)
        # 寻找隐私政策同意按钮
        matches = self.fuzzy_xpath_match(self.root, "/hierarchy")
        # Process the matched elements
        for element in matches:
            self.find_pp_element(element)
            if self.contains_pp_element:
                print('find pp')
                break
        if self.contains_pp_element:
            for element in matches:
                self.find_agree_button_by_text_content(element)
        if self.agree_pp_button is not None:
            res.append(self.agree_pp_button[:])
        return res

    # 检查是否有权限请求弹窗1,其中一种权限请求弹窗（位置信息请求）的类型
    def find_location_request_1(self):
        # 这类请求的弹窗XPATH为 //android.widget.RelativeLayout[@resource-id="com.tencent.mm:id/lzo"]
        # 这类请求的允许按钮的xpath为 //android.widget.Button[@resource-id="com.tencent.mm:id/lzx"]
        if len(self.tree.xpath('//android.widget.RelativeLayout[@resource-id="com.tencent.mm:id/lzo"]')) == 1:
            logger.info('find location permission request')
            if len(self.tree.xpath('//android.widget.Button[@resource-id="com.tencent.mm:id/lzx"]')) == 1:
                logger.info('find allow')
                return '//android.widget.Button[@resource-id="com.tencent.mm:id/lzx"]'
        return None


# TODO 小程序广告弹窗的位置无法探知。有的能在xml中看到，有的不能。听说能在webview中通过resource id看到，但是不知道怎么看
# TODO 小程序的隐私政策也有一些只能在webview里查看，需探索如何关闭
class PreMainDealerWebview:
    def __init__(self, html_content):
        # with open(html_name, 'r', encoding='utf8') as f:
        #     html_content = f.read()
        self.tree = html.fromstring(html_content)
        self.contains_pp_element = False
        self.agree_pp_button = None

    # 获取webview界面下隐私政策同意按钮的tag role open-type等信息
    def get_agree_button_info(self, element, agree_button_info):
        # Check if the element contains text and if the text contains "privacy"
        if element.text_content().strip():
            text_content = element.text_content().strip().lower()  # Assuming case-insensitive search
            if "同意" in text_content:
                if text_content in ['我同意', '同意', '同意并允许']:
                    # Extract element's tag name
                    tag_name = element.tag
                    # Extract attributes such as id, class, name, or any other relevant attributes
                    element_id = element.get('id', 'N/A')  # Defaults to 'N/A' if not present
                    class_name = element.get('class', 'N/A')
                    name_attribute = element.get('name', 'N/A')
                    # Example of extracting a custom data attribute
                    data_custom = element.get('data-custom',
                                              'N/A')  # Adjust 'data-custom' based on actual attribute name
                    role = element.get('role', 'N/A')
                    open_type = element.get('open-type', 'N/A')
                    # Construct a representation of the element's attributes for easier identification
                    attributes_info = f"id='{element_id}', class='{class_name}', name='{name_attribute}', data-custom='{data_custom}'"
                    agree_button_info.append(
                        {'tag_name': tag_name, 'role': role, 'open_type': open_type, 'id': element_id,
                         'class': class_name, 'name': name_attribute, 'data_custom': data_custom, 'text': text_content})

                    logger.info(
                        f"Element containing 'privacy': {tag_name}, Attributes: {attributes_info}, Text: {text_content},role:{role},open_type:{open_type}")
                # Optionally, collect information about elements in a set or list

        # Recursively process all child elements
        for child in element:
            self.get_agree_button_info(child, agree_button_info)

    # 处理获取到的属性，生成合适的xpath用于定位和点击。如果有open-type就只用open-type
    def deal_with_agree_button_info(self, agree_button_info):
        attributes = ['tag_name', 'role', 'open-type', 'name', 'text', 'id']
        logger.info(f'agree_button_info{agree_button_info}')
        # 目前的情况下，agree_button_info中只有一个元素
        xpath_exps = []
        for info in agree_button_info:
            xpath_exp = f"//{agree_button_info[0]['tag_name']}"
            conditions = []
            for attr in attributes[1:]:
                value = info.get(attr, 'N/A')
                if value != 'N/A':
                    if attr == 'text':
                        conditions.append(f"contains(text(),'{value}')")
                    else:
                        conditions.append(f"@{attr}='{value}'")
            if len(conditions) > 0:
                xpath_exp += "[" + " and ".join(conditions) + "]"
                xpath_exps.append(xpath_exp)
        return xpath_exps

    # 获取webview里隐私政策同意按钮入口方法
    def get_agree_button_xpath(self):
        agree_button_info = []
        self.get_agree_button_info(self.tree, agree_button_info)
        xpath = self.deal_with_agree_button_info(agree_button_info)
        logger.info(xpath)
        return xpath
