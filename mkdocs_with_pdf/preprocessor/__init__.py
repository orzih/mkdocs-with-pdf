import os

from bs4 import PageElement
from weasyprint import urls

from .links.transform import transform_href, transform_id
from .links.util import get_body_id, rel_pdf_href, replace_asset_hrefs


def get_combined(
        soup: PageElement,
        base_url: str,
        rel_url: str) -> PageElement:
    """ transforms all relative hrefs pointing to other html docs
    into relative pdf hrefs
    """

    for element in soup.find_all(id=True):
        element['id'] = transform_id(element['id'], rel_url)

    for a in soup.find_all('a', href=True):
        if urls.url_is_absolute(a['href']) or os.path.isabs(a['href']):
            continue

        a['href'] = transform_href(a['href'], rel_url)

    soup.body['id'] = get_body_id(rel_url)
    soup = replace_asset_hrefs(soup, base_url)

    return soup


def get_separate(soup: PageElement, base_url: str) -> PageElement:
    for a in soup.find_all('a', href=True):
        a['href'] = rel_pdf_href(a['href'])

    soup = replace_asset_hrefs(soup, base_url)
    return soup
