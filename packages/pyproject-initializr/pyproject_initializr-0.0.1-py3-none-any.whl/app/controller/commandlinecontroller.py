from app.generators.filegenerator import FileGenerator
from app.generators.foldergenerator import FolderGenerator 
from app.controller import GITIGNORE_CONTENT, EXAMPLE_UNIT_TEST_CONTENT

class CommandLineController():

	def __init__(self):
		self.file_generator = FileGenerator()
		self.folder_generator = FolderGenerator()

	def run(self, project_name):
		# create folders
		folders = [
			project_name, f"{project_name}/src/app", f"{project_name}/tests"
		]
		self.folder_generator.create_folders(folders)
		# create files
		file_map = {

			f"{project_name}/src/app/__init__.py": "",
			f"{project_name}/tests/__init__.py": "",
			f"{project_name}/tests/testexample.py": EXAMPLE_UNIT_TEST_CONTENT,
			f"{project_name}/.gitignore": GITIGNORE_CONTENT,
			f"{project_name}/README.md": "",

		}
		self.file_generator.create_files(file_map)
