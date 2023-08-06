import os
import shutil

def _fix_dirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def file_exists(path):
    return os.path.exists(path)

def get_data_tree(dir):
    tree = dict()
    for f in os.listdir(dir):
        full_f = os.path.join(dir,f)
        if os.path.isdir(full_f):
            tree[f] = get_data_tree(full_f)
        else:
            tree[f] = 0
    
    return tree

def clear_folder(folder):
    if not os.path.exists(folder):
        print("Not a folder")
        return
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def get_file_contents(file, mode='r'):
    if not os.path.exists(file): return None
    with open(file, mode) as f:
        return f.read()

"""
Saving data to a file.

dir => should end with a `/`, i.e. `C:/some/path/` (and not `C:/some/path`)
filename => should only contain allowed filename tokens
"""
def write_to_file(dir, filename, data):
    _fix_dirs(dir)

    path = dir+filename

    with open(path, 'wb+') as f:
        f.write(data)