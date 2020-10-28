import os
from bs4 import PageElement, BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import yaml

from .options import Options

def _gen_cover(soup: PageElement, options: Options):
    base_path = os.path.abspath(os.path.dirname(__file__))
    template_paths = [os.path.join(base_path, 'templates')]
    if os.path.exists(options.custom_template_path):
        template_paths.append(options.custom_template_path)

    with open('mkdocs.yml', 'r') as f:
        context = yaml.safe_load(f)

    file_loader = FileSystemLoader(template_paths)
    env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)
    template = env.select_template(['cover.html', 'default_cover.html'])
    soup_template = BeautifulSoup(template.render(context))
    soup.body.insert(0, soup_template)

def make_cover(soup: PageElement, options: Options):
    """ Generate a cover page.

    Arguments:
        soup {BeautifulSoup} -- target element.
        options {Options} -- the project options.
    """

    if not options.cover:
        return

    options.logger.info('Generate a cover page.')

    _gen_cover(soup, options)
