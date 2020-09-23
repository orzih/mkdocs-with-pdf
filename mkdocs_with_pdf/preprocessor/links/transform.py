import os
import re
from urllib.parse import (urljoin, urlparse, quote)


def transform_href(href: str, rel_url: str) -> str:
    """ Transform a href for single document.

    normalize href to #foo/bar/section:id

    Arguments:
        href {str} -- a linked URL string in document.
        rel_url {str} -- a current page URL(like a baseURL).

    Returns:
        str -- a replased URL string.
    """

    def transform():
        target_url = urlparse(href)

        if target_url.scheme or target_url.netloc:
            # do not care, will be not reachable
            return href

        hash = target_url.fragment
        target = urljoin(rel_url, target_url.path)

        if target in ['/', '.', 'index.html']:
            return f'#.:{hash}'

        if target.endswith('.png'):
            return href
        elif target.endswith('index.html'):
            target = re.sub(r'index\.html$', '', target)
        else:
            target = re.sub(r'\.(html|md)$', '/', target)

        if not target.endswith('/'):
            target += '/'

        return f'#{quote(target)}:{hash}'

    x_href = transform()

    ''' ...for DEBUG block. :FIXME: needs unit test.
    head, tail = os.path.split(href)
    import sys
    print(
        f'***** "{x_href}"\t\t"{href}",\t"{rel_url}"\t'
        f' -- ["{head}", "{tail}"]',
        file=sys.stderr)
    '''
    '''
    import sys
    print(f"[ ['{href}', '{rel_url}'], '{x_href}'],", file=sys.stderr)
    '''

    return x_href


def transform_id(id: str, rel_url: str):
    """normalize id to foo/bar/section:id"""

    if rel_url in ['.', 'index.html']:
        return f'.:{id}'

    head, tail = os.path.split(rel_url)
    section, _ = os.path.splitext(tail)

    def normalize(path):
        if len(path) == 0 or path in ['index']:
            return ''
        else:
            return path + '/'

    head = normalize(head)
    section = normalize(section)

    return f'{head}{section}:{id}'
