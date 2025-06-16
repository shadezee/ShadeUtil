import textwrap
import logging
from PyQt6.QtWidgets import (
  QMessageBox
)

logger = logging.getLogger(__name__)

class ErrorConstants:
  TITLES = {
    'STANDARD_ERROR_TITLE' : 'Error',
    'STARTUP_ERROR_TITLE' : 'Startup error',
    'DRIVER_ISSUES_TITLE' : 'Driver issues error',
    'STORAGE_TITLE' : 'Storage error',
    'SETTINGS_TITLE' : 'Settings error',
    'MISC_TITLE' : 'Misc error'
  }

  MESSAGES = {
    'STANDARD_ERROR' : 'Something went wrong.',
    'STARTUP_ERROR' : textwrap.dedent('''
                        Something went wrong during application startup.\n
                        Some features maybe disabled.
                      ''').strip(),
    'MISSING_DEVCON_ERROR' : 'Unable to find devcon.exe.',
    'INVALID_SETTINGS_FILE_ERROR' : 'Invalid or missing settings file.',
    'SAVE_SETTINGS_ERROR' : 'Error saving settings.',
    'LOAD_SETTINGS_ERROR' : 'Error loading settings.',
    'RESTART_WIFI_ERROR' : textwrap.dedent('''
                            Network driver could not be restarted.\n
                            Please check your permissions.
                          ''').strip(),
    'RESTART_HID_ERROR' : textwrap.dedent('''
                            HID drivers could not be restarted.\n
                            Please check your permissions or device id.
                          ''').strip(),
    'PARTIAL_SUCCESS_ERROR' : 'Operation partially successful.',
    'INVALID_SETTING_ERROR' : 'Invalid or missing setting for this particular operation.',
    'INSUFFICIENT_PRIVILEGES_ERROR' : 'Operation failed due to insufficient privileges.',
    'FILES_IN_USE_ERROR' : textwrap.dedent('''
                            Operation incomplete...\n
                            Some files are currently being used by another application.
                          ''').strip(),
    'BING_COMPILE_ERROR' : textwrap.dedent('''
                            There was an issue with original assets.\n
                            Bing compile failed.\n
                          ''').strip()
  }


class Errors:
  @staticmethod
  def raise_error(
    parent,
    title='STANDARD_ERROR_TITLE',
    errorType='STANDARD_ERROR',
    errorLevel='WARNING'
  ):
    title = ErrorConstants.TITLES.get(title)
    message = ErrorConstants.MESSAGES.get(errorType)

    if errorLevel == 'CRITICAL':
      QMessageBox.critical(parent, title, message)
      logger.error(f'{title} : {message}')
    elif errorLevel == 'WARNING':
      logger.warning(f'{title} : {message}')
      QMessageBox.warning(parent, title, message)
    elif errorLevel == 'INFORMATION':
      logger.debug(f'{title} : {message}')
      QMessageBox.information(parent, title, message)
