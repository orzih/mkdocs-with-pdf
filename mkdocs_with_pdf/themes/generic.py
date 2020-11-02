from bs4 import BeautifulSoup


def get_stylesheet(debug_html: bool) -> str:
    return None


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
