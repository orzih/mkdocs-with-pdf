import os
from urllib.parse import urljoin

from .util import is_doc


def transform_href(href: str, rel_url: str) -> str:
    """ Transform a href for single document.

    normalize href to #foo/bar/section:id

    Arguments:
        href {str} -- a linked URL string in document.
        rel_url {str} -- a current page URL(like a baseURL).

    Returns:
        str -- a replased URL string.
    """

    x_href = _transform_href(href, rel_url)

    ''' ...for DEBUG block. :FIXME: needs unit test.
    head, tail = os.path.split(href)
    import sys
    print(
        f'***** "{x_href}"\t\t"{href}",\t"{rel_url}"\t'
        f' -- ["{head}", "{tail}"]',
        file=sys.stderr)
    '''

    return x_href


def _transform_href(href: str, rel_url: str) -> str:
    # :FIXME: I want to be more simple implementation.

    head, tail = os.path.split(href)

    num_hashtags = tail.count('#')

    if tail.startswith('#'):

        id = tail[1:]
        if not id:
            id = '' if not rel_url.endswith('/') else rel_url.split('/')[-2]

        if rel_url == '.' and head == '':
            return f'#.:{id}'

        if head.endswith('.md'):
            head = _normalize_internal_href(head)
        else:
            head = _normalize_href(head, rel_url)
        section = ''

    elif num_hashtags == 1:

        section, ext = tuple(os.path.splitext(tail))
        id = str.split(ext, '#')[1]
        if head.startswith('..'):
            href = _normalize_href(href, rel_url)
            return f'#{href}:{id}'

    elif num_hashtags == 0:

        if tail == '' and not head.endswith('/'):
            return href
        elif head == '.' or rel_url == '.':
            if href.endswith('.png'):
                return href
            id = '' if not href.endswith('/') else href.split('/')[-2]
            return f'#{href}:{id}'
        elif href.startswith('..'):
            id = '' if not href.endswith('/') else href.split('/')[-2]
            href = _normalize_href(href, rel_url)
            return f'#{href}:{id}'
        elif not is_doc(href):
            return href

        href = _normalize_href(href, rel_url)
        return '#{}:'.format(href)

    if head != '' and not head.endswith('/') and not head.endswith('index'):
        head += '/'

    return '#{}{}:{}'.format(head, section, id)


def _normalize_href(href: str, rel_url: str) -> str:
    if href == '' and rel_url.endswith('index.html'):
        return rel_url.rsplit('.', 1)[0]
    return urljoin(rel_url, href)


def _normalize_internal_href(href: str) -> str:
    """
    normalized for the internal link (direct '.md' file link).

    convert to the embedded anchor-tag.

    + ignored all path and suffix information(using filename only).
    + considered to be the directory directly under the root.
    """

    filename = os.path.basename(href)
    if not filename:
        return href
    name, ext = os.path.splitext(filename)
    if not name or ext != '.md':
        return href
    return name + '/'


def transform_id(id: str, rel_url: str):
    """normalize id to foo/bar/section:id"""

    head, tail = os.path.split(rel_url)
    section, _ = os.path.splitext(tail)

    if len(head) > 0:
        head += '/'

    return '{}{}:{}'.format(head, section, id)
