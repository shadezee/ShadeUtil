
def get_hid_restart_script(devconPath: str, deviceID: str):
  script = f'''\n
    $devconPath = {devconPath}\n
    $deviceID = {deviceID}\n
    & $devconPath find * | Select-String $deviceID\n
    & $devconPath disable "$deviceID"\n
    Start-Sleep -Seconds 3\n
    & $devconPath enable "$deviceID"\n
  '''

  return script

def get_enable_network_interface_cmd():
  return 'netsh interface set interface Wi-Fi enable'

def get_disable_network_interface_cmd():
  return 'netsh interface set interface Wi-Fi disable'
