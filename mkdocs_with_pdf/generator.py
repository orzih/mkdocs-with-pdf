import logging
import os
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from uuid import uuid4

from bs4 import BeautifulSoup, PageElement
from weasyprint import HTML, urls

from .cover import make_cover
from .options import Options
from .preprocessor import get_combined as prep_combined
from .styles import style_for_print
from .themes import generic as generic_theme
from .toc import make_indexes
from .utils.soup_util import clone_element


class Generator(object):

    def __init__(self, options: Options):
        self._options = options

        self._theme = self._load_theme_handler()
        self._nav = None
        self._head = None

    def on_nav(self, nav):
        """ on_nav """
        self._nav = nav
        if nav:
            self._options.logger.debug(f'theme: {self._theme}')

    def on_post_page(self, output_content: str, page, pdf_path: str) -> str:
        """ on_post_page """
        soup = self._soup_from_content(output_content, page)

        self._remove_empty_tags(soup)

        if not self._head:
            self._head = soup.find('head')
            # self.logger.debug(f'{self._head}')

        # for 'material'
        article = soup.find('article')
        if article:
            article = clone_element(article)

        # for 'mkdocs' theme
        if not article:
            main = soup.find('div', attrs={'role': 'main'})
            if main:
                article = soup.new_tag('article')
                for child in main.contents:
                    article.append(clone_element(child))

        if article:
            # remove 'headerlink' if exists.
            for a in article.find_all('a', attrs={'class': 'headerlink'}):
                a.decompose()

            if self._options.heading_shift:
                article = self._shift_heading(article, page, page.parent)

            article['data-url'] = f'/{page.url}'
            setattr(page, 'pdf-article', article)

        return self._theme.inject_link(output_content, pdf_path)

    def on_post_build(self, config, output_path):
        soup = BeautifulSoup(
            '<html><head></head><body></body></html>', 'html.parser')
        if self._head:
            soup.html.insert(0, self._head)

        def add_stylesheet(stylesheet: str):
            if stylesheet:
                style_tag = soup.new_tag('style')
                style_tag.string = stylesheet
                soup.head.append(style_tag)
            pass

        add_stylesheet(style_for_print(self._options))
        add_stylesheet(self._theme.get_stylesheet())

        for page in self._nav:
            self._add_content(soup, page)

        make_indexes(soup, self._options)
        make_cover(soup, self._options)

        if self._options.debug_html:
            print(f'{soup}')

        html = HTML(string=str(soup))
        render = html.render()

        abs_pdf_path = os.path.join(config['site_dir'], output_path)
        os.makedirs(os.path.dirname(abs_pdf_path), exist_ok=True)

        render.write_pdf(abs_pdf_path)

    # ------------------------
    def _remove_empty_tags(self, soup: PageElement):
        includes = ['article', 'p']
        while True:
            hit = False
            for x in soup.find_all():
                if x.name in includes and len(x.get_text(strip=True)) == 0:
                    # self.logger.debug(f'Strip: {x}')
                    x.extract()
                    hit = True
            if not hit:
                break

    def _shift_heading(self, article: PageElement, page, parent):
        if not parent:
            return article

        for i in range(7, 0, -1):
            while True:
                h = article.find(f'h{i}')
                if not h:
                    break
                h.name = f'h{i + 1}'

        if page == parent.children[0]:
            article = self._shift_heading(article, parent, parent.parent)

            id = page.url if (hasattr(page, 'url') and page.url) else ''
            id = id.strip('/').rstrip('/')
            id = id if id else str(uuid4())

            soup = BeautifulSoup('', 'html.parser')
            h1 = soup.new_tag('h1', id=f'{id}')
            h1.append(parent.title)
            article.insert(0, h1)

        return article

    def _soup_from_content(self, content: str, page):
        soup = BeautifulSoup(content, 'html.parser')

        try:
            abs_dest_path = page.file.abs_dest_path
            src_path = page.file.src_path
        except AttributeError:
            abs_dest_path = page.abs_output_path
            src_path = page.input_path

        path = os.path.dirname(abs_dest_path)
        os.makedirs(path, exist_ok=True)
        filename = os.path.splitext(os.path.basename(src_path))[0]
        base_url = urls.path2url(os.path.join(path, filename))

        return prep_combined(soup, base_url, page.file.url)

    def _add_content(self, soup: PageElement, page):
        article = getattr(page, 'pdf-article', None)
        if article:
            soup.body.append(article)
        if page.children:
            for c in page.children:
                self._add_content(soup, c)

    # -------------------------------------------------------------

    @property
    def logger(self) -> logging:
        return self._options.logger

    def _load_theme_handler(self):
        theme = self._options.theme_name
        custom_handler_path = self._options.theme_handler_path
        module_name = '.' + (theme or 'generic').replace('-', '_')
        if custom_handler_path:
            try:
                spec = spec_from_file_location(
                    module_name, os.path.join(
                        os.getcwd(), custom_handler_path))
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
            except FileNotFoundError as e:
                self.logger.error(
                    f'Could not load theme handler {theme}'
                    f' from custom directory "{custom_handler_path}": {e}')
                pass

        try:
            return import_module(module_name, 'mkdocs_with_pdf.themes')
        except ImportError as e:
            self.logger.error(f'Could not load theme handler {theme}: {e}')
            return generic_theme
