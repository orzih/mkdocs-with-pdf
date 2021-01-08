import logging
import os
import sys
import importlib

from bs4 import BeautifulSoup

from mkdocs.config.base import Config
from mkdocs.structure.pages import Page


class EventHookHandler(object):
    """ Event hook on PDF generate sequence """

    _module_name = 'pdf_event_hook'

    @classmethod
    def on_serve(cls, server, builder, logger: logging):
        path = f'./{cls._module_name}.py'
        if os.path.isfile(path):
            logger.warn(f'watch {path}')
            server.watch(path, builder)

    def __init__(self, options: object, config: Config, logger: logging):
        self._options = options
        self._config = config
        self._logger = logger.getChild("HOOK")

        self._module = self._load_module()

    def _load_module(self):
        cwd = os.getcwd()
        if cwd not in sys.path:  # pragma: no cover
            sys.path.append(cwd)

        try:
            module = __import__(self.__class__._module_name)
            importlib.reload(module)
            self._logger.info('Found PDF rendering event hook module.')
        except ModuleNotFoundError:
            module = None

        return module

    #
    # HOOK methods
    #

    def inject_link(self, output_content: str, pdf_path: str,
                    page: Page, theme_handler) -> str:
        if self._module and hasattr(self._module, 'inject_link'):
            return self._module.inject_link(
                output_content, pdf_path, page, self._logger)
        return theme_handler.inject_link(output_content, pdf_path)

    def pre_js_render(self, soup: BeautifulSoup) -> BeautifulSoup:
        if self._module and hasattr(self._module, 'pre_js_render'):
            return self._module.pre_js_render(soup, self._logger)
        return soup

    def pre_pdf_render(self, html_string: str) -> BeautifulSoup:
        if self._module and hasattr(self._module, 'pre_pdf_render'):
            soup = BeautifulSoup(html_string, 'html.parser')
            soup = self._module.pre_pdf_render(soup, self._logger)
            return str(soup)
        return html_string
