from os import path, makedirs
import json
import sys
from ctypes import windll
from src.helpers.constants import get_default_settings

def get_setting(key: str, pwd: str):
  settingsPath = path.join(pwd, 'settings', 'settings.json')
  with open(settingsPath, 'r', encoding="utf-8") as f:
    settings = json.load(f)
  return settings[key]

def verify_devcon(pwd: str):
  devconPath = path.join(pwd, 'devcon')
  if not path.isdir(devconPath):
    makedirs(devconPath)
  devconPath = path.join(devconPath, 'devcon.exe')
  if not path.isfile(devconPath):
    return False
  return True

def verify_settings(pwd: str):
  try:
    settingsPath = path.join(pwd, 'settings')
    if not path.isdir(settingsPath):
      makedirs(settingsPath)

    settingsPath = path.join(settingsPath, 'settings.json')
    if not path.isfile(settingsPath):
      with open(settingsPath, 'w', encoding="utf-8") as f:
        json.dump(get_default_settings(), f)
  except Exception:
    return False

  return settingsPath

def is_admin():
  try:
    return windll.shell32.IsUserAnAdmin()
  except Exception:
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
