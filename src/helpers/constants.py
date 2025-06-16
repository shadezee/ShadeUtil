

def get_hid_restart_script(devconPath: str, deviceID: str):
  script = f'''
    $devconPath = "{devconPath}"
    $deviceID = "{deviceID}"
    & $devconPath find * | Select-String $deviceID
    & $devconPath disable "$deviceID"
    Start-Sleep -Seconds 1
    & $devconPath enable "$deviceID"
  '''

  return script

def get_protected_drivers():
  return [
    'HID\INTC816\3&D2322F2&0&0000',
    'HID\CONVERTEDDEVICE&COL01\5&32CF90E6&0&0000'
  ]

def get_enable_network_interface_cmd():
  return 'netsh interface set interface Wi-Fi enable'

def get_disable_network_interface_cmd():
  return 'netsh interface set interface Wi-Fi disable'

def get_default_settings():
  settings = {
    'hid_device_id' : '',
    'devcon_path' : '',
  }

  return settings

def get_bing_compile_script(bingAssetsPath: str, compilePath: str):
  script = [
    f'xcopy /s /i "{bingAssetsPath}" "{compilePath}"',
    f'cd "{compilePath}" && ren *.* *.jpg'
  ]

  return script
