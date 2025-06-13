from PyQt6.QtWidgets import (
  QApplication,
  QMainWindow,
)
from assets.shade_util_ui import Ui_MainWindow
from os import path, getcwd
from src.helpers.helper import is_admin, run_as_admin_user, verify_devcon

class ShadeUtil(QMainWindow, Ui_MainWindow):
  def __init__(self):
    if not verify_devcon(getcwd()):
      print('Devcon not found')

    super().__init__()
    self.setupUi(self)
    print('App started')

if __name__ == "__main__":
  if not is_admin():
    run_as_admin_user()

  app = QApplication([])
  window = ShadeUtil()
  window.show()
  app.exec()
