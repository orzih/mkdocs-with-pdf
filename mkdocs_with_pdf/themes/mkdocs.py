import os

import sass
from bs4 import BeautifulSoup


def get_stylesheet(debug_html: bool) -> str:
    base_path = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(base_path, "mkdocs.scss")
    return sass.compile(filename=filename)


def get_script_sources() -> list:
    return []


def inject_link(html: str, href: str) -> str:

    soup = BeautifulSoup(html, 'html.parser')
    if soup.head:
        link = soup.new_tag('link', href=href, rel='alternate',
                            title='PDF', type='application/pdf')
        soup.head.append(link)
        return str(soup)

    return html
