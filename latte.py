# A package manager meant for Pythonista, built on StaSh.

import requests
import sys
import argparse
from os import remove, mkdir, rename, listdir
from shutil import rmtree

class ansi:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	ORANGE = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def Orange(text):
	return ansi.ORANGE+text+ansi.ENDC
def Green(text):
	return ansi.GREEN+text+ansi.ENDC
def Red(text):
	return ansi.RED+text+ansi.ENDC
		
class SWConfig (object): # Parser for the config files such as the repository listing.
	def __init__(self, content):
		self.data = {}
		for line in content.splitlines():
			key = line.split("=")[0]
			value = line.split("=")[1]
			self.data[key] = value
			
	def __getitem__(self, key):
		return self.data[key]
		
	def keys(self):
		return self.data.keys()
		
def download_package(url, package_name): # Handles the installation of packages directories (since they're no longer tarfiles)
	content_listing = ["bin.py", "meta.latte"]
	mkdir(package_name)
	for item in content_listing:
		requested = requests.get(url+"/"+package_name+"/"+item)
		content = requested.text
		requested.close()
		opened = open(package_name+"/"+item, "w")
		opened.write(content)
		opened.close()

def main(sargs):
	parser = argparse.ArgumentParser()
	parser.add_argument("method", help="What action to perform (install, remove, etc)", type=str)
	parser.add_argument("package", help="Name of package", type=str)
	args = parser.parse_args(sargs)
	
	try:
		opened = open(".latte-repos.swconf", "r")
		opened.close()
	except:
		opened = open(".latte-repos.swconf", "w")
		print(Orange("PROBLEM") + ": Repository listing doesn't exist, rebuilding to default...")
		opened.write("universe=https://raw.githubusercontent.com/Seanld/latte-universe/master")
		opened.close()
	
	repo_listing_opened = open(".latte-repos.swconf", "r")
	listing_content = repo_listing_opened.read()
	repo_listing_opened.close()
	REPOSITORIES = SWConfig(listing_content)
		
	if args.method == "install":
		packageSplitted = args.package.split("/")
		try:
			package_name = packageSplitted[1]
			repo_to_use = REPOSITORIES[packageSplitted[0]]
		except IndexError:
			print(Orange("WARNING") + ": Did not specify repository, using universe repository instead.")
			repo_to_use = REPOSITORIES["universe"]
			package_name = packageSplitted[0]
		print("Downloading " + repo_to_use + "/" + package_name)
		try:
			download_package(repo_to_use, package_name)
		except:
			print(Red("ERROR") + ": Couldn't find package")
		# Move to correct locations
		print("Installing")
		try:
			rename(package_name+"/meta.latte", "/stash_extensions/latte/"+package_name+".latte")
		except:
			mkdir("/stash_extensions/latte")
			rename(package_name+"/meta.latte", "/stash_extensions/latte/"+package_name+".latte")
		rename(package_name+"/bin.py", "/stash_extensions/bin/"+package_name+".py")
		rmtree(package_name)
		print(Green("SUCCESS") + ": Package installed!")
	elif args.method == "remove":
		remove("/stash_extensions/bin/"+args.package+".py")
		remove("/stash_extensions/latte/"+args.package+".latte")
		print(Green("SUCCESS") + ": Removed "+args.package+" successfully!")
	elif args.method == "update":
		print("Jeez! Sorry, but we are currently working on self-update capabilities. For now, just redo the install process to update.")
	elif args.method == "new":
		try:
			mkdir(args.package)
			config = open(args.package+"/meta.latte", "w")
			config.write("developer=Your name here\ndescription=Enter description of your app here\nversion=0.1")
			config.close()
			index = open(args.package+"/bin.py", "w")
			index.write("# This is just an example template. You can change this all you like.\n\nimport sys\nimport argparse\n\ndef main(sargs):\n\tparser = argparse.ArgumentParser()\n\tparser.add_argument('echo', help='What you want the command to echo back.')\n\targs = parser.parse_args(sargs)\n\t\n\tprint('Echoing back: '+args.echo)\n\nif __name__ == '__main__':\n\tmain(sys.argv[1:])")
			index.close()
			print(Green("SUCCESS") + ": Made new package template '"+args.package+"'!")
		except:
			print(Red("ERROR") + ": Couldn't build, directory already exists.")
	elif args.method == "add-repo":
		try:
			request = requests.get(args.package+"/init.latte")
			data = request.text
			request.close()
			data_org = SWConfig(data)
			nickname = data_org["NICKNAME"]
			repo_listing = open(".latte-repos.swconf", "a")
			repo_listing.write("\n"+nickname+"="+args.package)
			repo_listing.close()
			print(Green("SUCCESS") + ": '"+nickname+"' added to repositories!")
		except:
			print(Orange("REPO ISSUE") + ": Either repository doesn't exist, or does not contain an 'init.latte' file.")
	elif args.method == "list-repos":
		if args.package == "all":
			opened = open(".latte-repos.swconf")
			content = opened.read()
			opened.close()
			as_config = SWConfig(content)
			for repo in as_config.keys():
				print(Green(repo) + ": " + Orange(as_config[repo]))
	else:
		print(Red("SYNTAX ERROR") + ": Unknown command '"+args.method+"'!")

if __name__ == "__main__":
	main(sys.argv[1:])
