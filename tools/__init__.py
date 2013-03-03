class XMLProfilerItem(object):
	def __init__(self, file_name):
		self.file_name = file_name

	def profile_search_tag_by_attribute(self, tag, attribute):
		raise NotImplementedError