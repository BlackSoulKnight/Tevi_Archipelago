import os
import json,pkgutil

from BaseClasses import Location, Region, MultiWorld, ItemClassification
from worlds.generic.Rules import add_rule, set_rule
from .items import TeviItem
from .Utility import evaluate_rule,parse_expression_logic,GetAllUpgradeables
from .Options import TeviOptions
from .TeviToApNames import TeviToApNames



def transitionShuffle(areaData,multiworld:MultiWorld):
    TransitionToBePlaced = []
    placedTransitions = []
    i = 0
    for transitions in areaData["Transitions"]:
        TransitionToBePlaced.append(transitions["Name"])
        i+=1
        transitions["Connections"][0]["Exit"] = "None"

    ConnectedGrap = {}
    for mapNR in areaData:
        for region in areaData[mapNR]:
            ConnectedGrap[region["Name"]] = []
            for connection in region["Connections"]:
                ConnectedGrap[region["Name"]].append(connection["Exit"])

    startArea = "Thanatara Canyon"
    availableExits = recursiveSearch(startArea,ConnectedGrap,[])

    while len(TransitionToBePlaced)>0:
        nextTarget = availableExits[multiworld.random.randint(0,len(availableExits)-1)]
        if not nextTarget in TransitionToBePlaced:
            continue

        newEntrance = TransitionToBePlaced[multiworld.random.randint(0,len(TransitionToBePlaced)-1)]
        if newEntrance == nextTarget:
            continue
        TransitionToBePlaced.sort()
        availableExits.sort()
        while newEntrance in availableExits and TransitionToBePlaced != availableExits:
            newEntrance = TransitionToBePlaced[multiworld.random.randint(0,len(TransitionToBePlaced)-1)]
        availableExits.remove(nextTarget)

        ConnectedGrap[newEntrance] += [nextTarget]
        ConnectedGrap[nextTarget].append(newEntrance)
        ConnectedGrap[newEntrance].remove("None")
        ConnectedGrap[nextTarget].remove("None")

        availableExits = recursiveSearch(startArea,ConnectedGrap,[])




        TransitionToBePlaced.remove(newEntrance)
        TransitionToBePlaced.remove(nextTarget)

    '''
    #No logic
    while len(a)>0:
        val1 = a[multiworld.random.randint(0,len(a)-1)]
        val2 = a[multiworld.random.randint(0,len(a)-1)]
        if val1 == val2: continue


        areaData["Transitions"][val1]["Connections"][0]["Exit"] = areaData["Transitions"][val2]["Name"]
        areaData["Transitions"][val2]["Connections"][0]["Exit"] = areaData["Transitions"][val1]["Name"]

        a.remove(val1)
        a.remove(val2)
    '''
    
    for area in areaData["Transitions"]:
        area["Connections"][0]["Exit"] = ConnectedGrap[area["Name"]][1]
        
    return areaData


def recursiveSearch(startArea,area,visited = []):
    r = []
    if startArea in visited: return r
    else: visited+=[startArea]
    if startArea not in area: return r
    for v in area[startArea]:
        r += recursiveSearch(v,area,visited)
    if startArea.isnumeric():
        if "None" in area[startArea]:
            return r+[startArea]
    return r