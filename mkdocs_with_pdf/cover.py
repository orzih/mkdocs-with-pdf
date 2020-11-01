from bs4 import PageElement, BeautifulSoup

from .options import Options


def make_cover(soup: PageElement, options: Options):
    """ Generate a cover page.

    Arguments:
        soup {BeautifulSoup} -- target element.
        options {Options} -- the project options.
    """

    if not options.cover:
        return

    try:
        keywords = options.template.keywords
        template = options.template.select(['cover', 'default_cover'])

        options.logger.info(f'Generate a cover page with "{template.name}".')
        soup_template = BeautifulSoup(template.render(keywords), 'html.parser')

        soup.body.insert(0, soup_template)
    except Exception as e:
        options.logger.error('Failed to generate the cover page: %s', e)
