import profilers
import os
import pstats
    
class ProfileManager(object):
    def __init__(self, profiler_list, xml_file_name, results_dir = 'results'):
        self.profiler_list = profiler_list
        self.results_dir = results_dir
        xml_file = open(xml_file_name)
        self.xml_data = xml_file.read()
        xml_file.close()


    def __get_complete_report(self, completed_results):
        stats = pstats.Stats(completed_results[0][profilers.file_name])
        for completed_result in completed_results[1:]: 
            stats.add(completed_result.file_name)
        return stats

    # def __stamp_test_results(self, result_item, expected_results):
        
    #     print 'Test %s of %s has %s' % (result_item.number,
    #                                     '<put name here>',
    #                                     'passed!' if result_item.passed else 'failed...')
    #     return result_item

    def search_tag_by_attribute(self, tag, attribute, attribute_value, 
                                sample_size = 25, results_dir = 'search_tag_by_attribute'):
        results_by_profile = {}
        stats_by_profile = {}
        expected_results = {'tag':tag, 'attribute_value':attribute_value}


        testing_dir = '%s/%s' % (self.results_dir, results_dir)

        for profiler in self.profiler_list:
            print '----- Running Profiler on %s -----' % (profiler.results_dir)

            results_path = profiler.get_results_dir(testing_dir)
            if not os.path.exists(results_path): 
                os.makedirs(results_path)

                
            # results_by_profile[profiler] = [self.__stamp_test_results(
            #                                 profiler.search_tag_by_attribute(self.xml_data, 
            #                                                                  tag,
            #                                                                  attribute, 
            #                                                                  attribute_value, 
            #                                                                  testing_dir, 
            #                                                                  x),
            #                                 expected_results) for x in xrange(sample_size)]

            stats_by_profile[profiler] = self.__get_complete_report(results_by_profile[profiler])

            stats_by_profile[profiler].dump_stats('%s/%s.stat' % (testing_dir, 
                                                                  profiler.results_dir ))


        return stats_by_profile

# [ results[profilers.STAT_FILE_NAME] for results in results_by_profile[profiler]]

