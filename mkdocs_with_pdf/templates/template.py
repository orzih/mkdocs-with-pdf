import os
from datetime import datetime

import jinja2
from mkdocs.config.base import Config

from .filters.datetime import strftime, strptime
from .filters.url import URLFilter

try:
    from .filters.barcode import Barcode
except ModuleNotFoundError:
    Barcode = None
try:
    from .filters.qrcode import QRCode
except ModuleNotFoundError:
    QRCode = None


class Template(object):

    """ Pickups key-value from `mkdocs.yml` """
    __KEYS = [
        "author", "copyright",
        "cover_title", "cover_subtitle", "cover_logo",

        "site_url",
        "repo_url"
    ]

    def __init__(self, options: object, config: Config):
        self._options = options
        self._config = config

        self._keywords = None
        self._jinja_env = None

    @property
    def _env(self) -> jinja2.Environment:

        def generate():
            base_path = os.path.abspath(os.path.dirname(__file__))
            template_paths = [os.path.join(base_path, '.')]

            if os.path.exists(self._options.custom_template_path):
                template_paths.append(self._options.custom_template_path)

            file_loader = jinja2.FileSystemLoader(template_paths)
            logging_undefined = jinja2.make_logging_undefined(
                logger=self._options.logger, base=jinja2.Undefined)
            env = jinja2.Environment(
                loader=file_loader,
                undefined=logging_undefined,
                lstrip_blocks=True,
                trim_blocks=True)

            env.filters['strptime'] = strptime
            env.filters['strftime'] = strftime

            env.filters['to_url'] = URLFilter(self._options, self._config)

            if Barcode:
                env.filters['barcode'] = Barcode(self._options, self._config)
            if QRCode:
                env.filters['qrcode'] = QRCode(self._options, self._config)

            return env

        if not self._jinja_env:
            self._jinja_env = generate()
        return self._jinja_env

    @property
    def keywords(self) -> dict:
        """ Keywords to pass when rendering the template. """

        import html

        def unescape_html_in_list(values: list) -> list:
            new_values = []
            for v in values:
                if isinstance(v, str):
                    new_values.append(html.unescape(v))
                elif isinstance(v, list):
                    new_values.append(unescape_html_in_list(v))
                elif isinstance(v, dict):
                    unescape_html(v)
                    new_values.append(v)
                else:
                    new_values.append(v)
            return new_values

        def unescape_html(variables: dict):
            for k, v in variables.items():
                if isinstance(v, str):
                    variables[k] = html.unescape(v)
                elif isinstance(v, list):
                    variables[k] = unescape_html_in_list(v)
                elif isinstance(v, dict):
                    unescape_html(v)

        def build_keywords():
            # keywords = {}
            keywords = self._config['extra']

            for key in self.__KEYS:
                if hasattr(self._options, key):
                    keywords[key] = getattr(self._options, key)
                elif key in self._config:
                    keywords[key] = self._config[key]

            unescape_html(keywords)

            keywords['now'] = datetime.now()

            if self._options.verbose or self._options.debug_html:
                from pprint import pformat
                self._options.logger.info('Template variables:')
                for line in pformat(keywords).split('\n'):
                    self._options.logger.info('  ' + line)

            return keywords

        if not self._keywords:
            self._keywords = build_keywords()

        return self._keywords

    def select(
        self, names: [str], parent=None, globals=None
    ) -> jinja2.Template:
        """ Find and load a template by names of given. """

        real_names = []
        for name in names:
            for ext in ['.html.j2', '.html.jinja2', '.html', '.htm']:
                real_names.append(name + ext)

        return self._env.select_template(
            real_names, parent=parent, globals=globals)
