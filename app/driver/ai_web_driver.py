from typing import Optional

import openai
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_ai.app.driver import completion_messages
from selenium_ai.app.driver.ai_web_element import AiWebElement


class AiWebDriver(WebDriver):
    ''' Currently only works for Chrome / automatically assumes we are using chrome'''

    def __init__(self):
        super().__init__()
        self.ai_client = openai.Client()

    def find_element(self, by=By.ID, value: Optional[str] = None) -> WebElement:
        '''
        Overrides the parent method, but behaves as usual unless an element isn't found

        If an element is not found, we will attempt one more time by leveraging AI to find
        what it thinks is the nearest matching element.
        '''
        try:
            return super().find_element(by, value)
        except NoSuchElementException:
            selector = self._get_chat_completion_find_element(by, value)
            return self.find_element(selector)

    def find_element_with_description(self, element_description: str) -> WebElement:
        '''
        Attempts to leverage AI to find the element in question
        :return:
        '''
        pass

    def _get_chat_completion_find_element(self, by, value):
        '''
        return: Returns a tuple with (By, value) to attempt to find the element again
        '''
        messages = [{
            'role': 'system',
            'content': completion_messages.FIND_ELEMENT_SYSTEM_MESSAGE,
        }, {
            'role': 'user',
            'content': f'We have failed using the following: driver.find_element(by={by}, value={value}'
        }, {
            'role': 'user',
            'content': f'The HTML is as follows """\n\n{self.page_source}\n\n"""'
        },]
        response = self.ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
