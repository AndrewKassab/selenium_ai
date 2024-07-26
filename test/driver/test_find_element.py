from unittest import TestCase
from unittest.mock import patch

from pathlib import Path

from selenium.webdriver.common.by import By

from selenium_ai.app.driver.ai_web_driver import AiWebDriver

html_path = str(Path(__file__).parent.parent / 'resources' / 'test_page.html')


class FindElementTest(TestCase):
    """Integration tests for AiWebDriver.find_element"""

    def setUp(self):
        self.driver = AiWebDriver()
        self.driver.get(html_path)

    @patch.object(AiWebDriver, '_get_ai_args_find_element')
    def test_find_element_correct_id_no_ai(self, spy_ai_args):
        element = self.driver.find_element(By.ID, 'email')
        spy_ai_args.assert_not_called()

    def test_find_element_false_id_use_ai(self):
        '''Test that AI is able to find the email element when the wrong ID is provided'''
        with patch.object(self.driver, '_get_ai_args_find_element',
                          wraps=self.driver._get_ai_args_find_element) as spy_ai_args:
            element = self.driver.find_element(By.ID, 'emal')
            spy_ai_args.assert_called_once()

