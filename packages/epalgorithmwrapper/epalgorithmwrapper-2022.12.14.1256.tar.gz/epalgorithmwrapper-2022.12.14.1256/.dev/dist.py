import os, shutil, time

dist_dir = "./dist/"

if not os.path.exists("./src"):
    raise Exception("You should run this script in the python-ep-algorithm-wrapper folder!")

if not os.path.exists("./.dev/local.creds.txt"):
    raise Exception("No credentials file")

def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)
else:
    clear_folder(dist_dir)

with open("./.dev/local.creds.txt", 'r') as f:
    creds = f.read().splitlines()

username = creds[0]
password = creds[1]

os.system("python -m pip uninstall -y epalgorithmwrapper")

os.system("python -m build")

os.system(f"python -m twine upload -u {username} -p {password} dist/*")

print("Manually reinstall eputils!")