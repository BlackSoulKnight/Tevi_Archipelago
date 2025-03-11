import os
import json,pkgutil

from typing import List, Set, Dict, Optional, Callable
from BaseClasses import Location, Region, MultiWorld, ItemClassification,LocationProgressType
from worlds.generic.Rules import add_rule, set_rule
from .items import TeviItem
from .Utility import evaluate_rule,parse_expression_logic,GetAllUpgradeables
from .Options import TeviOptions
from .TeviToApNames import TeviToApNames
from .transitionShuffle import *



class TeviLocation(Location):
    """Tevi Location Definition"""
    game: str = "Tevi"

class RegionDef:
    """
    This class provides methods associated with defining and connecting regions, locations,
    and the access rules for those regions and locations.
    """

    def __init__(self, multiworld: MultiWorld, player: int, options:TeviOptions):
        self.data = {}
        file = pkgutil.get_data(__name__, os.path.join('resources', 'Area.json')).decode()
        self.data["Area"] = json.loads(file)
        file = pkgutil.get_data(__name__, os.path.join('resources', 'Location.json')).decode()
        self.data["Location"] = json.loads(file)
        self.edges = {}
        self.locations = {}
        self.locationsItem = {}
        self.region_names = {}
        self.event_list =[]
        if options.transitionShuffle.value > 0:
            self.data["Area"] = transitionShuffle(self.data["Area"],multiworld)
        self.transitions = self.data["Area"]["Transitions"]
        self._get_region_name_list()
        self._get_location_rules()
        self.player = player
        self.multiworld = multiworld
        self.options = options

    def set_regions(self):
        """
        This method defines the regions from the existing randomizer data.
        It will then add it to the AP world.

        These regions are connected in the connect_region method.

        :returns: None
        """
        for name in self.region_names:
            self.multiworld.regions.append(Region(name, self.player, self.multiworld))
                
        
        self.multiworld.regions.append(Region("Menu", self.player, self.multiworld))

    def connect_regions(self):
        """
        This method will connect the regions defined in the set_regions method.
        That method MUST be called first!

        :returns: None
        """

        regions = self.multiworld.regions.region_cache[self.player]
        regions["Menu"].connect(regions["Thanatara Canyon"])


        for from_location in self.edges:
            for to_loaction in self.edges[from_location]:
                if to_loaction == "":
                    continue
                rule = self.edges[from_location][to_loaction]
                ap_rule = parse_expression_logic(rule)
                ap_rule = evaluate_rule(ap_rule,self.player,regions,self.options)
                regions[from_location].add_exits([to_loaction],{to_loaction:ap_rule})


    def set_locations(self, location_name_to_id):
        """
        This method creates all of the item locations within the AP world, and appends it to the
        appropriate region. It will also add the access rule for these locations, sourced from the
        existing randomizer.

        :dict[str, int] location_name_to_id: Map for location name -> id number
        :returns int: The total number of locations
        """
        total_locations = 0
        locations = self.data["Location"]
        regions = self.multiworld.regions.region_cache[self.player]
        for location in locations:

            location_name = location["LocationName"]
            region_name = location["Location"]


            rule = self.locations[location_name]
            ap_location = TeviLocation(
                self.player,
                location_name,
                location_name_to_id[location_name],
                regions[region_name]
            )
            ap_rule = parse_expression_logic(rule)
            ap_rule = evaluate_rule(ap_rule,self.player,regions,self.options)
            if "EVENT" in self.locationsItem[location_name]:
                self.event_list.append(({"Location":region_name,"Event":self.locationsItem[location_name],"Rule":ap_rule}))
                continue
            set_rule(ap_location,ap_rule)
            if("LibraryExtra" in rule and not self.options.superBosses.value > 0):
                ap_location.progress_type = LocationProgressType.EXCLUDED
            regions[region_name].locations.append(ap_location)
            total_locations += 1
        return total_locations

    def set_events(self):
        regions = self.multiworld.regions.region_cache[self.player]
        if self.options.open_morose.value:
            openMorose = TeviLocation(self.player,"OpenMorose",None,regions["Thanatara Canyon"])
            openMorose.place_locked_item(TeviItem("OpenMorose",ItemClassification.progression,None,self.player))
            regions["Thanatara Canyon"].locations.append(openMorose)
        eventNumber = 0
        for event in self.event_list:
            eventNumber+=1
            if "EVENT_Memine5" in event["Event"]:
                a = 2
            newEvent = TeviLocation(self.player,f'{event["Location"]} {event["Event"]} {eventNumber}',None,regions[event["Location"]])
            newEvent.show_in_spoiler = False
            if event["Rule"] != "":
                if isinstance(event["Rule"],str):
                    ap_rule = parse_expression_logic(event["Rule"])
                    ap_rule = evaluate_rule(ap_rule,self.player,regions,self.options)
                    event["Rule"] = ap_rule
                set_rule(newEvent,event["Rule"])
            newEvent.place_locked_item(TeviItem(event["Event"],ItemClassification.progression,None,self.player))
            regions[event["Location"]].locations.append(newEvent)



    def _get_region_name_list(self):
        regions = []
        self.edges = {}
        for maps in self.data["Area"].values():
            for fromArea in maps:
                regions.append(fromArea["Name"])
                for toArea in fromArea["Connections"]:
                    if fromArea["Name"] in self.edges and toArea["Exit"] in self.edges[fromArea["Name"]]:
                        self.edges[fromArea["Name"]][toArea["Exit"]] += f" || ({toArea['Method']})"
                    else:
                        if not fromArea["Name"] in self.edges:
                            self.edges[fromArea["Name"]] = {}
                        self.edges[fromArea["Name"]][toArea["Exit"]] = f"({toArea['Method']})" 
        self.region_names = regions

    def _get_location_rules(self):
        self.locations = {}
        for v in self.data["Location"]:
            location_name = v["LocationName"]
            self.locations[location_name] = ""
            self.locationsItem[location_name] = v["Itemname"]
            for ve in v["Requirement"]:
                if self.locations[location_name] == "":
                    self.locations[location_name] = f"({ve['Method']})"
                else:
                    self.locations[location_name] += f" || ({ve['Method']})"

    

  
def get_all_possible_locations():
    """
    This method retrieves a list of all locations in Rabi-Ribi. This is needed when instantiating the world.

    :returns: A full list of location names.
    """
    file = pkgutil.get_data(__name__, os.path.join('resources', 'Location.json')).decode()
    data = json.loads(file)

    
    return [location["LocationName"] for location in data]

def get_location_group_names():
    locations = get_all_possible_locations()
    location_name_groups = {}

    for v in locations:
        if "EVENT" in v:
            continue
        name = v.split("-")
        name[0] = name[0].strip()
        if "Memine" in name[0]:
            name[0] = "Memine"
        if len(name) == 1:
            continue
        if name[0] in location_name_groups:
            location_name_groups[name[0]].add(name[1])
        else:
            location_name_groups[name[0]] = {name[1]}
        if "shop" in v.lower():
            if "Shop" in location_name_groups:
                location_name_groups["Shop"].add(v)
            else:
                location_name_groups["Shop"] = {v}
    return location_name_groups