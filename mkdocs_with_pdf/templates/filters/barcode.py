import base64
import io

import barcode

from . import _FilterBase


#
# @see https://pypi.org/project/python-barcode/
#

class Barcode(_FilterBase):
    """ Generate Barcode for given value and returns embedded image data. """

    # Support:
    # ['code39', 'code128', 'ean', 'ean13', 'ean8',
    #  'gs1', 'gtin', 'isbn',
    #  'isbn10', 'isbn13', 'issn', 'jan',
    #  'pzn', 'upc', 'upca']

    def __call__(self, value, kind, **kwargs):
        coder = barcode.get_barcode_class(kind)
        img = coder(value, writer=None, **kwargs)
        with io.BytesIO() as stream:
            img.write(stream, dict(compress=True))
            data = base64.b64encode(stream.getvalue())
            return 'data:image/svg+xml;charset=utf-8;base64,' + \
                data.decode("ascii")
