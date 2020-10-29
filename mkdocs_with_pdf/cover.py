import os
import re
from bs4 import PageElement, BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import yaml

from .options import Options

def _get_context():
    with open('mkdocs.yml', 'r') as f:
        context = yaml.safe_load(f)
    
    # create a new key:value pair for each plugin for better handling in jinja templates
    # e.g. use `plugin_with_pdf["author"]` to get the author value from with-pdf plugin
    for plugin in context['plugins']:
        if isinstance(plugin, dict) and 'with-pdf' in plugin.keys():
            for plugin_name, plugin_values in plugin.items():
                plugin_key = re.sub('[^0-9a-zA-Z]+', '_', plugin_name)
                context['plugin_' + plugin_key] = plugin_values
                
    return context

def _gen_cover(soup: PageElement, options: Options):
    base_path = os.path.abspath(os.path.dirname(__file__))
    template_paths = [os.path.join(base_path, 'templates')]
    if os.path.exists(options.custom_template_path):
        template_paths.append(options.custom_template_path)

    file_loader = FileSystemLoader(template_paths)
    env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)
    template = env.select_template(['cover.html', 'default_cover.html'])
    soup_template = BeautifulSoup(template.render(_get_context()))
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
