import tools



if __name__ == "__main__":
    file_name = "test_xml/mega.xml"

    regy = tools.profilers.RegexProfile()
    lexy = tools.profilers.LXMLProfile()
    patty = tools.profilers.EXPatProfile()
    mini = tools.profilers.MiniDomProfile()

    profile_manager = tools.ProfileManager([lexy, regy, patty], file_name)

    profile_manager.search_tag_by_attribute('item', 'id', 'item21749',3)
    # profile_manager.search_tag_by_attribute('Column', 'name', 'StudentID',1000)








