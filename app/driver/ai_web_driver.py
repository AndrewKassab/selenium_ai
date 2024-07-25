import base64
import json
from typing import Optional

import openai
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_ai.app.chat_completions.system_messages import FIND_ELEMENT_SYSTEM_MESSAGE
from selenium_ai.app.chat_completions.tool_calls import FIND_ELEMENT_TOOL_CALL


class AiWebDriver(WebDriver):
    ''' Currently only works for Chrome / automatically assumes we are using chrome'''

    def __init__(self):
        super().__init__()
        self.ai_client = openai.Client()
        By.ID

    def find_element(self, by=By.ID, value: Optional[str] = None) -> WebElement:
        """
        Overrides the parent method, but behaves as usual unless an element isn't found

        If an element is not found, we will attempt one more time by leveraging AI to find
        what it thinks is the nearest matching element.
        """
        try:
            return super().find_element(by, value)
        except NoSuchElementException:
            arguments = self._get_ai_args_find_element(by, value)
            return self.find_element(arguments['by'].lower(), arguments['value'])

    def find_element_with_description(self, element_description: str) -> WebElement:
        """
        Attempts to leverage AI to find the element in question
        :return:
        """
        pass

    def _get_ai_args_find_element(self, by, value):
        """
        return: Returns a dictionary with (By, value) to attempt to find the element again
        """
        self.save_screenshot('ss.png')
        messages = [
            FIND_ELEMENT_SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': f'We have failed using the following: driver.find_element(by={by}, value={value}'
            },
            self._get_screenshot_as_ai_call_message(),
            {
                'role': 'user',
                'content': f'The HTML is as follows """\n\n{self.page_source}\n\n"""'
            }
        ]
        response = self.ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=[FIND_ELEMENT_TOOL_CALL],
            tool_choice="auto"
        )
        tool_call_arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        return tool_call_arguments

    def _get_screenshot_as_ai_call_message(self):
        self.save_screenshot('ss.png')
        with open('ss.png', 'rb') as image_file:
            base_64_image = base64.b64encode(image_file.read()).decode('utf-8')
            message = {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': 'This is a screenshot of the current web page.'
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            "url": f'data:image/jpeg;base64,{base_64_image}'
                        }
                    }
                ]
            }
            return message
