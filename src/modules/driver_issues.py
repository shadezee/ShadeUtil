from subprocess import (
  run,
  CREATE_NO_WINDOW
)
import logging
import textwrap
from PyQt6.QtCore import (
  QThread,
  pyqtSignal
)
from src.helpers.constants import (
  get_hid_restart_script,
  get_protected_drivers,
  get_disable_network_interface_cmd,
  get_enable_network_interface_cmd
)
from src.helpers.helper import (
  get_setting,
  verify_devcon
)


logger = logging.getLogger(__name__)


class DriverPermissionsException(Exception):
  def __init__(self):
    super().__init__('Operation failed due to insufficient privileges.')

class DriverIssuesException(Exception):
  def __init__(self):
    super().__init__('Operation failed.')

class PartialSuccessException(Exception):
  def __init__(self, failedDrivers: list, protectedFailed: list):
    allFailedList = ''
    protectedList = ''
    for index, driver in enumerate(failedDrivers):
      allFailedList += f'{index + 1}. {driver}\n'
    for index, driver in enumerate(protectedFailed):
      protectedList += f'{index + 1}. {driver}\n'
    allFailedList = allFailedList.strip()
    protectedList = protectedList.strip()

    message = textwrap.dedent(f'''
      Certain drivers failed to restart.
      Failed Drivers:
      {allFailedList if allFailedList else 'None'}
      Protected Drivers (could not be restarted due to protection):
      {protectedList if protectedList else 'None'}
    ''')
    super().__init__(message)

class DriverIssues(QThread):
  statusSignal = pyqtSignal(str, bool)
  errorSignal = pyqtSignal(str, str, str)

  def __init__(self, driver: str, pwd: str):
    super().__init__()
    self.driver = driver
    self.pwd = pwd
    logger.info(f'Initializing DriverIssues for {driver} driver.')

  def fix_wifi(self):
    restartScript = [
      get_disable_network_interface_cmd(),
      get_enable_network_interface_cmd()
    ]
    self.statusSignal.emit('Restarting WIFI driver...\n', False)
    i = 1
    for s in restartScript:
      logger.debug(f'Running command: {s}')
      self.statusSignal.emit(f'Running Phase: {i}...\n', False)
      i += 1
      result = run(s, shell=True, check=False)
      logger.debug(f'Result: {result}')
      if result.returncode == 1:
        raise DriverPermissionsException()
    self.statusSignal.emit('Operation complete!\n\n', True)

  def process_hid_output(self, result):
    logger.debug('processing results...')
    result = result.strip().splitlines()

    errors = 0
    success = 0
    failedDrivers = []
    protectedFailed = []
    for line in result:
      if line.strip().lower().endswith(': disabled'):
        errors += 1
      elif line.strip().lower().endswith(': enabled'):
        success += 1
      elif 'failed' in line.strip().lower():
        failedDrivers.append(line.split(':')[0].strip())

    if errors - success != 0:
      protectedDrivers = get_protected_drivers()
      failedDrivers = list(set(failedDrivers))
      protectedFailed = [
        driver for driver in failedDrivers if driver in protectedDrivers
      ]
      failedDrivers = failedDrivers - protectedDrivers

    logger.warning(
      textwrap.dedent(
        f'''
          Errors: {errors}
          Success: {success}
          Failed drivers: {failedDrivers}
          Protected failed drivers: {protectedFailed}
        '''
      )
    )
    return failedDrivers, protectedFailed

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
    logger.debug(f'Restart script: {restartScript}')

    self.statusSignal.emit('Restarting HID drivers...\n', False)
    result = run(
      ['powershell', '-Command', restartScript],
      capture_output=True, text=True, check=False,
      creationflags=CREATE_NO_WINDOW
    )

    logger.debug(f'STDOUT:\n{result.stdout}')
    logger.debug(f'STDERR:\n{result.stderr}')

    if result.stdout.find('No matching devices found.') != -1:
      raise DriverIssuesException()
    if result.stderr != '':
      raise DriverIssuesException()

    failedDrivers, protectedFailed = self.process_hid_output(result.stdout)
    if len(failedDrivers) > 0 or len(protectedFailed) > 0:
      logger.warning(
        textwrap.dedent(f'''
          Failed to restart drivers:\n
          Protected: {protectedFailed}\n
          Others: {failedDrivers}
        ''')
      )
      logger.warning(f'Others: {failedDrivers}')
      raise PartialSuccessException(failedDrivers, protectedFailed)

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
    except PartialSuccessException:
      self.errorSignal.emit(
        'DRIVER_ISSUES_TITLE',
        'PARTIAL_SUCCESS_ERROR',
        'WARNING'
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
