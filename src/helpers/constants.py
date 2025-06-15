
def get_hid_restart_script(devconPath: str, deviceID: str):
  script = f'''
    $devconPath = "{devconPath}"
    $deviceID = "{deviceID}"
    & $devconPath find * | Select-String $deviceID
    & $devconPath disable "$deviceID"
    Start-Sleep -Seconds 3
    & $devconPath enable "$deviceID"
  '''

  return script

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
