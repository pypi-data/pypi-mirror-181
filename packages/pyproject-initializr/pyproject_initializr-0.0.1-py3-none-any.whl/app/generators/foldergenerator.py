import os


class FolderGenerator():

	def create_folders(self, folder_paths):
		for path in folder_paths:
			os.makedirs(path)

