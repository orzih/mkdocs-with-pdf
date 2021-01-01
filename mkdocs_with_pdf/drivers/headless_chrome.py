import os
from logging import Logger
from shutil import which
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile


class HeadlessChromeDriver(object):
    """ 'Headless Chrome' executor """

    @classmethod
    def setup(self, program_path: str, logger: Logger):
        if not which(program_path):
            raise RuntimeError(
                'No such `Headless Chrome` program or not executable'
                + f': "{program_path}".')
        return self(program_path, logger)

    def __init__(self, program_path: str, logger: Logger):
        self._program_path = program_path
        self._logger = logger

    def render(self, html: str) -> str:
        temp = NamedTemporaryFile(delete=False, suffix='.html')
        try:
            temp.write(html.encode('utf-8'))
            temp.close()

            self._logger.info("Rendering on `Headless Chrome`(execute JS).")
            with Popen([self._program_path,
                        '--disable-web-security',
                        '--no-sandbox',
                        '--headless',
                        '--disable-gpu',
                        '--disable-web-security',
                        '-–allow-file-access-from-files',
                        '--run-all-compositor-stages-before-draw',
                        '--virtual-time-budget=10000',
                        '--dump-dom',
                        temp.name], stdout=PIPE) as chrome:
                return chrome.stdout.read().decode('utf-8')

        except Exception as e:
            self._logger.error(f'Failed to render by JS: {e}')
        finally:
            os.unlink(temp.name)

        return html
