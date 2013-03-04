
import cProfile
import pstats

class XMLProfilerItem(object):

    FOUND_RESULTS = 'FOUND_RESULTS'
    STAT_FILE_NAME = 'STAT_FILE_NAME'
    PASS = 'PASS'

    def __init__(self, results_dir):
        self.results_dir = results_dir

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, test_number = 0):
        raise NotImplementedError

    def get_results_dir(self, parent_dir = None):
        return '%s' % ('/'.join([parent_dir,self.results_dir]))

import re
class RegexProfile(XMLProfilerItem):

    def __init__(self, results_dir = 'regex'):
        super(RegexProfile, self).__init__(results_dir)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, parent_dir, test_number = 0):

        # search_string = '.*(<.*?id="open_auction2111".*?>)'
        # search_string = '(<.*?id="item21749".*?>)'
        # xml_file = open(self.file_name, 'r')
        reg_ex = '(<(%s).*?%s="(%s)".*?>)' % (tag, attribute, attribute_value)

        def to_profile(search_string, xml_data):
            pattern = re.compile(search_string)
            found = pattern.search(xml_data)
            if found is not None:

                return {'tag':found.group(2),'attribute_value':found.group(3)}
            return None

        profiler = cProfile.Profile()
        results = profiler.runcall(to_profile, reg_ex, file_data)
        stat_file_name = '%s/profile_%d.stat' % (self.get_results_dir(parent_dir), test_number)
        profiler.dump_stats(stat_file_name)

        search_passed = {'tag' :tag, 'attribute_value': attribute_value} == results

        return {self.FOUND_RESULTS: results, self.STAT_FILE_NAME: stat_file_name, self.PASS: search_passed}
