import itertools
from logging import Logger

from bs4 import PageElement


def convert_for_two_columns(soup: PageElement,
                            level: int,
                            logger: Logger = None):
    if level != 3:
        logger.warning('`two_columns_level` is only support `3` yet.')
        return

    ignored = []
    for el in soup.find_all('h3'):
        if el in ignored:
            continue
        els = [i for i in itertools.takewhile(
            lambda x: x.name not in ['h1', 'h2'],
            el.next_siblings)]
        section = soup.new_tag('section', **{'class': 'two-columns'})
        el.wrap(section)
        for tag in els:
            section.append(tag)
            if tag.name == 'h3':
                ignored.append(tag)
