#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A package manager meant for Pythonista, built on StaSh.
Code copyright (c) Seanld/sn3ksoftware 2017-2019, MIT License.
This is a fork by sn3ksoftware to patch
compatibility with other platforms (i.e Libterm.)
Works on Python 2.7+ and Python 3.6+.
"""
from __future__ import absolute_import, print_function, unicode_literals

import argparse
import os
import shutil
import sys

from os.path import join

import requests


def f(fstr):
    """f-strings for older versions of Python
    i.e 2.7, 3.5 and eariler.
    Uses globals(), which is somewhat hacky.
    """
    if type(fstr) is str:
        return fstr.format(**globals())
    else:
        return None


__version__ = "2.1.0-alpha"
__author__ = "Seanld/sn3ksoftware"
__copyright__ = "Copyright (c) Seanld/sn3ksoftware 2017-2019, MIT License."
desc = f("apt-get for Pythonista, version {__version__}.\n{__copyright__}")

# Tuple of user-facing functions
func_tuple = (
    "install",
    "remove",
    "new",
    "addrepo",
    "listrepo",
    "delrepo"
)


def onpy():
    """Check if Latte is running on Pythonista."""
    try:
        import objc_util
    except KeyError:
        return False
    else:
        return True


if onpy():
    ROOT = os.path.expanduser("~/Documents")
else:
    ROOT = os.path.expanduser("~/Library")


SWPATH = join(ROOT, ".latte-repos.swconf")
LATTEPATH = join(ROOT, ".latte")
BINPATH = join(ROOT, "bin")


# Placeholder code for making a new package
dev_template = """
# This is just an example template. You can change this all you like.

import sys
import argparse

