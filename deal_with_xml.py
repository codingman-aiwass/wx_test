from lxml import etree


def fuzzy_xpath_match(root, xpath):
    namespaces = {'android': 'http://schemas.android.com/apk/res/android'}
    return root.xpath(xpath, namespaces=namespaces)

def process_view_element(element, xpath, xpath_list):
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
                process_view_element(child, tree.getpath(child), xpath_list)


# Parse the XML file
tree = etree.parse('main_page.xml')
root = tree.getroot()
matches = fuzzy_xpath_match(root, "//android.webkit.WebView")
res = []
# Process the matched elements
for element in matches:
    process_view_element(element, tree.getpath(element), res)
print(res)
