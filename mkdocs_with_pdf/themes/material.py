import os

import sass
from bs4 import BeautifulSoup


def get_stylesheet(debug_html: bool) -> str:
    base_path = os.path.abspath(os.path.dirname(__file__))
    style = ""
    for src in ["material.scss", "material-polyfills.css"]:
        filename = os.path.join(base_path, src)
        style += sass.compile(filename=filename)
    return style


def get_script_sources() -> list:
    base_path = os.path.abspath(os.path.dirname(__file__))
    return list(map(lambda src: os.path.join(base_path, src),
                    ['material-polyfills.js']))


def inject_link(html: str, href: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    footer = soup.select('.md-footer-copyright')
    if footer and footer[0]:
        container = footer[0]

        container.append(' ... ')
        a = soup.new_tag('a', href=href, title='PDF',
                         download=None, **{'class': 'link--pdf-download'})
        a.append('download PDF')

        container.append(a)

        return str(soup)

    return html
