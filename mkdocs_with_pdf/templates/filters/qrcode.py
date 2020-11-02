import base64
import io

import qrcode
import qrcode.image.svg

from . import _FilterBase


#
# @see https://pypi.org/project/qrcode/
#

class QRCode(_FilterBase):
    """ Generate QRCode for given value and returns embedded image data. """

    def __call__(self, value, format='SVG'):
        if format.upper() == 'PNG':
            return self._to_png(value)
        else:
            return self._to_svg(value)

    def _to_svg(self, value):
        with io.BytesIO() as stream:
            img = qrcode.make(
                value,
                image_factory=qrcode.image.svg.SvgImage)
            stream = io.BytesIO()
            img.save(stream)
            data = base64.b64encode(stream.getvalue())
            return 'data:image/svg;base64,' + data.decode("ascii")

    def _to_png(self, value):
        with io.BytesIO() as stream:
            img = qrcode.make(value)
            img.save(stream, 'PNG')
            data = base64.b64encode(stream.getvalue())
            return 'data:image/png;base64,' + data.decode("ascii")

    def _with_icon(self, content, icon_path):
        """ generate QRCode with an icon in the center

        Args:
            content (str): the content encoded in QRCode
            icon_path (str): the path of icon image
        """

        import os
        from PIL import Image

        if not os.path.exists(icon_path):
            raise f"No such file {icon_path}"

        # first, generate an usual qr code image
        maker = qrcode.qrcode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=1)
        maker.add_data(data=content)
        maker.make(fit=True)
        img = maker \
            .make_image(fill_color="black", back_color="white") \
            .convert("rgba")

        # second, load icon image and resize it
        icon_img = Image.open(icon_path)
        code_width, code_height = img.size
        icon_img = icon_img.resize(
            (code_width / 4, code_height / 4), Image.antialias)

        # last, add the icon to original qr code
        img.paste(icon_img, (code_width * 3 / 8, code_width * 3 / 8))

        with io.BytesIO() as stream:
            img.save(stream, 'PNG')
            data = base64.b64encode(stream.getvalue())
            return 'data:image/png;base64,' + data.decode("ascii")
