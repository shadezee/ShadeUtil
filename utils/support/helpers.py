from os import path, walk, environ as env
from ctypes import windll, create_unicode_buffer

def get_temp_folder_size():
    total_size = 0

    for dirpath, dirnames, filenames in walk(env.get('TEMP')):
        for filename in filenames:
            filepath = path.join(dirpath, filename)
            total_size += path.getsize(filepath)

    total_size = ((total_size / 1024) / 1024)

    return total_size

def get_recycle_bin_size():
    shell32 = windll.shell32
    buffer = create_unicode_buffer(260)
    shell32.SHGetFolderPathW(0, 10, 0, 0, buffer)
    recycle_bin_path = buffer.value
    recycle_bin_path = path.join(env['HOMEDRIVE'], '\$Recycle.Bin')

    total_size = 0
    for dirpath, _, filenames in walk(recycle_bin_path):
        for filename in filenames:
            filepath = path.join(dirpath, filename)
            total_size += path.getsize(filepath)

    total_size = (total_size / (1024 * 1024))

    return total_size
