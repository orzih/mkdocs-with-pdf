from logging import Logger
from bs4 import PageElement


def convert_iframe(soup: PageElement, entries: list, logger: Logger = None):
    """Replace iFrame to a(anchor)

    e.g:
        ```html "before:"
        <iframe frameborder="0" height="100%" src="SRC"/>
        ```

        ```html "after:"
        <a class="converted-iframe" href="SRC" target="_blank">
          <img src="POSTER IMAGE"/>
        </a>
        ```
    """

    for iframe in soup.find_all('iframe', src=True):
        for entry in entries:
            if iframe['src'] != entry.get('src'):
                continue

            a = soup.new_tag('a', href=iframe['src'], target='_blank',
                             **{'class': 'converted-iframe'})
            img_src = entry.get('img')
            if img_src:
                a.append(soup.new_tag('img', src=img_src))
            text = entry.get('text')
            if text:
                span = soup.new_tag('span')
                span.string = text
                a.append(span)

            # copy attributes
            for key, val in iframe.attrs.items():
                if key in ['style']:
                    a[key] = val

            iframe.replace_with(a)
