import os
import requests

BINPATH = os.path.join(os.path.expanduser("~"), "Documents", "bin")

print("Downloading...")

request = requests.get("https://raw.githubusercontent.com/sn3ksoftware/Latte/master/latte.py")
data = request.text

print("Installing...")

try:
    os.mkdir(BINPATH)
except FileExistsError:
    pass
except Exception as e:
    print("ERROR: Failed to create the bin folder.")
    exit()

opened = open(os.path.join(BINPATH, "latte.py"), "w")
opened.write(data)
opened.close()

request.close()

print("Latte has been successfully installed!")
