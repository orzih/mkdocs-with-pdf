import itertools
from logging import Logger

from bs4 import PageElement


def wrap_tabbed_set_content(soup: PageElement, logger: Logger = None):
    for ts in soup.select('div.tabbed-set'):
        for radio in ts.select('input'):
            els = [i for i in itertools.takewhile(
                lambda x: x.name not in ['input'],
                radio.next_siblings)]
            wrapper = soup.new_tag('div', **{'class': 'tabbed-content--wrap'})
            radio.wrap(wrapper)
            for tag in els:
                wrapper.append(tag)

    for d in soup.select('details'):
        d['open'] = ''
