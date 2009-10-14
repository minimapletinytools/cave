def enTables(exml):
    if not exml.hasAttribute("name"):
        print "entity has no name attribute"
        return None
    
    name = exml.getAttribute("type")
    if name == "SpikeEn":
        return MW_entity.SpikeEn(exml)