from subprocess import run, CREATE_NO_WINDOW
from PyQt6.QtCore import (
  QThread,
  pyqtSignal
)
from src.helpers.constants import (
  get_hid_restart_script,
  get_disable_network_interface_cmd,
  get_enable_network_interface_cmd
)
from src.helpers.helper import (
  get_setting,
  verify_devcon
)


class DriverPermissionsException(Exception):
  def __init__(self):
    super().__init__('Operation failed due to insufficient privileges.')

class DriverIssuesException(Exception):
  def __init__(self):
    super().__init__('Operation failed.')

class DriverIssues(QThread):
  statusSignal = pyqtSignal(str, bool)
  errorSignal = pyqtSignal(str, str, str)

  def __init__(self, driver: str, pwd: str):
    super().__init__()
    self.driver = driver
    self.pwd = pwd

  def fix_wifi(self):
    restartScript = [
      get_disable_network_interface_cmd(),
      get_enable_network_interface_cmd()
    ]
    self.statusSignal.emit('Restarting WIFI driver...\n', False)
    i = 1
    for s in restartScript:
      self.statusSignal.emit(f'Running Phase: {i}...\n', False)
      i += 1
      result = run(s, shell=True, check=False)
      if result.returncode == 1:
        raise DriverPermissionsException()
    self.statusSignal.emit('Operation complete!\n\n', True)

  def fix_hid(self):
    devconPath = verify_devcon(self.pwd)
    deviceID = get_setting('hid_device_id', self.pwd)

    if deviceID == '':
      self.errorSignal.emit(
        'SETTINGS_TITLE', 
        'INVALID_SETTING_ERROR',
        'CRITICAL'
      )
      raise DriverIssuesException()
    restartScript = get_hid_restart_script(devconPath, deviceID)

    self.statusSignal.emit('Restarting HID drivers...\n', False)
    result = run(
        ["powershell", "-Command", restartScript],
        capture_output=True, text=True, check=False,
        creationflags=CREATE_NO_WINDOW
    )

    if result.stdout.find('Disable failed') != -1:
      raise DriverPermissionsException()
    if result.stdout.find('No matching devices found.') != -1:
      raise DriverIssuesException()
    if result.stderr != '':
      raise DriverIssuesException()
    self.statusSignal.emit('Operation complete!\n\n', True)

  def run(self):
    try:
      match self.driver:
        case 'wifi':
          self.fix_wifi()
        case 'hid':
          self.fix_hid()
    except DriverPermissionsException:
      self.errorSignal.emit(
        'DRIVER_ISSUES_TITLE',
        'INSUFFICIENT_PRIVILEGES_ERROR',
        'CRITICAL'
      )
    except Exception:
      match self.driver:
        case 'wifi':
          self.errorSignal.emit(
            'DRIVER_ISSUES_TITLE',
            'RESTART_WIFI_ERROR',
            'WARNING'
          )
        case 'hid':
          self.errorSignal.emit(
            'DRIVER_ISSUES_TITLE',
            'RESTART_HID_ERROR',
            'WARNING'
          )
