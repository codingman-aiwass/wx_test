from lxml import etree


def find_elements_by_class(file_path, class_name):
    # Parse the XML file
    with open(file_path, 'rb') as file:  # Use binary mode for lxml
        tree = etree.parse(file)

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


# Example usage
file_path = '../亚马逊隐私政策.xml'  # Replace with your actual XML file path
class_name = 'android.widget.CheckBox'

found, elements = find_elements_by_class(file_path, class_name)

if found:
    print(f"Components with class '{class_name}' found in the XML.")
    for i in range(len(elements)):
        print(f"//android.widget.CheckBox[{i+1}]")

else:
    print(f"Components with class '{class_name}' not found in the XML.")
