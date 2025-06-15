from os import path, makedirs, walk, environ as env
import json
import sys
from ctypes import windll, create_unicode_buffer
from src.helpers.constants import get_default_settings


def is_admin():
  try:
    return windll.shell32.IsUserAnAdmin()
  except Exception:
    return False

def run_as_admin_user():
  if sys.platform == 'win32':
    if windll.shell32.IsUserAnAdmin() == 0:
      sysExecutable = sys.executable
      params = " ".join(sys.argv)
      windll.shell32.ShellExecuteW(None, "runas", sysExecutable, params, None, 1)
      sys.exit(1)
  return True

def verify_devcon(pwd: str):
  try:
    devconPath = get_setting('devcon_path', pwd)
    if devconPath == '':
      devconPath = path.join(pwd, 'devcon')
      if not path.isdir(devconPath):
        makedirs(devconPath)
      devconPath = path.join(devconPath, 'devcon.exe')
    if not path.isfile(devconPath):
      return False
  except Exception:
    return False
  return devconPath

def verify_settings(pwd: str):
  try:
    settingsPath = path.join(pwd, 'settings')
    if not path.isdir(settingsPath):
      makedirs(settingsPath)

    defaultStructure = dict(get_default_settings())
    settingsPath = path.join(settingsPath, 'settings.json')
    if not path.isfile(settingsPath):
      with open(settingsPath, 'w', encoding="utf-8") as f:
        json.dump(defaultStructure, f)
      return settingsPath

    try:
      with open(settingsPath, 'r', encoding="utf-8") as f:
        settings = json.load(f)
    except Exception:
      settings = {}

    modified = False
    for key, value in defaultStructure.items():
      if key not in settings:
        settings[key] = value
        modified = True

    if modified:
      with open(settingsPath, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
  except Exception:
    return False

  return settingsPath

def get_setting(key: str, pwd: str):
  settingsPath = path.join(pwd, 'settings', 'settings.json')
  with open(settingsPath, 'r', encoding="utf-8") as f:
    settings = json.load(f)
  return settings[key]

async def get_temp_folder_size():
  totalSize = 0

  for dirpath, _, filenames in walk(env.get('TEMP')):
    for filename in filenames:
      filepath = path.join(dirpath, filename)
      totalSize += path.getsize(filepath)

  return (totalSize / 1024) / 1024

async def get_recycle_bin_size():
  shell32 = windll.shell32
  buffer = create_unicode_buffer(260)
  shell32.SHGetFolderPathW(0, 10, 0, 0, buffer)
  recycleBinPath = path.join(env['HOMEDRIVE'], '\\$Recycle.Bin')

  totalSize = 0
  for dirpath, _, filenames in walk(recycleBinPath):
    for filename in filenames:
      filepath = path.join(dirpath, filename)
      totalSize += path.getsize(filepath)

  return totalSize / (1024 * 1024)
