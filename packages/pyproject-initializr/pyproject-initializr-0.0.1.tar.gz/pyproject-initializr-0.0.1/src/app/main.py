from app.controller.commandlinecontroller import CommandLineController

import argparse
import os
import shutil
import traceback

def main():
	# print("hello world")
	parser = argparse.ArgumentParser(description="Creates a project directory with some default files and directories")
	parser.add_argument("--createproject", help="Creates a project directory in current dir with given project name")
	args = parser.parse_args()
	if args.createproject:
		project_name = args.createproject
		print(f"Creating project {project_name}")
		if project_name in os.listdir():
			response = input(f"Project {project_name} already exists in current directory. Delete? (y/n) ")
			if response.lower() == 'y':
				shutil.rmtree(project_name)
			else:
				exit()
		controller = CommandLineController()
		controller.run(args.createproject)
		print(f"Created project {project_name}")