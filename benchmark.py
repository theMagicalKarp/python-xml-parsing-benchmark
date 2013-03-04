import sys, cProfile, re
from xml.parsers import expat
from lxml import etree
import tools

def expat_parse(f):
   
    def start_element(name, attrs):
        if name == 'item':
            id_attribute = attrs.get('id',None)
            if id_attribute and id_attribute == 'item21749':
                print name,attrs['featured']

    p = expat.ParserCreate()
    p.StartElementHandler = start_element
    p.Parse(f)

def reg_ex_parse(f):
    # search_string = '.*(<.*?id="open_auction2111".*?>)'
    # search_string = '(<.*?id="item21749".*?>)'
    # search_string = "(<item(?:\D+=\"\S*\")*\s+id=\"(item21749)\")"
    search_string = '(<(item).*?id="(item21749)".*?>)'
    pattern = re.compile(search_string)
    results = pattern.search(unicode(f.read()))


    print results.group(2), results.group(3)
    # val_search_string = 'featured="(.*?)"'
    # val_pattern = re.compile(val_search_string)
    # val_result = val_pattern.search(unicode(node))
    # print 'item' ,val_result.group(1)



def lxml_parse(f):
    tree = etree.fromstring(f)

    result = tree.find('//item[@id="item21749"]')
    print result.tag, result.get('featured')

    
if __name__ == "__main__":
    # file_name = sys.argv[1]

    file_name = "test_xml/mega.xml"
    regy = tools.profilers.RegexProfile()

    profile_manager = tools.ProfileManager([regy], file_name)
    
    profile_manager.search_tag_by_attribute('item', 'id', 'item21749')

    # for x in xrange(30):
    #     regy.profile_search_tag_by_attribute_value('item', 'id', 'item21749',x)

    # f1 = open(file_name,'r')
    # print 'REG EX RESULTS'
    # cProfile.runctx('reg_ex_parse(file)',globals(), {'file':f1})
    # print '-------------------------------------\n\n'
    # f1.close()

    # f1 = open(file_name,'r')
    # print 'eXPAT RESULTS'
    # cProfile.runctx('expat_parse(file)',globals(), {'file':f1})
    # print '-------------------------------------\n\n'
    # f1.close()

    # f1 = open(file_name,'r')
    # print 'LXML RESULTS'
    # cProfile.runctx('lxml_parse(file)',globals(), {'file':f1})
    # print '-------------------------------------\n\n'
    # f1.close()





