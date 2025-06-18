from os import (
  getcwd,
  environ as env,
  path,
  makedirs
)
import asyncio
import textwrap
import logging
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
  QApplication,
  QMainWindow
)
from PyQt6.QtGui import (
  QIcon,
  QCursor
)
from qasync import QEventLoop
from assets.shade_util_ui import Ui_MainWindow
from src.helpers.helper import (
  is_admin,
  run_as_admin_user,
  verify_devcon,
  verify_settings,
  get_temp_folder_size,
  get_recycle_bin_size,
  verify_bing_folder,
  create_bing_compile_folder
)
from src.modules.settings import Settings
from src.modules.driver_issues import DriverIssues
from src.modules.storage import Storage
from src.modules.misc import Misc
from src.helpers.errors import Errors
from assets.stylesheets import get_initial_stylesheet

def setup_logging():
  logDir = path.join(getcwd(), 'data', 'logs')
  # pylint: disable-next=redefined-outer-name
  logFile = path.join(logDir, 'shade_util.log')

  if not path.exists(logDir):
    makedirs(logDir)
  with open(logFile, 'w', encoding='utf-8'):
    pass

  logging.basicConfig(
    filename=logFile,
    level=logging.NOTSET,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
  )

  return logFile

logFile = setup_logging()
logger = logging.getLogger(__name__)


