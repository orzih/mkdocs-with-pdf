import unittest
from pathlib import Path
from logging import Logger
from mkdocs_with_pdf.drivers.headless_chrome import HeadlessChromeDriver
from mkdocs_with_pdf.drivers.web_driver import WebDriver
from mkdocs_with_pdf.drivers.headless_chrome import HeadlessChromeDriver


class WebDriverTest(unittest.TestCase):

    __input_html = Path('tests') / Path('assets') / Path('input.html')

    __output_html = Path('tests') / Path('assets') / Path('output.html')

    def test_drivers(self):

        log = Logger('tests')
        drivers: list[WebDriver] = [
            HeadlessChromeDriver(program_path='chromium', logger=log),
        ]

        for driver in drivers:
            self.__assert_render(driver)

    def __assert_render(self, driver: WebDriver):

        input_html = self.__input_html.read_text()
        expected_output_html = self.__output_html.read_text()

        rendered_html = driver.render(input_html)

        # self.__output_html.read_text(rendered_html)

        self.assertEqual(rendered_html, expected_output_html)
