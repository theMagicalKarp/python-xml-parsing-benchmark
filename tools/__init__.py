class XMLProfilerItem(object):
	def __init__(self, file_name, results_dir, result_file_prefix):
		xml_file = open(file_name)
		self.file_data = xml_file.read()
		xml_file.close()
		
		self.results_dir = results_dir
		self.result_file_prefix = result_file_prefix

	def search_tag_by_attribute(self, tag, attribute, attribute_value):
		raise NotImplementedError