from logging import Logger
from bs4 import PageElement


def fix_image_alignment(soup: PageElement, logger: Logger = None):
    """ (workaraound) convert <img align=*> to `float` style.
    and, move <img width=*>, <image height=*> to style attributes.
    """

    if logger:
        logger.debug('Converting img align(workaround).')

    for img in soup.select('img'):
        try:
            if img.has_attr('class') and 'twemoji' in img['class']:
                continue

            styles = _parse_style(getattr(img, 'style', ''))

            logger.debug(f'  | {img}')
            if img.has_attr('align'):
                if img['align'] == 'left':
                    styles['float'] = 'left'
                    styles['padding-right'] = '1rem'
                    styles['padding-bottom'] = '0.5rem'
                    img.attrs.pop('align')
                elif img['align'] == 'right':
                    styles['float'] = 'right'
                    styles['padding-left'] = '1rem'
                    styles['padding-bottom'] = '0.5rem'
                    img.attrs.pop('align')

            if img.has_attr('width'):
                styles['width'] = _convert_dimension(img['width'])
                img.attrs.pop('width')
            if img.has_attr('height'):
                styles['height'] = _convert_dimension(img['height'])
                img.attrs.pop('height')

            img['style'] = " ".join(f'{k}: {v};' for k, v in styles.items())
        except Exception as e:
            if logger:
                logger.warning(f'Failed to convert img align: {e}')
            pass


def _parse_style(style_string: str) -> dict:
    styles = {}
    if style_string:
        for attr in style_string.split(';'):
            val = attr.split(':', 2)
            styles[val[0]] = val[1]
    return styles


def _convert_dimension(dim_str: str) -> str:
    if dim_str.isdecimal():
        return dim_str + 'px'
    return dim_str