def main(sargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('echo', help='What you want the command to echo back.')
    args = parser.parse_args(sargs)
    
    print('Echoing back: '+args.echo)

if __name__ == '__main__':
    main(sys.argv[1:])
"""
meta_template = """
developer=Your name here
description=Enter description of your app here
version=0.0.1
"""


if onpy():
    class ansi:
        """Collection of Stash's ANSI escape codes."""
        bold = u"\033[1m"
        underscore = u"\x9b4m"
        attr_end = u"\x9b0m"
        
        fore_red = u"\x9b31m"
        fore_yellow = u"\x9b51m"
        fore_green = u"\x9b32m"
        fore_brown = u"\x9b33m"
        fore_blue = u"\x9b34m"
        fore_pink = u"\x9b35m"
        fore_cyan = u"\x9b36m"
        fore_white = u"\x9b37m"
        fore_end = u"\x9b39m"
        
        back_red = u"\x9b41m"
        back_green = u"\x9b42m"
        back_brown = u"\x9b43m"
        back_blue = u"\x9b44m"
        back_pink = u"\x9b45m"
        back_cyan = u"\x9b46m"
        back_white = u"\x9b47m"
        back_end = u"\x9b49m"
else:
    class ansi:
        """Collection of LibTerm's ANSI escape codes."""
        bold = u"\u001b[1m"
        italic = u"\u001b[3m"
        underscore = u"\x9b4m"
        attr_end = u"\u001b[0m"

        # All 'bright' colours execpt for red and brown.
        fore_red = u"\u001b[31m"
        fore_yellow = u"\u001b[91m"
        fore_green = u"\u001b[90m"
        fore_brown = u"\u001b[33m"
        fore_blue = u"\u001b[92m"
        fore_pink = u"\u001b[93m"
        fore_cyan = u"\u001b[94m"
        fore_white = u"\u001b[30m"
        fore_end = u"\u001b[0m"


def Red(text):
    return ansi.fore_red + text + ansi.fore_end


def Blue(text):
    return ansi.fore_blue + text + ansi.fore_end


def Green(text):
    return ansi.fore_green + text + ansi.fore_end


def Cyan(text):
    return ansi.fore_cyan + text + ansi.fore_end


def Yellow(text):
    return ansi.fore_yellow + text + ansi.fore_end


class SWConfig(object):
    """Parser for the config files such as the repository listing."""
    def __init__(self, content):
        self.data = {}
        for line in content.splitlines():
            if line == "":
                continue

            key = line.split("=")[0]
            # If value does not exist, replace with None
            try:
                value = line.split("=")[1]
            except IndexError:
                value = None
            finally:
                self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()


def init():
    """Setup Latte files and dirs"""
    req_paths = [LATTEPATH, BINPATH]
    for path in req_paths:
        if os.path.isdir(path):
            continue
        else:
            try:
                os.mkdir(path)
            except Exception as e:
                err = str(e)
                print(
                    Red("ERROR") +
                    f(": Could not create {path}. Traceback: {err}")
                )
            else:
                continue


def loadconfig(PATH):
    """Load Latte's repo configuration from
    the PATH. A dictionary of the config data is returned, otherwise None."""
    try:
        f = open(PATH, "r")
    except FileNotFoundError:
        return None
    else:
        confobj = SWConfig(f.read())
        if confobj is None:
            return None
        else:
            return confobj.data


def download_package(url, package_name):
    """Download a Latte package from the url
    to the current directory (under dir
    'package_name')."""
    
    content_listing = ["bin.py", "meta.latte"]
    
    try:
        os.mkdir(join(ROOT, package_name))
    except OSError:
        print(
            Yellow("WARNING") +
            ": Temporary folder for package already exists."
        )
    for item in content_listing:
        requested = requests.get(url + "/" + package_name + "/" + item)
        content = requested.text
        if not requested:
            # Delete the unused temp folder first
            shutil.rmtree(join(ROOT, package_name))
            sys.exit()
        else:
            opened = open(join(ROOT, package_name, item), "w")
            opened.write(content)
            opened.close()
        requested.close()
    return True


def install(pkg_name):
    """Install packages from a repo. pkg_name
    can be 'nickname/package', where nickname
    is the name of the repo (universe by
    default)."""

    REPOSITORIES = loadconfig(SWPATH)
    packageSplitted = pkg_name.split("/")

    try:
        package_name = packageSplitted[1]
        repo_to_use = REPOSITORIES[packageSplitted[0]]
    except IndexError:
        repo_to_use = REPOSITORIES["universe"]
        package_name = packageSplitted[0]
        print(
            Yellow("WARNING") +
            ": No repository specified, using universe by default..."
        )

    try:
        download_package(repo_to_use, package_name)
    except requests.ConnectionError:
        print(
            Red("ERROR") +
            ": Couldn't find package. Check your Internet connection?"
        )
        sys.exit()
    except requests.HTTPError:
        print(
            Red("ERROR") +
            ": Invaild HTTP response. Contact the server admin/repo owner."
        )
        sys.exit()
    except Exception as e:
        err = str(e)
        print(
            Red("ERROR") +
            ": Unhandled exception occured. Content: {err}"
        )
        sys.exit()

    # Move to correct locations
    print("Extracting package files...")
    try:
        os.rename(
            join(ROOT, package_name, "meta.latte"),
            join(LATTEPATH, package_name + ".latte")
        )
    except Exception as e:
        err = str(e)
        print(
            Red("ERROR") +
            f(": Could not move meta.latte to LATTEPATH. Error: {err}")
        )
        sys.exit()
    else:
        pass
    
    try:
        os.rename(
            join(ROOT, package_name, "bin.py"),
            join(BINPATH, package_name + ".py")
        )
    except Exception as e:
        err = str(e)
        print(
            Red("ERROR") +
            f(": Could not move bin.py to BINPATH. Exeception: {err}")
        )
    else:
        pass
    
    shutil.rmtree(join(ROOT, package_name))
    print(
        Green("SUCCESS") +
        ": Package '" +
        package_name +
        "' successfully installed!"
    )
    return True


def remove(pkg_name):
    """Remove installed packages with name
    'pkg_name'."""
    
    try:
        os.remove(join(BINPATH, pkg_name + ".py"))
        os.remove(join(LATTEPATH, pkg_name + ".latte"))
    except FileNotFoundError:
        print(
            Red("ERROR") +
            ": Couldn't remove package; Not found in registry."
        )
        sys.exit()
    except Exception as e:
        err = str(e)
        print(
            Red("ERROR") +
            f(": Couldn't remove package. Exception: {err}")
        )
        sys.exit()
    print(Green("SUCCESS") + ": '" + pkg_name + "' removed!")
    return True


def new(pkg_name, path=None):
    """Create a new package with name
    'pkg_name' in the path provided. By
    default, create in the current directory.
    """
    
    if path is None:
        path = os.getcwd()
    pkg_path = join(path, pkg_name)

    try:
        os.mkdir(pkg_path)
        config = open(join(pkg_path, "meta.latte"), "w")
        config.write(meta_template)
        config.close()
        index = open(join(pkg_path, "bin.py"), "w")
        index.write(dev_template)
        index.close()
    except FileExistsError:
        print(
            Red("ERROR") +
            ": Couldn't generate package; directory may already exist."
        )
        sys.exit()
    except Exception as e:
        err = str(e)
        print(
            Red("ERROR") +
            f(": Exception occured. Traceback: {err}")
        )
        sys.exit()
    else:
        print(
            Green("SUCCESS") +
            ": Package '" +
            pkg_name +
            "' generated, check current working directory!"
        )
        return True


def addrepo(url):
    """Add a repo url to the Latte swconfig.
    """

    request = requests.get(url + "/init.latte")
    if request:
        data = request.text
        data_org = SWConfig(data)
    else:
        print(
            Red("ERROR") +
            ": Repository URL is inaccessible. Request returned error code " +
            str(request.status_code) +
            "."
        )
        sys.exit()
    
    try:
        nickname = data_org["NICKNAME"]
    except KeyError:
        print(
            Red("ERROR") +
            ": Repo does not contain an 'init.latte' file."
        )
        sys.exit()
    else:
        repo_listing = open(SWPATH, "a")
        repo_listing.write("\n" + nickname + "=" + url)
        repo_listing.close()
        print(
            Green("SUCCESS") +
            ": '" +
            nickname +
            "' added to repositories!"
        )
        return True


def listrepo(pattern):
    """List repositories in the Latte swconf by pattern."""

    REPOSITORIES = loadconfig(SWPATH)

    if pattern == "all":
        opened = open(SWPATH)
        content = opened.read()
        opened.close()
        as_config = SWConfig(content)
        for repo in as_config.keys():
            print(Cyan(repo) + ": " + Green(as_config[repo]))
    else:
        # Search for repo nickname in swconfig
        try:
            repo_url = REPOSITORIES[pattern]
        except KeyError:
            print(
                Red("ERROR") +
                f(": No repository with nickname {pattern}.")
            )
        else:
            print(Cyan(pattern) + ": " + Green(repo_url))


def delrepo(nickname):
    """Remove repository URL with name 'nickname'."""
    
    REPOSITORIES = loadconfig(SWPATH)
    
    # Check if nickname in swconfig
    if nickname in REPOSITORIES:
        # Pop out the nickname and write back
        removed = REPOSITORIES.pop(nickname)
        # Erase the file first
        swfile_w = open(SWPATH, "w")
        swfile_w.write("")
        # Write back changed dict
        swfile_a = open(SWPATH, "a")
        for key, val in REPOSITORIES.items():
            swfile_a.write("\n" + key + "=" + val)
        swfile_a.close()
        print(
            Green("SUCCESS") +
            ": Removed repo " +
            Green(removed) +
            " with nickname " +
            Cyan(nickname) + "."
        )
        return True
    else:
        print(
            Red("ERROR") +
            f(": Repo with nickname {nickname} not found!")
        )
        sys.exit()


def _main(sargs):
    init()
    
    parser = argparse.ArgumentParser(
        description=desc
    )
    parser.add_argument(
        "method",
        help="install, remove, new, addrepo, listrepo, delrepo",
        type=str
    )
    parser.add_argument(
        nargs="*",
        action="store",
        dest="input",
        help="Package name/repo nickname (i.e, 'universe', 'all')"
    )
    args = parser.parse_args(sargs)

    try:
        opened = open(SWPATH, "r")
        opened.close()
    except:
        opened = open(SWPATH, "w")
        print(
            Yellow("WARNING") +
            ": Repository listing doesn't exist, rebuilding to default..."
        )
        opened.write(
            "universe=https://raw.githubusercontent.com/sn3ksoftware/latte-universe/master"
        )
        opened.close()

    if args.method in func_tuple:
        func = eval(args.method)
        # Check if it is empty
        if not bool(args.input):
            print(
                Red("ERROR") +
                ": Secondary input (i.e latte [method] input) is required."
            )
        else:
            func(args.input[0])
    else:
        print(Red("ERROR") + ": Unknown command '" + args.method + "'!")


if __name__ == "__main__":
    try:
        _main(sys.argv[1:])
    except KeyboardInterrupt:
        print(
            Red("ERROR") +
            ": Latte was terminated with Ctrl-C."
        )
        sys.exit()
    else:
        pass
