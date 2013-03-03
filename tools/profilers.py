import tools
import cProfile
import pstats
class RegexProfile(tools.XMLProfilerItem):


    def __init__(self, file_name, results_dir, result_file_prefix = 'regex'):
        super(RegexProfile, self).__init__(file_name, results_dir, result_file_prefix)

    def search_tag_by_attribute(self, tag, attribute, attribute_value, test_number = 0):
        import re
        # search_string = '.*(<.*?id="open_auction2111".*?>)'
        # search_string = '(<.*?id="item21749".*?>)'
        # xml_file = open(self.file_name, 'r')
        reg_ex = '(<(%s).*?%s="(%s)".*?>)' % (tag, attribute, attribute_value)

        def to_profile(search_string, xml_data):
            pattern = re.compile(search_string)
            found = pattern.search(self.file_data)
            if found is not None:
                return {'tag':found.group(2),'attribute_value':found.group(3)}
            return None

        profiler = cProfile.Profile()
        results = profiler.runcall(to_profile, reg_ex, self.file_data)
        stat_file_name= '%s/%s_%d.stats' % (self.results_dir, self.result_file_prefix, test_number)
        profiler.dump_stats(stat_file_name)

        return {'results':results, 'stat_file_name':stat_file_name}
