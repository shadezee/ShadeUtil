from os import (
  listdir,
  path,
  remove,
)
import textwrap
from shutil import rmtree
from PyQt6.QtCore import (
  QThread,
  pyqtSignal
)
from send2trash import send2trash as trash


class Storage(QThread):
  statusSignal = pyqtSignal(str, bool)
  errorSignal = pyqtSignal(str, str, str)

  def __init__(self, dirPath:str, recycle: bool):
    super().__init__()
    self.recycle = recycle
    self.errors = []
    self.path = dirPath

  def clear_folder(self):
    self.statusSignal.emit(f'Clearing: {self.path}\n', False)
    for fileName in listdir(self.path):
      filePath = path.join(self.path, fileName)
      fileSize = path.getsize(filePath) / (1024 * 1024)

      try:
        if path.isdir(filePath):
          if self.recycle:
            trash(filePath)
          else:
            rmtree(filePath)
        else:
          if self.recycle:
            trash(filePath)
          else:
            remove(filePath)
      except Exception as e:
        if 'OLE error' in str(e):
          e = 'Currently being used by another application.'

        self.errors.append(
          textwrap.dedent(f"""
            Name: {fileName}
            Size: {fileSize:.2f} MB
            Reason {e}
          """).strip()
        )

    message = 'Cleared successfully!'
    errorCount = len(self.errors)
    if errorCount != 0:
      message = f'Cleared with {errorCount} errors!'
      self.errorSignal.emit(
        'STORAGE_TITLE',
        'FILES_IN_USE_ERROR',
        'INFORMATION'
      )
      for error in self.errors:
        message += '\n\n' + error

    self.statusSignal.emit(message, True)

  def run(self):
    self.clear_folder()
