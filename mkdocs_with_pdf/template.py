import os

import jinja2
from mkdocs.config.base import Config


class Template(object):

    """ Pickups key-value from `mkdocs.yml` """
    __KEYS = [
        "author", "copyright",
        "cover_title", "cover_subtitle", "logo_url",

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
        if not self._jinja_env:
            base_path = os.path.abspath(os.path.dirname(__file__))
            template_paths = [os.path.join(base_path, 'templates')]

            if os.path.exists(self._options.custom_template_path):
                template_paths.append(self._options.custom_template_path)

            file_loader = jinja2.FileSystemLoader(template_paths)
            logging_undefined = jinja2.make_logging_undefined(
                logger=self._options.logger, base=jinja2.Undefined)
            self._jinja_env = jinja2.Environment(
                loader=file_loader,
                undefined=logging_undefined,
                lstrip_blocks=True,
                trim_blocks=True)
        return self._jinja_env

    @property
    def keywords(self) -> dict:
        """ Keywords to pass when rendering the template. """

        def build_keywords():
            # keywords = {}
            keywords = self._config['extra']

            for key in self.__KEYS:
                if hasattr(self._options, key):
                    keywords[key] = getattr(self._options, key)
                elif hasattr(self._config, key):
                    keywords[key] = getattr(self._config, key)
            if self._options.verbose or self._options.debug_html:
                self._options.logger.info(f'Template variables: {keywords}')
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
