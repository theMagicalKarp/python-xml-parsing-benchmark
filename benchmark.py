import tools, sys, getopt

def main(argv):
    # default args
    sample_size = 100
    file_name = 'test_xml/books.xml'
    tag = 'book'
    attribute = 'id'
    attribute_value = 'bk110'

    def show_options():
        print 'benchmark.py -s <sample_size> -f <file_name> -t <tag> -a <attribute> -av <attribute_value>'

    try:
        opts, args = getopt.getopt(argv, 'hs:f:t:a:av:',["sample_size=","file_name=","tag=",
                                                        "attribute=", "attribute_value="])
    except getopt.GetoptError:
        show_options()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            show_options()
            sys.exit()
        elif opt == '-s':
            sample_size = int(arg)
        elif opt == '-f':
            file_name = arg
        elif opt == '-t':
            tag =arg
        elif opt == '-a':
            attribute = arg
        elif opt == '-av':
            attribute_value = arg

    regy = tools.profilers.RegexProfile()
    lexy = tools.profilers.LXMLEtreeProfile()
    maple = tools.profilers.LXMLParserProfile()
    izzy = tools.profilers.LXMLIterProfile()
    patty = tools.profilers.EXPatProfile()
    paxxy = tools.profilers.EXPatHackProfile()

    mini = tools.profilers.MiniDomProfile() # memory hog for large files

    profile_manager = tools.ProfileManager([regy, lexy, maple, izzy, patty, paxxy], file_name)

    profile_manager.search_tag_by_attribute(tag, attribute, attribute_value, sample_size)
    # profile_manager.search_tag_by_attribute('item', 'id', 'item21749',100)
    # profile_manager.search_tag_by_attribute('Column', 'name', 'StudentID',1000)

if __name__ == "__main__":
    main(sys.argv[1:])









