import os
from urllib.parse import urlparse

from . import _FilterBase


class URLFilter(_FilterBase):
    """ Finds a matching filename in some directories and returns its URL. """

    def __call__(self, pathname: str) -> str:
        if not pathname:
            return ''

        # Check for URL(eg. 'https://...')
        target_url = urlparse(pathname)
        if target_url.scheme or target_url.netloc:
            return pathname

        # Search image file in below directories:
        dirs = [
            self.options.custom_template_path,
            getattr(self.config['theme'], 'custom_dir', None),
            self.config['docs_dir'],
            '.'
        ]

        for d in dirs:
            if not d:
                continue
            path = os.path.abspath(os.path.join(d, pathname))
            if os.path.isfile(path):
                return 'file://' + path

        # not found?
        return pathname
