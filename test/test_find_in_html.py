from lxml import etree

# Your HTML content (for demonstration, it's just the provided element, but it could be a whole HTML document)
# html_content = '''
# <wx-button class="btn privacy--btn confirm-btn privacy--confirm-btn data-v-5bb8db51 privacy--data-v-5bb8db51" data-event-opts="agreeprivacyauthorization,handleAgree,$event" id="481b619f--agree-btn" open-type="agreePrivacyAuthorization" role="button" aria-disabled="false" data-appium-inspector-width="391" data-appium-inspector-height="113" data-appium-inspector-x="541" data-appium-inspector-y="1687">我同意</wx-button>
# '''
with open('掌上公交隐私政策页面.html', 'r', encoding='utf8') as f:
    html_content = f.read()

# Parse the HTML
root = etree.HTML(html_content)

'''
# Use XPath to find elements by tag and content
# Note: The use of `normalize-space()` function to trim any leading/trailing whitespace around the text
elements = root.xpath("//wx-button[normalize-space(text())='我同意']")
# If the element is found, you can then further interact with it
for elem in elements:
    print(
        f"Found element: ID = {elem.get('id')}, Class = {elem.get('class')}, Width = {elem.get('data-appium-inspector-width')}, Height = {elem.get('data-appium-inspector-height')},X = {elem.get('data-appium-inspector-x')},Y = {elem.get('data-appium-inspector-y')}")
'''

# Find all elements in the page
elements = driver.find_elements_by_xpath("//*")

# Iterate through each element and check for text containing "privacy"
for element in elements:
    try:
        text = element.text
        if "privacy" in text.lower():  # Check if "privacy" is in the element's text (case insensitive)
            print(f"Found 'privacy' in element: {element.tag_name}, text: {text}")
    except Exception as e:
        # Handle potential errors, e.g., element not being visible anymore
        print(f"Error processing element: {e}")