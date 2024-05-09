from os import listdir, path, remove, startfile
from os import environ as env
from shutil import rmtree
from send2trash import send2trash as trash

def get_env():
    return env.get('TEMP')

def clean_temp_folder(recycle):
    temp_path = get_env()
    result = clean_dir(temp_path, recycle)
    return result

def clean_dir(temp_path, recycle):
    errors = []
    for file_name in listdir(temp_path):
        file_path = path.join(temp_path, file_name)
        file_size = path.getsize(file_path) / (1024 * 1024)

        try:
            if(path.isdir(file_path)):
                if(recycle):
                    trash(file_path)
                else:
                    rmtree(file_path)
            else:
                if(recycle):
                    trash(file_path)
                else:
                    remove(file_path)
        except Exception as e:
            if ('OLE error') in str(e):
                e = 'Currently being used by another application.'

            errors.append(f'Name: {file_name}\n'
                        f'Size: {file_size:.2f} MB\n'
                        f'Reason {e}\n')

    return errors

def open_temp():
    startfile(get_env())
