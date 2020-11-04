from bs4 import PageElement, Tag

from .options import Options
from .utils.soup_util import clone_element


def make_indexes(soup: PageElement, options: Options) -> None:
    """ Generate ordered chapter number and TOC of document.

    Arguments:
        soup {BeautifulSoup} -- DOM object of Document.
        options {Options} -- The options of this sequence.
    """

    # Step 1: (re)ordered headdings
    _inject_heading_order(soup, options)

    # Step 2: generate toc page
    level = options.toc_level
    if level < 1 or level > 3:
        return

    options.logger.info(
        f'Generate a table of contents up to heading level {level}.')

    h1li = None
    h2ul = h2li = h3ul = None
    exclude_lv2 = exclude_lv3 = False

    def makeLink(h: Tag) -> Tag:
        li = soup.new_tag('li')
        ref = h.get('id', '')
        a = soup.new_tag('a', href=f'#{ref}')
        for el in h.contents:
            if el.name == 'a':
                a.append(el.contents[0])
            else:
                a.append(clone_element(el))
        li.append(a)
        options.logger.debug(f"| [{h.get_text(separator=' ')}]({ref})")
        return li

    toc = soup.new_tag('article', id='doc-toc')
    title = soup.new_tag('h1')
    title.append(soup.new_string(options.toc_title))
    toc.append(title)

    h1ul = soup.new_tag('ul')
    toc.append(h1ul)

    headings = soup.find_all(['h1', 'h2', 'h3'])
    for h in headings:

        if h.name == 'h1':

            h1li = makeLink(h)
            h1ul.append(h1li)
            h2ul = h2li = h3ul = None

            exclude_lv2 = _is_exclude(h.get('id', None), options)

        elif not exclude_lv2 and h.name == 'h2' and level >= 2:

            if not h2ul:
                h2ul = soup.new_tag('ul')
                h1li.append(h2ul)
            h2li = makeLink(h)
            h2ul.append(h2li)
            h3ul = None

            exclude_lv3 = _is_exclude(h.get('id', None), options)

        elif not exclude_lv2 and not exclude_lv3 \
                and h.name == 'h3' and level >= 3:

            if not h2li:
                continue
            if not h3ul:
                h3ul = soup.new_tag('ul')
                h2li.append(h3ul)
            h3li = makeLink(h)
            h3ul.append(h3li)

        else:
            continue
        pass

    soup.body.insert(0, toc)


def _inject_heading_order(soup: Tag, options: Options):

    level = options.ordered_chapter_level
    if level < 1 or level > 3:
        return

    options.logger.info(f'Number headings up to level {level}.')

    h1n = h2n = h3n = 0
    exclude_lv2 = exclude_lv3 = False

    headings = soup.find_all(['h1', 'h2', 'h3'])
    for h in headings:

        if h.name == 'h1':

            h1n += 1
            h2n = h3n = 0
            prefix = f'{h1n}. '

            exclude_lv2 = _is_exclude(h.get('id', None), options)

        elif not exclude_lv2 and h.name == 'h2' and level >= 2:

            h2n += 1
            h3n = 0
            prefix = f'{h1n}.{h2n} '

            exclude_lv3 = _is_exclude(h.get('id', None), options)

        elif not exclude_lv2 and not exclude_lv3 \
                and h.name == 'h3' and level >= 3:

            h3n += 1
            prefix = f'{h1n}.{h2n}.{h3n} '

        else:
            continue

        options.logger.debug(f"| [{prefix} {h.text}]({h.get('id', '(none)')})")

        nm_tag = soup.new_tag('span', **{'class': 'pdf-order'})
        nm_tag.append(prefix)
        h.insert(0, nm_tag)


def _is_exclude(url: str, options: Options) -> bool:
    if not url:
        return False

    if url in options.excludes_children:
        options.logger.info(f"|  (exclude '{url}')")
        return True

    return False
