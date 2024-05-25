from subprocess import run

def network_fix():
    disable_interface_command = 'netsh interface set interface Wi-Fi disable'
    enable_interface_command = 'netsh interface set interface Wi-Fi enable'
    try:
        run(disable_interface_command, shell=True, check=False)
        run(enable_interface_command, shell=True, check=False)
        return True
    except Exception as e:
        return e