class ShadeUtil(QMainWindow, Ui_MainWindow):
  # MAIN
  # buttons: settingsBtn

  # DRIVER ISSUES TAB
  # buttons: resetNetworkBtn, resetHidBtn
  # display: driverIssuesDisplay

  # STORAGE TAB
  # buttons: recycleRdo, clearTempBtn
  # display: folderDetailsDisplay, operationDetailsDisplay

  # MISC TAB
  # buttons: bingCompileBtn
  # display: miscDisplay

  def __init__(self):
    super().__init__()
    self.setupUi(self)

    startUpError = False
    self.pwd = getcwd()
    logger.debug(f'Running in {self.pwd}')

    if not verify_settings(self.pwd):
      startUpError = True
      self.settingsBtn.setEnabled(False)
      self.handle_errors(
        'SETTINGS_TITLE',
        'INVALID_SETTINGS_FILE_ERROR',
        'WARNING'
      )
    if not verify_devcon(self.pwd):
      startUpError = True
      self.resetHidBtn.setEnabled(False)
      self.handle_errors(
        'DRIVER_ISSUES_TITLE',
        'MISSING_DEVCON_ERROR',
        'WARNING'
      )
    if startUpError:
      self.handle_errors(
        'STARTUP_ERROR_TITLE',
        'STARTUP_ERROR',
        'CRITICAL'
      )

    QtCore.QDir.addSearchPath('icons', 'assets/icons')
    self.setWindowIcon(QIcon('icons:/app_icon.ico'))
    self.tabs.setCurrentIndex(0)

    self.settings = Settings(parent=self, pwd=self.pwd)
    self.opn  = None
    self.opnMapping = {}

    self.settingsBtn.setIcon(QIcon('icons:/settings.ico'))
    self.settingsBtn.setIconSize(QtCore.QSize(75, 75))
    self.settingsBtn.clicked.connect(self.settings.load_settings_ui)

    self.resetNetworkBtn.clicked.connect(self.perform_driver_issues_operations)
    self.resetHidBtn.clicked.connect(self.perform_driver_issues_operations)

    self.clearTempBtn.clicked.connect(self.perform_storage_operations)
    QtCore.QTimer.singleShot(
      0,
      lambda: asyncio.ensure_future(self.populate_storage_tab())
    )

    self.bingCompileBtn.clicked.connect(self.perform_misc_operations)

  def handle_errors(self, title: str, errorType: str, errorLevel: str):
    Errors.raise_error(
      self,
      title,
      errorType,
      errorLevel,
    )

  def toggle_button_status(self, opn, inProgress: bool, button=None):
    logger.debug(f'Current mapping: \n{self.opnMapping}')
    if inProgress:
      if button:
        self.opnMapping[opn] = button
    else:
      button = self.opnMapping.pop(opn)
    button.setEnabled(not button.isEnabled())

  def perform_driver_issues_operations(self):
    sender = self.sender()
    match sender.text():
      case 'Reset HID':
        self.opn = DriverIssues('hid', self.pwd)
      case 'Reset WIFI driver':
        self.opn = DriverIssues('wifi', self.pwd)
      case _ :
        self.opn = None
        return

    self.toggle_button_status(self.opn, True, sender)
    self.opn.statusSignal.connect(self.update_di_status)
    self.opn.errorSignal.connect(self.handle_errors)
    opn = self.opn
    self.opn.finished.connect(lambda: self.toggle_button_status(opn, inProgress=False))

    self.driverIssuesDisplay.setTextInteractionFlags(
      QtCore.Qt.TextInteractionFlag.NoTextInteraction
    )
    self.driverIssuesDisplay.viewport().setCursor(
      QCursor(
        QtCore.Qt.CursorShape.BusyCursor
      )
    )
    self.opn.start()

  def kill_driver_operations(self):
    try:
      self.opn.terminate()
      self.opn = None
    except Exception:
      pass

  def perform_storage_operations(self):
    recycle = self.recycleRdo.isChecked()

    sender = self.sender()
    match sender.text():
      case 'Clear Temp folder':
        self.opn = Storage(env.get('TEMP'), recycle)
      case _ :
        self.opn = None
        return

    self.toggle_button_status(self.opn, True, sender)
    self.opn.statusSignal.connect(self.update_storage_status)
    self.opn.errorSignal.connect(self.handle_errors)
    self.opn.finished.connect(lambda: self.toggle_button_status(self.opn, inProgress=False))

    self.operationDetailsDisplay.setTextInteractionFlags(
      QtCore.Qt.TextInteractionFlag.NoTextInteraction
    )
    self.operationDetailsDisplay.viewport().setCursor(
      QCursor(
        QtCore.Qt.CursorShape.BusyCursor
      )
    )
    self.opn.start()

  async def populate_storage_tab(self):
    tempSize, recycleBinSize = await asyncio.gather(
      get_temp_folder_size(),
      get_recycle_bin_size()
    )

    self.folderDetailsDisplay.clear()
    self.folderDetailsDisplay.setText(
      textwrap.dedent(f'''
        Temp folder size: {round(tempSize)} MB.
        Recycle bin size: {round(recycleBinSize)} MB.
      ''').strip()
    )

  def perform_misc_operations(self):
    sender = self.sender()

    match sender.text():
      case 'Fetch today\'s Bing wallpapers':
        bingPath = verify_bing_folder()
        compilePath = create_bing_compile_folder(self.pwd)

        if bingPath and compilePath:
          self.opn = Misc('bingCompile', [bingPath, compilePath])
      case _ :
        return

    self.toggle_button_status(self.opn, True, sender)
    self.opn.statusSignal.connect(self.update_misc_status)
    self.opn.errorSignal.connect(self.handle_errors)
    self.opn.finished.connect(lambda: self.toggle_button_status(self.opn, inProgress=False))

    self.opn.start()

  def update_di_status(self, message: str, error: bool):
    self.driverIssuesDisplay.setText(
      f'{self.driverIssuesDisplay.toPlainText()}{message}'
    )
    self.driverIssuesDisplay.setTextInteractionFlags(
      QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
    )
    self.driverIssuesDisplay.viewport().setCursor(
      QCursor(
        QtCore.Qt.CursorShape.ArrowCursor
      )
    )

    if error:
      self.kill_driver_operations()

  def update_storage_status(self, message: str, refresh: bool):
    if refresh:
      QtCore.QTimer.singleShot(
        0,
        lambda: asyncio.ensure_future(self.populate_storage_tab())
      )
      self.operationDetailsDisplay.setTextInteractionFlags(
        QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
      )
      self.operationDetailsDisplay.viewport().setCursor(
        QCursor(
          QtCore.Qt.CursorShape.ArrowCursor
        )
      )

    self.operationDetailsDisplay.setText(
      f'{self.operationDetailsDisplay.toPlainText()}{message}\n\n'
    )

  def update_misc_status(self, message: str):
    self.miscDisplay.setText(
      f'{self.miscDisplay.toPlainText()}{message}\n\n'
    )


if __name__ == '__main__':
  logger.info('Application startup initiated.')
  try:
    if not is_admin():
      run_as_admin_user()

    app = QApplication([])
    app.setStyleSheet(get_initial_stylesheet())

    logger.info('Application style set.')
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    logger.info('Event loops initialized.')

    window = ShadeUtil()
    window.show()

    with loop:
      loop.run_forever()
  except Exception:
    Errors.raise_error(
      None,
      title='STARTUP_ERROR_TITLE',
      errorType='STANDARD_ERROR',
      errorLevel='CRITICAL'
    )
