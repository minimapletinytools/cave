import PEG_entity
import pedo_player

enList = ("Player", "SolidEntity")
def enTables(exml):
    if not exml.hasAttribute("type"):
        return None
    name = exml.getAttribute("type")
    if name == "Player":
        return pedo_player.Player(exml)
    if name == "SolidEntity":
        return PEG_entity.SolidEntity(exml)
    if name == "Editor":
        return PEG_entity.Editor(exml)