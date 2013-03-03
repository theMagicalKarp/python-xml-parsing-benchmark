import sys, cProfile, re
from xml.parsers import expat
from lxml import etree

def expat_parse(f):
   
    def start_element(name, attrs):
        if name == 'item':
            id_attribute = attrs.get('id',None)
            if id_attribute and id_attribute == 'item21749':
                print name,attrs['featured']

    p = expat.ParserCreate()
    p.StartElementHandler = start_element
    p.ParseFile(f)

def reg_ex_parse(f):
    # search_string = '.*(<.*?id="open_auction2111".*?>)'
    search_string = '(<.*?id="item21749".*?>)'
    pattern = re.compile(search_string)
    results = pattern.search(unicode(f.read()))

    node = results.group(1)

    val_search_string = 'featured="(.*?)"'
    val_pattern = re.compile(val_search_string)
    val_result = val_pattern.search(unicode(node))
    print 'item' ,val_result.group(1)



def lxml_parse(f):
    tree = etree.parse(f)

    result = tree.find('//item[@id="item21749"]')
    print result.tag, result.get('featured')

    
if __name__ == "__main__":
    # file_name = sys.argv[1]
    # cProfile.run('reg_ex_parse("hello")')
    file_name = "test_xml/mega.xml"
    # lxml_parse('')

    # f1 = open(file_name,'r')
    # print 'REG EX RESULTS'
    # cProfile.runctx('reg_ex_parse(file)',globals(), {'file':f1})
    # print '-------------------------------------\n\n'
    # f1.close()

    # f1 = open(file_name,'r')
    # print 'LXML RESULTS'
    # cProfile.runctx('lxml_parse(file)',globals(), {'file':f1})
    # print '-------------------------------------\n\n'
    # f1.close()

    f1 = open(file_name,'r')
    print 'eXPAT RESULTS'
    cProfile.runctx('expat_parse(file)',globals(), {'file':f1})
    print '-------------------------------------\n\n'
    f1.close()



