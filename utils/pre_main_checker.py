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
        self.home_page_login_button = None

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

    def find_element_and_parent_xpath_by_text(self, search_text):
        elements = self.tree.xpath(f"//*[contains(@text, '{search_text}')]")
        res = []
        for element in elements:
            # Get XPath of the element
            element_xpath = self.tree.getpath(element)
            print(f"Element XPath: {element_xpath}")

            # Get parent element
            parent = element.getparent()
            if parent is not None:
                # Get XPath of the parent element
                parent_xpath = self.tree.getpath(parent)
                print(f"Parent XPath: {parent_xpath}")
                res.append(parent_xpath[:])
            else:
                print("No parent found.")
        return res

    # 通过text内容是否包含同意 我同意 同意并继续判断是否为隐私政策同意按钮
    def find_agree_button_by_text_content(self, element):
        if 'text' in element.attrib:
            text_content = element.attrib['text']
            if '同意' in text_content:
                # if text_content == '同意' or text_content == '我同意':
                if text_content in ['同意', '我同意', '同意并继续']:
                    self.agree_pp_button = self.tree.getpath(element)
            # 也有可能是 确认
            if '确认' in text_content:
                # if text_content == '同意' or text_content == '我同意':
                if text_content in ['确认', '确认并同意']:
                    self.agree_pp_button = self.tree.getpath(element)
        for child in element:
            self.find_agree_button_by_text_content(child)

    def find_login_button_by_text_content(self, element):
        if 'text' in element.attrib:
            text_content = element.attrib['text']
            if '登录' in text_content:
                if text_content in ['去登录', '登录', '一键登录']:
                    self.home_page_login_button = self.tree.getpath(element)
        for child in element:
            self.find_login_button_by_text_content(child)

    # 在登录页面点击多选框和登录按钮
    def get_checkbox_login_button_xpath(self):
        res = []
        # 先检查有没有多选框需要勾选
        checkbox_list = self.get_checkbox_xpath()
        if len(checkbox_list) > 0:
            res.extend(checkbox_list)
        self.find_login_button_by_text_content(self.tree)
        if self.home_page_login_button is not None:
            res.append(self.home_page_login_button)
        return res

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

    # 检查是否有发送一次以下信息请求，通过查看有没有xpath为//android.view.View[@resource-id="com.tencent.mm:id/nsy"] 或者直接查id为 com.tencent.mm:id/nsy的组件
    # 有则说明有可能这个申请框
    # 然后查找是否有拒绝按钮出现
    # 如果也有的话直接点击拒绝按钮
    def find_message_send_request_1(self):
        if len(self.tree.xpath('//android.view.View[@resource-id="com.tencent.mm:id/nsy"]')) >= 1:
            logger.info('find message send request')
        if len(self.tree.xpath('//android.widget.Button[@text="拒绝"]')) == 1:
            logger.info('find refuse button')
            return '//android.widget.Button[@text="拒绝"]'
        return None


# 处理点击手机号快捷登录以后出现的 申请获取并验证你的手机号 弹窗
# 需要切换到NATIVE_APP模式下，webview中没有
def get_login_popup_xpath():
    # 根据xpath定位并点击
    # //android.widget.TextView[@text="微信绑定号码"] 里面的文字内容 也可能是 上次提供，需要都点击试试
    return ['//android.widget.TextView[@text="微信绑定号码"]', '//android.widget.TextView[@text="微信绑定号码"]']


