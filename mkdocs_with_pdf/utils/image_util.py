from logging import Logger
from bs4 import PageElement, Tag


def fix_image_alignment(soup: PageElement, logger: Logger = None):
    """ (workaraound) convert <img align=*> to `float` style.
    and, move <img width=*>, <image height=*> to style attributes.
    """

    if logger:
        logger.info('Converting <img> alignment(workaround).')

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


def images_size_to_half_in(section: Tag):

    def _split(s):
        for i, c in enumerate(s):
            if not c.isdigit():
                break
        number = s[:i]
        unit = s[i:].lstrip()
        return (number, unit)

    for img in section.find_all('img'):
        if not img.has_attr('style'):
            continue
        styles = _parse_style(img['style'])
        if not len(styles):
            continue

        for key in ['width', 'height', 'padding-left', 'padding-right']:
            if key in styles:
                (dim, u) = _split(styles[key])
                styles[key] = str(int(dim) / 2) + u
        img['style'] = " ".join(f'{k}: {v};' for k, v in styles.items())


def _parse_style(style_string: str) -> dict:
    styles = {}
    if style_string:
        for attr in style_string.split(';'):
            if not len(attr):
                continue
            val = attr.split(':', 2)
            styles[val[0].strip()] = val[1].strip()
    return styles


def _convert_dimension(dim_str: str) -> str:
    if dim_str.isdecimal():
        return dim_str + 'px'
    return dim_str
