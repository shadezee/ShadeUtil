
from subprocess import run
from os import startfile
import logging
from PyQt6.QtCore import (
  QThread,
  pyqtSignal
)
from src.helpers.constants import get_bing_compile_script

logger = logging.getLogger(__name__)


class BingCompileException(Exception):
  def __init__(self):
    super().__init__('message')

class Misc(QThread):
  statusSignal = pyqtSignal(str)
  errorSignal = pyqtSignal(str, str, str)

  def __init__(self, operation: str, args: list[str]):
    super().__init__()
    self.operation = operation
    self.args = args
    logger.info(f'Initializing Misc for: {operation}')

  def bing_compile(self, bingPath: str, compilePath: str):
    script = get_bing_compile_script(bingPath, compilePath)
    for s in script:
      logger.debug(f'Running command: {s}')
      result = run(s, shell=True, check=False)
      logger.info(f'ran with result: {result}')
      if result.returncode != 0:
        raise BingCompileException()

  def run(self):
    try:
      match self.operation:
        case 'bingCompile':
          self.statusSignal.emit(
            'Compilation started...',
          )
          bingPath = self.args[0]
          compilePath = self.args[1]
          self.bing_compile(bingPath, compilePath)
          startfile(compilePath)
          self.statusSignal.emit(
            f'Operation completed at {compilePath}',
          )
        case _ :
          pass
    except BingCompileException:
      self.errorSignal.emit(
        'MISC_TITLE',
        'BING_COMPILE_ERROR',
        'WARNING'
      )
    except Exception:
      self.errorSignal.emit(
        'MISC_TITLE',
        'STANDARD_ERROR',
        'WARNING'
      )
