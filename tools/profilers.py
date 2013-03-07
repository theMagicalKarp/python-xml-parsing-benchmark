
import cProfile
import pstats

FOUND_RESULTS = 'FOUND_RESULTS'
STAT_FILE_NAME = 'STAT_FILE_NAME'
TEST_NUM = 'TEST_NUM'
PASS = 'PASS'
NAME = 'NAME'

class ResultItem(object):
    def __init__(self, number, data, profile_result):
        self.number = number
        self.data = data
        self.profile_result = profile_result
        self.passed = False

    def test(self, expected_results):
        self.passed = self.data == expected_results 
        return self.passed
        

class XMLProfilerItem(object):
    def __init__(self, name):
        self.name = name

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):
        raise NotImplementedError

    def run_profile(self, to_profile, local_dict):
        profiler = cProfile.Profile()
        results = profiler.runcall(to_profile, local_dict)
        # stat_file_name = '%s/profile_%d.stat' % (self.get_results_dir(local_dict['parent_dir']), 
        #                                          local_dict['test_number'])
        # profiler.dump_stats(stat_file_name)
        return ResultItem(local_dict['test_number'],
                           results,
                           profiler)

import re
class RegexProfile(XMLProfilerItem):
    def __init__(self, name = 'regex'):
        super(RegexProfile, self).__init__( name)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):
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
    def __init__(self, name = 'lxml'):
        super(LXMLProfile, self).__init__(name)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):

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
    def __init__(self, name = 'expat'):
        super(EXPatProfile, self).__init__(name)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):

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


from xml.dom.minidom import parse, parseString
class MiniDomProfile(XMLProfilerItem):
    def __init__(self, name = 'minidom'):
        super(MiniDomProfile, self).__init__(name)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):

        def to_profile(local_dict):
            found = {'tag':'', 'attribute_value':''}
            dom = parseString(local_dict['file_data'])
            elements = dom.getElementsByTagName(local_dict['tag'])
            for element in elements:
                element_value = element.getAttribute(local_dict['attribute'])
                # print element_value
                if element_value == local_dict['attribute_value']:
                    found = {'tag':element.tagName, 'attribute_value':element_value}
                    break

            
            return found

        return self.run_profile(to_profile, locals())

