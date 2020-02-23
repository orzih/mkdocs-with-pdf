import os
import sass

from ..options import Options


def style_for_print(options: Options) -> str:
    scss = f"""
    :root {{
        string-set: author '{options.author}';
        string-set: copyright '{options.copyright}';
    }}
    h1, h2, h3 {{
        string-set: chapter content();
    }}
    """
    root = sass.compile(string=scss)

    base_path = os.path.abspath(os.path.dirname(__file__))

    filename = os.path.join(base_path, "report-print.scss")
    for_printing = sass.compile(filename=filename, output_style='compressed')

    if options.cover:
        filename = os.path.join(base_path, "cover.scss")
        for_cover = sass.compile(filename=filename, output_style='compressed')
    else:
        for_cover = ''

    return root + for_printing + for_cover
