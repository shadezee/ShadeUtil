
from subprocess import run
from os import startfile
from PyQt6.QtCore import (
  QThread,
  pyqtSignal
)
from src.helpers.constants import get_bing_compile_script


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

  def bing_compile(self, bingPath: str, compilePath: str):
    script = get_bing_compile_script(bingPath, compilePath)
    print(script)
    for s in script:
      print('s',s)
      result = run(s, shell=True, check=False)
      print(result)
      if result.returncode != 0:
        raise BingCompileException()

  def run(self):
    try:
      match self.operation:
        case 'bingCompile':
          print('START')
          self.statusSignal.emit(
            'Compilation started...\n',
          )
          bingPath = self.args[0]
          compilePath = self.args[1]
          self.bing_compile(bingPath, compilePath)
          startfile(compilePath)
          self.statusSignal.emit(
            f'Operation completed at {compilePath}!\n\n',
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
