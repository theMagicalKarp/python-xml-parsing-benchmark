import tools


    
if __name__ == "__main__":
    file_name = "test_xml/mega.xml"
    regy = tools.profilers.RegexProfile()
    lexy = tools.profilers.LXMLProfile()
    patty = tools.profilers.EXPatProfile()

    profile_manager = tools.ProfileManager([regy, patty, lexy], file_name)
    
    profile_manager.search_tag_by_attribute('item', 'id', 'item21749',10)






