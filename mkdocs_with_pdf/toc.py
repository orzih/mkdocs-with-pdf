from dataclasses import dataclass, field
from typing import Any, List, Tuple
from bs4 import BeautifulSoup, Tag

from .options import Options
from .utils.soup_util import clone_element


_MAX_HEADER_LEVEL = 6  # <h1> ... <h6>


@dataclass
class _HeaderTree:
    """ Normalized tree of document headers. Missed levels have `element` set to `None` """
    element: Tag | None
    subheaders: List['_HeaderTree'] = field(default_factory=list)


def make_indexes(soup: BeautifulSoup, options: Options) -> None:
    """ Generate ordered chapter number and TOC of document.

    Arguments:
        soup {BeautifulSoup} -- DOM object of Document.
        options {Options} -- The options of this sequence.
    """

    # Step 1: (re)ordered headings
    _inject_heading_order(soup, options)

    # Step 2: generate toc page
    start_level = 1 if options.ignore_top_header else 0
    stop_level = options.toc_level
    if stop_level <= start_level:
        return
    if stop_level > _MAX_HEADER_LEVEL:
        options.logger.warning(f'Ignore `toc_level` value {stop_level}. Use max possible {_MAX_HEADER_LEVEL} instead')
        stop_level = _MAX_HEADER_LEVEL

    options.logger.info(f'Generate a table of contents from h{start_level + 1} to h{stop_level}')

    def make_link(h: Tag) -> Tag:
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

    def create_toc(headers: List[_HeaderTree], parent: Tag):
        ul_tag = soup.new_tag('ul')
        parent.append(ul_tag)
        for header in headers:
            if header.element is not None:
                link_tag = make_link(header.element)
            else:
                options.logger.warning(f'Adding missed header to TOC')
                link_tag = soup.new_tag('li')
            ul_tag.append(link_tag)
            if len(header.subheaders) > 0:
                create_toc(header.subheaders, link_tag)

    top_headers = _collect_headers(soup, options, start_level, stop_level)

    toc = soup.new_tag('article', id='doc-toc')
    title = soup.new_tag('h1')
    title.append(soup.new_string(options.toc_title))
    toc.append(title)

    create_toc(top_headers, toc)
    soup.body.insert(0, toc)


def _set_list_elements(l: List[Any], value: Any, start: int, end: int | None = None) -> None:
    for i in range(start, end if end is not None else len(l)):
        l[i] = value


def _collect_headers(soup: BeautifulSoup, options: Options, start_level: int, stop_level: int) -> List[_HeaderTree]:
    """Collect document headers.
    Retuns a list of top headers with their subheaders
    Levels are counted from zero i.e. zero level corresponds to h1
    """
    assert 0 <= start_level < stop_level
    assert 0 < stop_level <= _MAX_HEADER_LEVEL

    top_headers: List[_HeaderTree] = []

    header_levels: List[_HeaderTree | None] = [None] * stop_level
    exclude_levels: List[bool] = [False] * stop_level

    html_headers = soup.find_all([f'h{i + 1}' for i in range(start_level, stop_level)])
    for h in html_headers:
        level = int(h.name[1:]) - 1

        exclude_levels[level] = _is_exclude(h.get('id', None), options)
        _set_list_elements(exclude_levels, False, level + 1)

        if any(exclude_levels[:level]):
            continue

        header = _HeaderTree(h)

        if level == start_level:
            top_headers.append(header)
        else:
            parent_header = header_levels[level - 1]
            if parent_header is None:
                # Add skipped levels
                for i in range(start_level, level):
                    if header_levels[i] is not None:
                        continue

                    missed_header = _HeaderTree(None)
                    if i == start_level:
                        top_headers.append(missed_header)
                    else:
                        parent_header = header_levels[i - 1]
                        assert parent_header is not None
                        parent_header.subheaders.append(missed_header)
                    header_levels[i] = missed_header

                parent_header = header_levels[level - 1]

            assert parent_header is not None
            parent_header.subheaders.append(header)

        header_levels[level] = header
        _set_list_elements(header_levels, None, level + 1)

    return top_headers


def _inject_heading_order(soup: BeautifulSoup, options: Options) -> None:
    start_level = 1 if options.ignore_top_header else 0
    stop_level = options.ordered_chapter_level
    if stop_level <= start_level:
        return
    if stop_level > _MAX_HEADER_LEVEL:
        options.logger.warning(f'Ignore `ordered_chapter_level` value {stop_level}. Use max possible {_MAX_HEADER_LEVEL} instead')
        stop_level = _MAX_HEADER_LEVEL

    options.logger.info(f'Number headers from h{start_level + 1} to h{stop_level}')

    def inject_order(headers: List[_HeaderTree], numbers_prefix: List[int] = []):
        assert len(numbers_prefix) < _MAX_HEADER_LEVEL
        for i, header in enumerate(headers):
            prefix = numbers_prefix + [i + 1]
            prefix_str = '.'.join(str(n) for n in prefix)
            if header.element is not None:
                options.logger.debug(f"| [{prefix_str} {header.element}]({header.element.get('id', '(none)')})")
                nm_tag = soup.new_tag('span', **{'class': 'pdf-order'})
                nm_tag.append(prefix_str + ' ')
                header.element.insert(0, nm_tag)
            else:
                options.logger.warning(f'Assigned number for a missed header {prefix_str}')
            if len(header.subheaders) > 0:
                inject_order(header.subheaders, prefix)

    top_headers = _collect_headers(soup, options, start_level, stop_level)
    inject_order(top_headers)


def _is_exclude(url: str, options: Options) -> bool:
    if not url:
        return False

    if url in options.excludes_children:
        options.logger.info(f"|  (exclude '{url}')")
        return True

    return False
