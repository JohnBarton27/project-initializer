# Initializes a new project
import argparse
import configparser
import logging
import json
import os
import pathlib
import pprint
import requests
import shlex
import subprocess

from Project import Project

parser = argparse.ArgumentParser(description="Initialize a new programming project")
parser.add_argument("name", help="Name of the project to initialize")
parser.add_argument("--description", help="Description for this project")

args = parser.parse_args()

# Get project initializer directory
initializer_root = pathlib.Path(__file__).parent.absolute()

# Load config file
config = configparser.ConfigParser()
config.read(os.path.join(initializer_root, "config.ini"))

# Log config
logging.basicConfig(level=logging.INFO)

# Create project based on passed name
project = Project(args.name, description=args.description)

# Make a directory in projects folder
projects_dir = os.path.join(config["local"]["projects_dir"], project.no_spaces_name)

# Ensure the path doesn't already exist
if os.path.exists(projects_dir):
    raise Exception("Project directory '{}' already exists!".format(projects_dir))

logging.info("Creating local directory for '{}' at {}".format(project.pretty_name, projects_dir))
os.mkdir(projects_dir)
os.chdir(projects_dir)

# Initialize git repo
subprocess.run(shlex.split("git init"))

with open("README.md", "w") as readme:
    readme.write("# {}\n{}".format(project.pretty_name, project.description))

# Add README to git
subprocess.run(shlex.split("git add README.md"))

# Initial Commit
subprocess.run(shlex.split("git commit -m \"Initial Commit\""))

# Add Github repository
github_username = config["github"]["username"]
github_api_token = config["github"]["api_token"]

print(github_username, github_api_token)

url = "https://api.github.com/user/repos"
data = {
    "name": project.no_spaces_name,
    "private": False
}

response = requests.post(url, data=json.dumps(data), headers={'Authorization': 'token {}'.format(github_api_token)})

use_ssh = config.getboolean("github", "use_ssh")
remote_url = response.json()["ssh_url"] if use_ssh else response.json()["clone_url"]
subprocess.run(shlex.split("git remote add origin {}".format(remote_url)))
subprocess.run(shlex.split("git push -u origin master"))
