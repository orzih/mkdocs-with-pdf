from bs4 import PageElement

from .options import Options


def make_cover(soup: PageElement, options: Options):
    """ Generate a cover page.

    Arguments:
        soup {BeautifulSoup} -- target element.
        options {Options} -- the project options.
    """

    if not options.cover:
        return

    options.logger.info('Generate a cover page.')

    article = soup.new_tag('article', id='doc-cover')

    d = soup.new_tag('div', **{'class': 'wrapper'})
    article.append(d)

    box = soup.new_tag('div', **{'class': 'wrapper'})
    article.append(box)

    title = options.cover_title
    h1 = soup.new_tag('h1')
    h1.append(title)
    box.append(h1)

    sub_title = options.cover_subtitle
    if sub_title:
        h2 = soup.new_tag('h2')
        h2.append(sub_title)
        box.append(h2)

    article.append(_gen_address(soup, options))

    soup.body.insert(0, article)


def _gen_address(soup: PageElement, options: Options) -> PageElement:

    box = soup.new_tag('div', **{'class': 'properties'})

    address = soup.new_tag('address')
    box.append(address)

    if options.author:
        span = soup.new_tag('p', id="author")
        span.append(options.author)
        address.append(span)

    if options.copyright:
        span = soup.new_tag('p', id="copyright")
        import html
        span.append(html.unescape(options.copyright))
        address.append(span)

    return box
