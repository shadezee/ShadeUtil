from os import path, makedirs
import sys
from ctypes import windll

def verify_devcon(pwd: str):
  devconPath = path.join(pwd, 'devcon')
  if not path.isdir(devconPath):
    makedirs(devconPath)
  devconPath = path.join(devconPath, 'devcon.exe')
  if not path.isfile(devconPath):
    return False
  return True

def is_admin():
  try:
    return windll.shell32.IsUserAnAdmin()
  except:
    return False

def run_as_admin_user():
  print('Running as admin from function')
  if sys.platform == 'win32':
    if windll.shell32.IsUserAnAdmin() == 0:
      sysExecutable = sys.executable
      params = " ".join(sys.argv)
      windll.shell32.ShellExecuteW(None, "runas", sysExecutable, params, None, 1)
      sys.exit(1)
  return True

# run_as_admin_user()