class PreMainDealerWebview:
    def __init__(self, html_content):
        # with open(html_name, 'r', encoding='utf8') as f:
        #     html_content = f.read()
        self.tree = html.fromstring(html_content)
        self.contains_pp_element = False
        self.agree_pp_button = None

    def get_component_by_class_name(self, target_class_names, element, info):
        # Check if the element's class attribute contains "checkbox"
        class_name = element.get('class', '')
        for target_class_name in target_class_names:
            if target_class_name in class_name:
                # Extract element's tag name
                tag_name = element.tag
                # Extract attributes such as id, class, name, or any other relevant attributes
                element_id = element.get('id', 'N/A')  # Defaults to 'N/A' if not present
                name_attribute = element.get('name', 'N/A')
                # Example of extracting a custom data attribute
                data_custom = element.get('data-custom', 'N/A')  # Adjust based on actual attribute name
                role = element.get('role', 'N/A')
                open_type = element.get('open-type', 'N/A')
                data_private_id = element.get('data-private-node-id', 'N/A')
                # Construct a representation of the element's attributes for easier identification
                attributes_info = f"id='{element_id}', class='{class_name}', name='{name_attribute}', data-custom='{data_custom}, data-private-node-id={data_private_id}'"
                info.append({
                    'tag_name': tag_name,
                    'role': role,
                    'open_type': open_type,
                    'id': element_id,
                    'class': class_name,
                    'name': name_attribute,
                    'data_custom': data_custom,
                    'data-private-node-id': data_private_id
                })

                logger.info(f"element found: {tag_name}, Attributes: {attributes_info}")

        # Recursively process all child elements
        for child in element:
            self.get_component_by_class_name(target_class_names, child, info)

    def deal_with_close_icon(self, infos):
        attributes = ['role', 'open-type', 'name', 'id', 'class', 'data-private-node-id']
        logger.info(f'infos: {infos}')
        res = []
        for info in infos:
            xpath_exp = f"//{info['tag_name']}"
            conditions = []
            for attr in attributes:
                value = info.get(attr, 'N/A')
                if value != 'N/A':
                    conditions.append(f"@{attr}='{value}'")
            if len(conditions) > 0:
                xpath_exp += "[" + " and ".join(conditions) + "]"
            res.append(xpath_exp)
        return res

    def get_checkbox_info(self, element, checkbox_info):
        # Check if the element's class attribute contains "checkbox"
        class_name = element.get('class', '')
        if 'checkbox' in class_name:
            # Extract element's tag name
            tag_name = element.tag
            # Extract attributes such as id, class, name, or any other relevant attributes
            element_id = element.get('id', 'N/A')  # Defaults to 'N/A' if not present
            name_attribute = element.get('name', 'N/A')
            # Example of extracting a custom data attribute
            data_custom = element.get('data-custom', 'N/A')  # Adjust based on actual attribute name
            role = element.get('role', 'N/A')
            open_type = element.get('open-type', 'N/A')
            # Construct a representation of the element's attributes for easier identification
            attributes_info = f"id='{element_id}', class='{class_name}', name='{name_attribute}', data-custom='{data_custom}'"
            checkbox_info.append({
                'tag_name': tag_name,
                'role': role,
                'open_type': open_type,
                'id': element_id,
                'class': class_name,
                'name': name_attribute,
                'data_custom': data_custom
            })

            logger.info(f"Checkbox element found: {tag_name}, Attributes: {attributes_info}")

        # Recursively process all child elements
        for child in element:
            self.get_checkbox_info(child, checkbox_info)

    def deal_with_checkbox_info(self, checkbox_info):
        attributes = ['role', 'open-type', 'name', 'id', 'class']
        logger.info(f'checkbox_info{checkbox_info}')
        res = []
        for info in checkbox_info:
            xpath_exp = f"//{info['tag_name']}"
            conditions = []
            for attr in attributes:
                value = info.get(attr, 'N/A')
                if value != 'N/A':
                    conditions.append(f"@{attr}='{value}'")
            if len(conditions) > 0:
                xpath_exp += "[" + " and ".join(conditions) + "]"
            res.append(xpath_exp)
        return res

    # 获取webview下所有checkbox的xpath
    def get_checkbox_xpath(self):
        checkbox_info = []
        self.get_checkbox_info(self.tree, checkbox_info)
        ret_xpath_list = self.deal_with_checkbox_info(checkbox_info)
        return ret_xpath_list

    # 在主页寻找去登陆按钮
    def get_to_login_button_info_in_main_page(self, element, to_login_button_info):
        if element.text_content().strip():
            text_content = element.text_content().strip().lower()  # Assuming case-insensitive search
            if "登录" in text_content or '快速' in text_content or '快捷' in text_content:
                if text_content in ['去登录', '快捷登录', '一键登录', '手机号快捷登录', '登录', '马上登录', '立刻登录',
                                    '手机号快速验证']:
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
                    to_login_button_info.append(
                        {'tag_name': tag_name, 'role': role, 'open_type': open_type, 'id': element_id,
                         'class': class_name, 'name': name_attribute, 'data_custom': data_custom, 'text': text_content})

                    logger.info(
                        f"Element containing 'privacy': {tag_name}, Attributes: {attributes_info}, Text: {text_content},role:{role},open_type:{open_type}")
                # Optionally, collect information about elements in a set or list

        # Recursively process all child elements
        for child in element:
            self.get_to_login_button_info_in_main_page(child, to_login_button_info)

    def get_to_login_button_xpath(self):
        to_login_button_info = []
        self.get_to_login_button_info_in_main_page(self.tree, to_login_button_info)
        ret_xpath_list = self.deal_with_agree_button_info(to_login_button_info)
        return ret_xpath_list

    # 在登录页面，去找到菜鸟 手机号快捷登录的按钮
    def get_login_button_info(self, element, login_button_info):
        # Check if the element contains text and if the text contains "privacy"
        if element.text_content().strip():
            text_content = element.text_content().strip().lower()  # Assuming case-insensitive search
            if "登录" in text_content:
                if text_content in ['手机号快捷登录', '快捷登录', '一键登录']:
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
                    login_button_info.append(
                        {'tag_name': tag_name, 'role': role, 'open_type': open_type, 'id': element_id,
                         'class': class_name, 'name': name_attribute, 'data_custom': data_custom, 'text': text_content})

                    logger.info(
                        f"Element containing 'privacy': {tag_name}, Attributes: {attributes_info}, Text: {text_content},role:{role},open_type:{open_type}")
                # Optionally, collect information about elements in a set or list

        # Recursively process all child elements
        for child in element:
            self.get_login_button_info(child, login_button_info)

    # 获取登录界面下checkbox的xpath和快捷登录按钮的xpath
    def get_login_button_xpath(self):
        login_button_info = []
        self.get_login_button_info(self.tree, login_button_info)
        login_button_xpath_list = self.deal_with_agree_button_info(login_button_info)
        checkbox_xpath_list = self.get_checkbox_xpath()
        return checkbox_xpath_list + login_button_xpath_list

    # TODO 还有类似任你购这种登录界面样式不同的小程序需要处理

    # 获取webview界面下隐私政策同意按钮的tag role open-type等信息
    def get_agree_button_info(self, element, agree_button_info):
        # Check if the element contains text and if the text contains "privacy"
        if element.text_content().strip():
            text_content = element.text_content().strip().lower()  # Assuming case-insensitive search
            if "同意" in text_content:
                if text_content in ['我同意', '同意', '同意并允许', '同意并继续']:
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
            self.get_login_button_info(child, agree_button_info)

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
        self.get_login_button_info(self.tree, agree_button_info)
        xpath = self.deal_with_agree_button_info(agree_button_info)
        logger.info(xpath)
        return xpath

    # 获取html页面的源码，生成所有组件的xpath，用于后续点击
