
import cProfile
import pstats


class ResultItem(object):
    """ Results Item 
    Storage for results on a profile that has ran.

    Attributes:
        number: the sample number of the results
        data: the data returned from profiled method
        profile_result: holds and instance of a cProfile object 
            to reference for stats
        passed: shows if the results passed inspections and been validated 
            for returning the correct values
    """
    def __init__(self, number, data, profile_result):
        self.number = number
        self.data = data
        self.profile_result = profile_result
        self.passed = False


    def test(self, expected_results):
        """ Tests if the data returned was correct
        This ensures that all the profilers are running correctly
        and not skewing results.
        Args:
            expected_results: the profiles epxected response
        Returns:
            Whether or not the reuslt did pass
        """
        self.passed = self.data == expected_results 
        return self.passed
        


class XMLProfilerItem(object):
    """ XML Profiler Item
    A class to interface with when wanting to
    profile a new library.

    Attributes:
        name: is an identifier for each profiler
    """
    def __init__(self, name):
        self.name = name

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):
        """ Serach tag by attribute
        This should run a profile on how fast 
        the library can find a xml tag
        by an attribute value.

        Args:
            name: is an identifier for each profiler
            file_data: string representation of the xml file to parse
            tag: the name of the tag we need to find
            attribute: the attribute are we inspecting
            attribute_value: the value of our attrubte we 
                are trying to find
            test_number: this is the sample number we are on
        Returns:
            A populated result item that has the statistical
            data collected from this method
        """
        raise NotImplementedError

    def run_profile(self, to_profile, local_dict):
        """ Run Profile
        Runs the selected method in a controlled enviorement 
        to gather anaylitical data on the execution.

        Args:
            to_profile: the method we are going to profile
            local_dict: the dictionary will hold the context variables
                for which the method will be ran.
        Returns:
            A populated result item that has the statistical
            data collected from this method
        """
        profiler = cProfile.Profile()
        results = profiler.runcall(to_profile, local_dict)
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
class LXMLEtreeProfile(XMLProfilerItem):
    def __init__(self, name = 'lxml etree'):
        super(LXMLEtreeProfile, self).__init__(name)

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



class LXMLParserProfile(XMLProfilerItem):
    def __init__(self, name = 'lxml xml parser'):
        super(LXMLParserProfile, self).__init__(name)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):
        class OurParser:
            found = {'tag':'', 'attribute_value':''}
            def start(self, found_tag, found_attributes):
                if found_tag == tag:
                    found_attribute = found_attributes.get(attribute,None)
                    if found_attribute and found_attribute == attribute_value:
                        self.found['tag'] = found_tag
                        self.found['attribute_value'] = found_attribute
            def close(self):
                return self.found

        def to_profile(local_dict):
            parser = etree.XMLParser(target=local_dict['OurParser']())
            parser.feed(local_dict['file_data'])
            return parser.close()

        return self.run_profile(to_profile, locals())

import StringIO
class LXMLIterProfile(XMLProfilerItem):
    def __init__(self, name = 'lxml iter parser'):
        super(LXMLIterProfile, self).__init__(name)

    def search_tag_by_attribute(self, file_data, tag, attribute, attribute_value, 
                                test_number = 0):
        def to_profile(local_dict):
            context = etree.iterparse(StringIO.StringIO(local_dict['file_data']))
            for action, elem in context:
                if elem.tag == local_dict['tag']:
                    found_value = elem.attrib.get(local_dict['attribute'], None)
                    if found_value and found_value == local_dict['attribute_value']:
                        return {'tag':elem.tag, 'attribute_value':found_value}
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

