from selenium.webdriver.remote.webelement import WebElement
from selenium_ai.app.driver.ai_web_driver import ai_client


class AiWebElement(WebElement):

    def __init__(self):
        super().__init__()
