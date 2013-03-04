import profilers
import os

class ProfileManager(object):
    def __init__(self, profiler_list, xml_file_name, results_dir = 'results'):
        self.profiler_list = profiler_list
        self.results_dir = results_dir
        xml_file = open(xml_file_name)
        self.xml_data = xml_file.read()
        xml_file.close()

    def search_tag_by_attribute(self, tag, attribute, attribute_value, sample_size = 5, results_dir = 'search_tag_by_attribute'):
        test_results = {}

        testing_dir = '%s/%s' % (self.results_dir, results_dir)
        for profiler in self.profiler_list:

            results_path = profiler.get_results_dir(testing_dir)
            if not os.path.exists(results_path): 
                os.makedirs(results_path)

            test_results[profiler] = [profiler.search_tag_by_attribute(self.xml_data, tag, attribute, attribute_value, testing_dir, x) for x in xrange(sample_size)]




