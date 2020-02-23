import os

from weasyprint import urls
from bs4 import PageElement


def is_doc(href: str) -> bool:
    """check if href is relative

    if it is relative it *should* be an html that generates a PDF doc

    Arguments:
        href {str} -- a string of URL.

    Returns:
        bool -- result
    """

    tail = os.path.basename(href)
    _, ext = os.path.splitext(tail)

    absurl = urls.url_is_absolute(href)
    abspath = os.path.isabs(href)
    htmlfile = ext.startswith('.html')
    if absurl or abspath or not htmlfile:
        return False

    return True


def rel_pdf_href(href: str):
    head, tail = os.path.split(href)
    filename, _ = os.path.splitext(tail)

    internal = href.startswith('#')
    if not is_doc(href) or internal:
        return href

    return urls.iri_to_uri(os.path.join(head, filename + '.pdf'))


def abs_asset_href(href: str, base_url: str):
    if urls.url_is_absolute(href) or os.path.isabs(href):
        return href

    return urls.iri_to_uri(urls.urljoin(base_url, href))


def replace_asset_hrefs(soup: PageElement, base_url: str) -> PageElement:
    """makes all relative asset links absolute"""

    for link in soup.find_all('link', href=True):
        link['href'] = abs_asset_href(link['href'], base_url)

    for asset in soup.find_all(src=True):
        asset['src'] = abs_asset_href(asset['src'], base_url)

    return soup


def get_body_id(url: str):
    section, _ = os.path.splitext(url)
    return '{}:'.format(section)
