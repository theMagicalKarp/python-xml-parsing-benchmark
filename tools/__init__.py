
import sys, profilers, pstats

class ProfileManager(object):
    def __init__(self, profiler_list, xml_file_name):
        self.profiler_list = profiler_list
        xml_file = open(xml_file_name)
        self.xml_data = xml_file.read()
        xml_file.close()

    def print_stats(self, stats, results, sample_size):
        num_passed = sum(res.passed for res in results)
        print '////////////////////////////////////////////////////////'
        print '/////    Average number of calls per sample, %s' % (stats.total_calls/(sample_size))
        print '/////    Average run time per sample, %s seconds' % (stats.total_tt/(sample_size))
        print '/////    %d out of %d test passed' % (num_passed, sample_size)
        print '////////////////////////////////////////////////////////'
        stats.sort_stats('time')
        stats.print_stats()

    def print_current_status(self, to_write):
        print to_write,
        sys.stdout.flush()
        print "\r",

    def search_tag_by_attribute(self, tag, attribute, attribute_value, 
                                sample_size = 25):
        results_by_profile = {}
        stats_by_profile = {}
        expected_result = {'tag':tag, 'attribute_value':attribute_value}

        for profiler in self.profiler_list:
            print '----- Running Profiler on %s -----' % (profiler.name)

            results_by_profile[profiler] = []
            num_passed = 0
            for sample_num in xrange(sample_size):
                self.print_current_status(' Currently profiling sample %s...' % (sample_num+1))
                result = profiler.search_tag_by_attribute(self.xml_data, 
                                                          tag, attribute, attribute_value, 
                                                          sample_num)
                num_passed = num_passed+1 if result.test(expected_result) else num_passed
                results_by_profile[profiler].append(result)

                if profiler in stats_by_profile:
                    stats_by_profile[profiler].add(result.profile_result)
                else:
                    stats_by_profile[profiler] = pstats.Stats(result.profile_result)

            self.print_stats(stats_by_profile[profiler], results_by_profile[profiler], sample_size)
        return stats_by_profile
