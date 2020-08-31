import os
from logging import Logger
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile


def render_js(html: str, logger: Logger = None) -> str:

    temp = NamedTemporaryFile(delete=False, suffix='.html')
    try:
        temp.write(html.encode('utf-8'))
        temp.close()

        if logger:
            logger.info("Rendering by JS using `headless chrome`")

        with Popen(['google-chrome', '--headless', '--disable-gpu',
                    '--dump-dom',
                    temp.name], stdout=PIPE) as chrome:
            return chrome.stdout.read().decode('utf-8')

    except Exception as e:
        if logger:
            logger.error(f'Failed to render by JS: {e}')
    finally:
        os.unlink(temp.name)

    return html
