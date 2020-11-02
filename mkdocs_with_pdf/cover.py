from bs4 import PageElement, BeautifulSoup

from .options import Options


def make_cover(soup: PageElement, options: Options):
    """ Generate a cover pages.

    Arguments:
        soup {BeautifulSoup} -- target element.
        options {Options} -- the project options.
    """

    if options.cover:
        _make_cover(soup, options)

    if options.back_cover:
        _make_back_cover(soup, options)


def _make_cover(soup: PageElement, options: Options):
    try:
        keywords = options.template.keywords
        template = options.template.select(['cover', 'default_cover'])

        options.logger.info(f'Generate a cover page with "{template.name}".')
        soup_template = BeautifulSoup(template.render(keywords), 'html.parser')

        soup.body.insert(0, soup_template)
    except Exception as e:
        options.logger.error('Failed to generate the cover page: %s', e)


def _make_back_cover(soup: PageElement, options: Options):
    try:
        keywords = options.template.keywords
        template = options.template.select(
            ['back_cover', 'default_back_cover'])

        options.logger.info(
            f'Generate a back cover page with "{template.name}".')
        soup_template = BeautifulSoup(template.render(keywords), 'html.parser')

        soup.body.append(soup_template)
    except Exception as e:
        options.logger.error('Failed to generate the back cover page: %s', e)
