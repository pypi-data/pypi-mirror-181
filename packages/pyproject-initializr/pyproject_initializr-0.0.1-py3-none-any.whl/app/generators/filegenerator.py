class FileGenerator():

	def create_files(self, file_map):

		for path in file_map:
			with open(path, 'w') as file_writer:
				file_writer.write(file_map[path])