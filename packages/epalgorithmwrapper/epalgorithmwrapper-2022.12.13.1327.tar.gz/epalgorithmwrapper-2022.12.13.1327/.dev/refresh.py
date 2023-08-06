import os

print("1")
# os.system("dir")
os.system("cd python-ep-algorithm-wrapper && py .\\.dev\\dist.py")

print("2")
os.system("cd ..")

os.system("py -m pip install --upgrade epalgorithmwrapper")
os.system("py -m pip install --upgrade epalgorithmwrapper") # Only picks last version after second call..?

print("3")
os.system("docker compose -f .\\local.docker-compose.build-template.yml build --no-cache")

print("Done!")
