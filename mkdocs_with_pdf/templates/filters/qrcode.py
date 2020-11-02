import base64
import io
from enum import Enum

import qrcode
import qrcode.image.svg

from . import _FilterBase

#
# @see https://pypi.org/project/qrcode/
#


class _Format(Enum):
    SVG = 1
    PNG = 2


def _parse_format(format: str) -> _Format:
    if format.upper() == 'PNG':
        return _Format.PNG
    return _Format.SVG


def _parse_error_correction(error_correction: str):
    if error_correction:
        lv = error_correction.upper()
        if lv.startswith('Q'):
            return qrcode.constants.ERROR_CORRECT_Q
        elif lv.startswith('H'):
            return qrcode.constants.ERROR_CORRECT_H
        elif lv.startswith('L'):
            return qrcode.constants.ERROR_CORRECT_L
    return qrcode.constants.ERROR_CORRECT_M


def _image_factory(fmt: _Format):
    if fmt == _Format.PNG:
        return None
    return qrcode.image.svg.SvgPathImage


def _save_kind(fmt: _Format):
    if fmt == _Format.PNG:
        return 'PNG'
    return 'SVG'


def _content_type(fmt: _Format) -> str:
    if fmt == _Format.PNG:
        return 'image/png'
    return 'image/svg+xml;charset=utf-8'


class QRCode(_FilterBase):
    """ Generate QRCode for given value and returns embedded image data. """

    def __call__(self, content: str, format='SVG',
                 version=None,
                 error_correction=None,
                 box_size=10, border=4,
                 mask_pattern=None,
                 optimize=20):

        fmt = _parse_format(format)

        maker = qrcode.QRCode(
            version=version,
            error_correction=_parse_error_correction(error_correction),
            box_size=box_size,
            border=border,
            image_factory=_image_factory(fmt),
            mask_pattern=mask_pattern)
        maker.add_data(content, optimize=optimize)
        img = maker.make_image()

        with io.BytesIO() as stream:
            img.save(stream, kind=_save_kind(fmt))
            data = base64.b64encode(stream.getvalue())
            return f'data:{_content_type(fmt)};base64,' + data.decode("ascii")
