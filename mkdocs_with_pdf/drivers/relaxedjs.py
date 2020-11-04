import os
from logging import Logger
from shutil import which
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory


class RelaxedJSRenderer(object):

    @classmethod
    def setup(self, program_path: str, logger: Logger):
        if not program_path:
            return None

        if not which(program_path):
            raise RuntimeError(
                'No such `ReLaXed` program or not executable'
                + f': "{program_path}".')

        return self(program_path, logger)

    def __init__(self, program_path: str, logger: Logger):
        self._program_path = program_path
        self._logger = logger

    def write_pdf(self, html_string: str, output: str):
        self._logger.info(' Rendering with `ReLaXed JS`.')

        with TemporaryDirectory() as work_dir:
            entry_point = os.path.join(work_dir, 'pdf_print.html')
            with open(entry_point, 'w+') as f:
                f.write(html_string)
                f.close()

            self._logger.info(f"  entry_point: {entry_point}")
            with Popen([self._program_path, entry_point, output,
                        "--build-once"],
                       stdout=PIPE) as proc:
                while True:
                    log = proc.stdout.readline().decode().strip()
                    if log:
                        self._logger.info(f"  {log}")
                    if proc.poll() is not None:
                        break
