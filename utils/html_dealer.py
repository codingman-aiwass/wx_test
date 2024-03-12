from lxml import html


class HtmlDealer:
    def __init__(self, html_file):
        with open(html_file,'r',encoding='utf8') as f:
            html_content = f.read()
        self.tree = html.fromstring(html_content)

    # 由于id class 可能是微信动态生成的，所以我们需要获取一些比较固定的属性。比如 open-type role

    def get_agree_button_info(self, element, agree_button_info):
        # Check if the element contains text and if the text contains "privacy"
        if element.text_content().strip():
            text_content = element.text_content().strip().lower()  # Assuming case-insensitive search
            if "同意" in text_content:
                if text_content in ['我同意','同意','同意并允许']:
                    # Extract element's tag name
                    tag_name = element.tag
                    # Extract attributes such as id, class, name, or any other relevant attributes
                    element_id = element.get('id', 'N/A')  # Defaults to 'N/A' if not present
                    class_name = element.get('class', 'N/A')
                    name_attribute = element.get('name', 'N/A')
                    # Example of extracting a custom data attribute
                    data_custom = element.get('data-custom',
                                              'N/A')  # Adjust 'data-custom' based on actual attribute name
                    role = element.get('role','N/A')
                    open_type = element.get('open-type','N/A')
                    # Construct a representation of the element's attributes for easier identification
                    attributes_info = f"id='{element_id}', class='{class_name}', name='{name_attribute}', data-custom='{data_custom}'"
                    agree_button_info.append({'tag_name':tag_name, 'role':role, 'open_type':open_type})

                    print(
                        f"Element containing 'privacy': {tag_name}, Attributes: {attributes_info}, Text: {text_content},role:{role},open_type:{open_type}")
                # Optionally, collect information about elements in a set or list

        # Recursively process all child elements
        for child in element:
            self.get_agree_button_info(child, agree_button_info)

    def main(self):
        res = []
        # Process the whole document starting from the root element
        self.get_agree_button_info(self.tree, res)
        return res
