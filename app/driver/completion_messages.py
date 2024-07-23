from selenium.webdriver.common.by import By

by_options = ', '.join([attr for attr in dir(By) if not callable(getattr(By, attr)) and not attr.startswith("__")])

FIND_ELEMENT_SYSTEM_MESSAGE = 'You are working in conjunction with Selenium in Python to create a WebElement object. ' \
                              'When a programmer fails, you are needed for parsing HTML to find a unique selector ' \
                              'for the element that you believe the programmer was attempting to find. I will first ' \
                              'tell you the parameters the programmer was using, and then I will send over the HTML ' \
                              'for the page. Respond first with the By option and then the value separated by a space ' \
                              f'like so: XPATH "//input[@name=field]". The options are as follows: {by_options}.' \
                              'Please wait for both the input and the HTML before attempting a solution' \
