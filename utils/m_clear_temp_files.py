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
            errors.append(f'{file_name} with {e}.')
    return errors

def open_temp():
    startfile(get_env())
