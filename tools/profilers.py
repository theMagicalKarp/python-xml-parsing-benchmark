
import cProfile
import pstats

FOUND_RESULTS = 'FOUND_RESULTS'
STAT_FILE_NAME = 'STAT_FILE_NAME'
TEST_NUM = 'TEST_NUM'
PASS = 'PASS'
NAME = 'NAME'

class ResultsItem(object):
    def __init__(self, number, data, file_name):
        self.number = number
        self.passed = False
        self.data = data
        self.file_name = file_name

    def test_results(expected_results):
        result_item.passed = result_item.data == expected_results 
        

class XMLProfilerItem(object):
    def __init__(self, results_dir):
        self.results_dir = results_dir

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                parent_dir, test_number = 0):
        raise NotImplementedError

    def get_results_dir(self, parent_dir = None):
        return '%s' % ('/'.join([parent_dir,self.results_dir]))

    def run_profile(self, to_profile, local_dict):
        profiler = cProfile.Profile()
        results = profiler.runcall(to_profile, local_dict)
        stat_file_name = '%s/profile_%d.stat' % (self.get_results_dir(local_dict['parent_dir']), 
                                                 local_dict['test_number'])
        profiler.dump_stats(stat_file_name)
        return ResultsItem(local_dict['test_number'],
                           results,
                           stat_file_name)
        # return {FOUND_RESULTS: results,
        #         STAT_FILE_NAME: stat_file_name, 
        #         TEST_NUM:local_dict['test_number'], 
        #         NAME:self.results_dir}

import re
class RegexProfile(XMLProfilerItem):
    def __init__(self, results_dir = 'regex'):
        super(RegexProfile, self).__init__(results_dir)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                parent_dir, test_number = 0):
        # search_string = '.*(<.*?id="open_auction2111".*?>)'
        # search_string = '(<.*?id="item21749".*?>)'
        # xml_file = open(self.file_name, 'r')
        reg_ex = '(<(%s).*?%s="(%s)".*?>)' % (tag, attribute, attribute_value)

        def to_profile(local_dict):
            pattern = re.compile(local_dict['reg_ex'])
            found = pattern.search(local_dict['file_data'])
            if found is not None:

                return {'tag':found.group(2),'attribute_value':found.group(3)}
            return {'tag':'', 'attribute_value':''}

        return self.run_profile(to_profile, locals())


from lxml import etree
class LXMLProfile(XMLProfilerItem):
    def __init__(self, results_dir = 'lxml'):
        super(LXMLProfile, self).__init__(results_dir)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                parent_dir, test_number = 0):

        xpath_query = './/%s[@%s="%s"]' % (tag, attribute, attribute_value)
        def to_profile(local_dict):
            tree = etree.fromstring(local_dict['file_data'])
            found = tree.find(local_dict['xpath_query'])
            if found is not None:
                return {'tag':found.tag, 'attribute_value':found.get(local_dict['attribute'])}
            return {'tag':'', 'attribute_value':''}

        return self.run_profile(to_profile, locals())


from xml.parsers import expat
class EXPatProfile(XMLProfilerItem):
    def __init__(self, results_dir = 'expat'):
        super(EXPatProfile, self).__init__(results_dir)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                parent_dir, test_number = 0):

        def to_profile(local_dict):
            found = {'tag':'', 'attribute_value':''}
            def start_element(name, attrs):
                if name == local_dict['tag']:
                    found_attribute = attrs.get(local_dict['attribute'],None)
                    if found_attribute and found_attribute == local_dict['attribute_value']:
                        found['tag'] = name
                        found['attribute_value'] = found_attribute

            p = expat.ParserCreate()
            p.StartElementHandler = start_element
            p.Parse(local_dict['file_data'])
            return found

        return self.run_profile(to_profile, locals())


