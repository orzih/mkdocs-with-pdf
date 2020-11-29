import html
import os

import sass

from ..options import Options


def _css_escape(text: str) -> str:
    """ @see https://developer.mozilla.org/en-US/docs/Web/CSS/string """

    if not text:
        return ''

    text = html.unescape(text)

    # -- probably not needed.
    # text = text.encode('unicode-escape').decode('ascii').replace('\\u', '\\')

    return text.replace("'", '\\27')


def style_for_print(options: Options) -> str:
    scss = f"""
    :root {{
        string-set: author '{_css_escape(options.author)}',
            copyright '{_css_escape(options.copyright)}',
            title '{_css_escape(options.cover_title)}';
    }}
    h1, h2, h3 {{
        string-set: chapter content();
    }}
    """
    css = sass.compile(string=scss)

    base_path = os.path.abspath(os.path.dirname(__file__))

    filename = os.path.join(base_path, "report-print.scss")
    css += sass.compile(filename=filename)

    if options.cover or options.back_cover:
        filename = os.path.join(base_path, "cover.scss")
        css += sass.compile(filename=filename)

    filename = os.path.join(options.custom_template_path, 'styles.scss')
    if os.path.exists(filename):
        css += sass.compile(filename=filename)

    return css
