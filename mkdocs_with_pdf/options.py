import logging

from bs4 import BeautifulSoup
from mkdocs.config import config_options

from .drivers.headless_chrome import HeadlessChromeDriver


def _normalize(text: str) -> str:
    if text:
        return BeautifulSoup(text, 'html.parser').text
    return None


class Options(object):

    config_scheme = (
        ('enabled_if_env', config_options.Type(str)),

        ('verbose', config_options.Type(bool, default=False)),
        ('debug_html', config_options.Type(bool, default=False)),
        ('show_anchors', config_options.Type(bool, default=False)),

        ('output_path', config_options.Type(str, default="pdf/document.pdf")),
        ('theme_handler_path', config_options.Type(str, default=None)),

        ('author', config_options.Type(str, default=None)),
        ('copyright', config_options.Type(str, default=None)),

        ('cover', config_options.Type(bool, default=True)),
        ('cover_title', config_options.Type(str, default=None)),
        ('cover_subtitle', config_options.Type(str, default=None)),

        ('toc_title', config_options.Type(str, default="Table of contents")),
        ('heading_shift', config_options.Type(bool, default=True)),
        ('toc_level', config_options.Type(int, default=2)),
        ('ordered_chapter_level', config_options.Type(int, default=3)),
        ('excludes_children', config_options.Type(list, default=[])),

        ('exclude_pages', config_options.Type(list, default=[])),
        ('convert_iframe', config_options.Type(list, default=[])),
        ('two_columns_level', config_options.Type(int, default=0)),

        ('render_js', config_options.Type(bool, default=False)),
        ('headless_chrome_path',
            config_options.Type(str, default='chromium-browser'))
    )

    def __init__(self, local_config, config, logger: logging):
        self.strict = True if config['strict'] else False

        self.verbose = local_config['verbose']
        self.debug_html = local_config['debug_html']
        self.show_anchors = local_config['show_anchors']

        self.output_path = local_config.get('output_path', None)
        self.theme_handler_path = local_config.get('theme_handler_path', None)

        # Author and Copyright
        self._author = _normalize(local_config['author'])
        if not self._author:
            self._author = _normalize(config['site_author'])

        self._copyright = _normalize(local_config['copyright'])
        if not self._copyright:
            self._copyright = _normalize(config['copyright'])

        # Cover
        self.cover = local_config['cover']
        if self.cover:
            self._cover_title = local_config['cover_title'] \
                if local_config['cover_title'] else config['site_name']
            self._cover_subtitle = local_config['cover_subtitle']

        # TOC and Chapter heading
        self.toc_title = _normalize(local_config['toc_title'])
        self.heading_shift = local_config['heading_shift']
        self.toc_level = local_config['toc_level']
        self.ordered_chapter_level = local_config['ordered_chapter_level']
        self.excludes_children = local_config['excludes_children']

        # Page
        self.exclude_pages = local_config['exclude_pages']
        self.convert_iframe = local_config['convert_iframe']

        self.two_columns_level = local_config['two_columns_level']

        # ...etc.
        self.js_renderer = None
        if local_config['render_js']:
            self.js_renderer = HeadlessChromeDriver.setup(
                local_config['headless_chrome_path'], logger)

        # Theming
        self.theme_name = config['theme'].name
        self.theme_handler_path = config.get('theme_handler_path', None)

        # for system
        self._logger = logger

    @property
    def author(self) -> str:
        return self._author

    @property
    def copyright(self) -> str:
        return self._copyright

    @property
    def cover_title(self) -> str:
        return self._cover_title

    @property
    def cover_subtitle(self) -> str:
        return self._cover_subtitle

    @property
    def logger(self) -> logging:
        return self._logger
