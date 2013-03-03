import tools

class Regex(tools.XMLProfilerItem):
    def __init__(self, file_name):
        super(Regex, self).__init__(file_name)

    def profile_search_tag_by_attribute(self, tag, attribute):
        # search_string = '.*(<.*?id="open_auction2111".*?>)'
        # search_string = '(<.*?id="item21749".*?>)'
        search_string = "<item(?:\D+=\"\S*\")*\s+id=\"(\d*)\""
        pattern = re.compile(search_string)
        results = pattern.search(unicode(f.read()))

        node = results.group(1)

        val_search_string = 'featured="(.*?)"'
        val_pattern = re.compile(val_search_string)
        val_result = val_pattern.search(unicode(node))
        print 'item' ,val_result.group(1)