# Installer file for Latte, a Python-based
# package manager for Pythonista/Libterm.

import os
import requests

ROOT = os.path.expanduser("~")

try:
    import objc_util
except ImportError:
    BINPATH = os.path.join(ROOT, "Library", "bin")
else:
    BINPATH = os.path.join(ROOT, "Documents", "bin")

print("Downloading...")

try:
    request = requests.get(
        "https://raw.githubusercontent.com/sn3ksoftware/Latte/master/latte.py"
    )
except requests.ConnectionError:
    print("ERROR: Could not connect to server!!! Check your Internet?")
    exit()
except Exception as e:
    print("ERROR: Unhandled exception occured! Exception:" + str(e))
else:
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
