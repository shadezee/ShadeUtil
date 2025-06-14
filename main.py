from os import getcwd
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
  QApplication,
  QMainWindow,
)
from PyQt6.QtGui import QIcon
import qdarkstyle
from assets.shade_util_ui import Ui_MainWindow
from src.helpers.helper import (
  is_admin,
  run_as_admin_user,
  verify_devcon,
  verify_settings
)
from src.modules.driver_issues import DriverIssues
from src.modules.settings import Settings

class ShadeUtil(QMainWindow, Ui_MainWindow):
  # DRIVER ISSUES TAB
  # buttons: settingsBtn, resetNetworkBtn, resetHidBtn
  # display: driverIssuesDisplay
  # labels: appLabel

  def __init__(self):
    self.pwd = getcwd()
    if not verify_devcon(self.pwd):
      pass
    if not verify_settings(self.pwd):
      pass

    super().__init__()
    self.setupUi(self)
    QtCore.QDir.addSearchPath('icons', 'assets/icons')
    self.setWindowIcon(QIcon('icons:/app_icon.ico'))
    self.settings = Settings(parent=self, pwd=self.pwd)

    self.settingsBtn.setIcon(QIcon('icons:/settings.ico'))
    self.settingsBtn.setIconSize(QtCore.QSize(50, 50))
    self.settingsBtn.clicked.connect(self.settings.load_settings_ui)

    self.resetNetworkBtn.clicked.connect(self.reset_driver_issues)
    self.resetHidBtn.clicked.connect(self.reset_driver_issues)

    self.opn  = None

  def reset_driver_issues(self):
    sender = self.sender()
    match sender.text():
      case 'Reset HID':
        self.opn = DriverIssues('hid', self.pwd)
      case 'Reset WIFI driver':
        self.opn = DriverIssues('wifi', self.pwd)
      case _:
        self.opn = None
        return

    self.opn.statusSignal.connect(self.update_status)
    self.opn.start()

  def update_status(self, message: str, error: bool):
    self.driverIssuesDisplay.setText(f'{self.driverIssuesDisplay.toPlainText()}{message}')
    self.driverIssuesDisplay.selectAll()

    if error:
      self.kill_driver_operations()

  def kill_driver_operations(self):
    try:
      self.opn.terminate()
      self.opn = None
    except Exception:
      pass


if __name__ == "__main__":
  if not is_admin():
    run_as_admin_user()

  app = QApplication([])
  app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
  window = ShadeUtil()
  window.show()
  app.exec()
