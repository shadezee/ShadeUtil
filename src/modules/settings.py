import json
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon
from assets.settings_ui import Ui_settingsDialog
from src.helpers.helper import (
  verify_settings,
  get_default_settings
)


class Settings(QDialog, Ui_settingsDialog):
  # labels: hidLabel, devconLabel
  # textEdits: hidText, devconText
  # buttons: saveBtn, resetBtn

  def __init__(self, parent=None, pwd:str=None):
    super(Settings, self).__init__(parent)
    self.setupUi(self)
    self.setWindowIcon(QIcon('icons:/app_icon.ico'))
    self.pwd = pwd

    self.saveBtn.clicked.connect(self.save_settings)
    self.resetBtn.clicked.connect(self.load_settings)

  def save_settings(self):
    try:
      settingsPath = verify_settings(self.pwd)
      hidDeviceId = str(self.hidText.text()).strip()

      structure = get_default_settings()
      structure['hid_device_id'] = hidDeviceId
      with open(settingsPath, 'w', encoding="utf-8") as file:
        json.dump(structure, file)
      self.close_settings_ui()
    except Exception as e:
      print(e)

  def load_settings(self):
    try:
      settingsPath = verify_settings(self.pwd)

      with open(settingsPath, 'r', encoding="utf-8") as file:
        settings = json.load(file)

      self.hidText.setText(settings['hid_device_id'])
    except Exception as e:
      print(e)

  def load_settings_ui(self):
    self.load_settings()
    self.show()

  def close_settings_ui(self):
    self.close()
