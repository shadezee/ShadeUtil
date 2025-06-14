from subprocess import run
from PyQt6.QtCore import QThread, pyqtSignal
from src.helpers.constants import (
  get_hid_restart_script,
  get_disable_network_interface_cmd,
  get_enable_network_interface_cmd,
)
from src.helpers.helper import get_setting

class DriverIssuesException(Exception):
  def __init__(self, message: str):
    super().__init__(message)
    self.message = message

class DriverIssues(QThread):
  statusSignal = pyqtSignal(str, bool)

  def __init__(self, driver: str, pwd: str):
    super().__init__()
    self.driver = driver
    self.pwd = pwd

    match driver:
      case 'hid':
        devconPath = '../../devcon/devcon.exe'
        deviceID = get_setting('hid_device_id', pwd)
        self.restartScript = get_hid_restart_script(devconPath, deviceID)
      case 'wifi':
        self.restartScript = [
          get_disable_network_interface_cmd(),
          get_enable_network_interface_cmd()
        ]

  def fix_wifi(self):
    self.statusSignal.emit('Restarting WIFI driver...\n', False)
    i = 1
    for s in self.restartScript:
      self.statusSignal.emit(f'Running Phase: {i}...\n', False)
      i += 1
      result = run(s, shell=True, check=False)
      if result.returncode == 1:
        raise DriverIssuesException('Operation failed due to insufficient privileges.\n')
    self.statusSignal.emit('Operation complete!\n\n', True)

  def fix_hid(self):
    pass

  def run(self):
    try:
      match self.driver:
        case 'wifi':
          self.fix_wifi()
        case 'hid':
          pass
    except Exception as e:
      self.statusSignal.emit(f'\nAn error occurred.\n{str(e)}\n', True)
