#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A package manager meant for Pythonista, built on StaSh.
Code copyright (c) Seanld/sn3ksoftware 2017-2019, MIT License.
This is a fork by sn3ksoftware to enable
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

__version__ = "2.0.1-alpha"
__author__ = "Seanld/sn3ksoftware"
__copyright__ = "Copyright (c) Seanld/sn3ksoftware 2017-2019, MIT License."
desc = "apt-get for Pythonista, version {v}.\n{c}".format(
    v=__version__,
    c=__copyright__
)


def onstash():
    """Check if Latte is running on StaSh."""
    try:
        globals()['_stash']
    except KeyError:
        return False
    else:
        return True


if onstash():
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


if onstash():
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
            else:
                key = line.split("=")[0]
                value = line.split("=")[1]
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
                print(
                    Red("ERROR") +
                    ": Could not create {p}. Traceback: {err}".format(
                            p=path,
                            err=str(e)
                        )
                )
            else:
                continue


def download_package(url, package_name):
    """Handles the installation of packages
    directories (since they're no longer
    tarfiles)"""
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


def main(sargs):
    init()
    
    parser = argparse.ArgumentParser(
        description=desc
    )
    parser.add_argument(
        "method",
        help="install, remove, new, add-repo, list-repos, del-repo",
        type=str
    )
    parser.add_argument(
        "package",
        help="Name of package/nickname of repo (i.e, universe, all)",
        type=str
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

    repo_listing_opened = open(SWPATH, "r")
    listing_content = repo_listing_opened.read()
    repo_listing_opened.close()
    REPOSITORIES = SWConfig(listing_content)

    if args.method == "install":
        packageSplitted = args.package.split("/")
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
            print(
                Red("ERROR") +
                ": Unhandled exception occured. Content: " +
                e
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
            print(
                Red("ERROR") +
                ": Could not move meta.latte to LATTEPATH. Error: {str(e)}"
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
            print(
                Red("ERROR") +
                ": Could not move bin.py to BINPATH. Exeception: {str(e)}"
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
    elif args.method == "remove":
        try:
            os.remove(join(BINPATH, args.package + ".py"))
            os.remove(join(LATTEPATH, args.package + ".latte"))
        except FileNotFoundError:
            print(
                Red("ERROR") +
                ": Couldn't remove package; Not found in registry."
            )
            sys.exit()
        except Exception as e:
            print(
                Red("ERROR") +
                ": Couldn't remove package. Exception: {err}".format(
                        err=str(e)
                    )
            )
            sys.exit()
        print(Green("SUCCESS") + ": '" + args.package + "' removed!")
    elif args.method == "new":
        try:
            os.mkdir(args.package)
            config = open(join(args.package, "meta.latte"), "w")
            config.write(meta_template)
            config.close()
            index = open(join(args.package, "bin.py"), "w")
            index.write(dev_template)
            index.close()
            print(
                Green("SUCCESS") +
                ": Package '" +
                args.package +
                "' generated, check current working directory!"
            )
        except FileExistsError:
            print(
                Red("ERROR") +
                ": Couldn't generate package; directory may already exist."
            )
        except Exception as e:
            print(
                Red("ERROR") +
                ": Exception occured. Traceback: " +
                str(e)
            )
    elif args.method == "add-repo":
        try:
            request = requests.get(args.package + "/init.latte")
            data = request.text
            request.close()
            data_org = SWConfig(data)
            nickname = data_org["NICKNAME"]
            repo_listing = open(SWPATH, "a")
            repo_listing.write("\n" + nickname + "=" + args.package)
            repo_listing.close()
            print(
                Green("SUCCESS") +
                ": '" +
                nickname +
                "' added to repositories!"
                )
        except:
            print(
                Red("ERROR") +
                ": Either repository doesn't exist," +
                "or does not contain an 'init.latte' file."
            )
    elif args.method == "list-repos":
        if args.package == "all":
            opened = open(SWPATH)
            content = opened.read()
            opened.close()
            as_config = SWConfig(content)
            for repo in as_config.keys():
                print(Cyan(repo) + ": " + Green(as_config[repo]))
        else:
            # Search for repo nickname in swconfig
            try:
                repo_url = REPOSITORIES[args.package]
            except KeyError:
                print(
                    Red("ERROR") +
                    ": No repository with nickname {name}.".format(
                            name=args.packqge
                        )
                )
            else:
                print(Cyan(args.package) + ": " + Green(repo_url))
    elif args.method == "del-repo":
        # Check if nickname in swconfig
        repo_d = REPOSITORIES.data
        if args.package in repo_d:
            # Pop out the nickname and write back
            removed = repo_d.pop(args.package)
            # Erase the file first
            swfile_w = open(SWPATH, "w")
            swfile_w.write("")
            # Write back changed dict
            swfile_a = open(SWPATH, "a")
            for key, val in repo_d.items():
                swfile_a.write("\n" + key + "=" + val)
            swfile_a.close()
            print(
                Green("SUCCESS") +
                ": Removed repo " +
                Green(removed) +
                " with nickname " +
                Cyan(args.package) + "."
            )
        else:
            print(
                Red("ERROR") +
                ": Repo with nickname {name} not found!".format(
                        name=args.package
                    )
            )
    else:
        print(Red("ERROR") + ": Unknown command '" + args.method + "'!")


if __name__ == "__main__":
    main(sys.argv[1:])
