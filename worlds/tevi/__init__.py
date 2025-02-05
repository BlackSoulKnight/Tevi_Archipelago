"""
This module serves as an entrypoint into the Tevi AP world.
"""
from collections import defaultdict
from typing import ClassVar, Dict, Set,List

from BaseClasses import ItemClassification
from Fill import swap_location_item
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from .items import TeviItem, item_table, event_item_table, get_items_by_category,get_potential_new_item,get_potential_new_filler_item
from .Regions import RegionDef, get_all_possible_locations
from .Options import TeviOptions
from .Web import TeviWeb
from .Utility import GetAllUpgradeables
from .TeviToApNames import TeviToApNames,ApNamesToTevi

class TeviWorld(World):
    """
    Description of TEVI
    """
    game: str = "Tevi"
    options_dataclass = TeviOptions
    options: TeviOptions
    topology_present: bool = False
    web: WebWorld = TeviWeb()

    base_id: int = 44966541000

    item_name_groups: Dict[str, Set[str]] = {}
    location_name_groups: Dict[str, Set[str]] = {}

    item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}
    location_name_to_id: Dict[str, int] = {
        name: id_num for
        id_num, name in enumerate(get_all_possible_locations(), base_id)
    }

    item_name_groups = {

    }

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.total_locations = 0
        self.transitionShuffle = []

    def generate_early(self) -> None:
        """Set world specific generation properties"""
        #Set up the number of find able Gears
        item_table["Astral Gear"].quantity = self.options.gear_count.value
        # Reduce Goal to match Gear count if its greater
        if self.options.gear_count.value < self.options.goal_count.value:
            self.options.goal_count.value = self.options.gear_count.value



    def create_item(self, name: str) -> TeviItem:
        """Create a Tevi item for this player"""
        data = item_table[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> TeviItem:
        data = event_item_table[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        """
        Define regions and locations.
        This also defines access rules for the regions and locations.
        """
        region_def = RegionDef(self.multiworld, self.player, self.options)
        region_def.set_regions()
        region_def.connect_regions()
        self.total_locations = region_def.set_locations(self.location_name_to_id)
        region_def.set_events()
        self.transitionShuffle = region_def.transitions
        

    def create_items(self) -> None:
        item_pool: List[TeviItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        upgradeable = GetAllUpgradeables()
        #total_locations += 2
        for name, data in item_table.items():
            data.quantity = data.default_quantity
            
            #Havent found a better place
            if not self.options.randomize_knife.value and name == "Dagger":
                data.quantity -=1
                total_locations -=1
            if name == "Astral Gear":
                data.quantity = max(self.options.gear_count.value,self.options.goal_count)
            if not self.options.randomize_orb.value and name == "Orbitars":
                data.quantity -=1
                total_locations -=1
            # Celia and Sable are added to the player start inventory
            #if self.options.celia_sable.value and (name == "I20" or name =="I19"):
                #data.quantity -=1
                #total_locations -=1
            if not self.options.randomize_item_upgrade.value and ApNamesToTevi[name] in upgradeable:
                data.quantity -=2
                total_locations -=2
            if self.options.chaos_mode.value and data.classification != ItemClassification.progression  \
                                             and data.classification != ItemClassification.progression_skip_balancing:
                data.quantity = 0 
            
            item_pool += [self.create_item(name) for _ in range(0, data.quantity)]

        
        while len(item_pool) < total_locations:
            if self.options.chaos_mode.value:
                item_pool.append(self.create_item(self.get_chaos_item_name()))
            else:
                item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += item_pool

    def fill_slot_data(self) -> dict:
        data = self.multiworld.get_filled_locations(self.player)
        locationData = []
        transitionData = []
        for location in data:
            if location.item.name in ApNamesToTevi:
                item = ApNamesToTevi[location.item.name]
            else:
                item = location.item.name
            locationData.append ({
                "location":location.name,
                "item":item,
                "player":location.item.player,
                "game":location.item.game,
                "progressive":location.item.advancement})
        for v in self.transitionShuffle:
            transitionData.append({
                "from":v["Name"],
                "to":v["Connections"][0]["Exit"]
                })

        options = self.options.getOptions()
        return {
            "openMorose": self.options.open_morose.value,
            "attackMode": self.options.free_attack_up.value,
            "CeliaSable": self.options.celia_sable.value,
            "GoalCount": self.options.goal_count.value,
            "locationData": locationData,
            "transitionData":transitionData,
            "opstions": options
        }

    def set_rules(self) -> None:
        """
        Set remaining rules (for now this is just the win condition). 
        """
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.can_reach_region("Illusion Palace",self.player)

    def pre_fill(self) -> None:
        if not self.options.randomize_knife.value:
            self.multiworld.get_location("Thanatara Canyon - Dagger",self.player).place_locked_item(self.create_item("Dagger"))
        if not self.options.randomize_orb.value:
            self.multiworld.get_location("Thanatara Canyon - Orbitars",self.player).place_locked_item(self.create_item("Orbitars"))
        if not self.options.randomize_item_upgrade.value:
            for item in GetAllUpgradeables():
                self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #1",self.player).place_locked_item(self.create_item(TeviToApNames[item]))
                self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #2",self.player).place_locked_item(self.create_item(TeviToApNames[item]))


    def get_chaos_item_name(self) -> str:
        fillers = get_potential_new_item()
        weights = [data.weight for data in fillers.values()]
        choice = self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        #this needs to be change / Multiple Tevi Games will run into an itempool overflow
        item_table[choice].quantity +=1
        return choice
    
    def get_filler_item_name(self) -> str:
        fillers = get_potential_new_filler_item()
        weights = [data.weight for data in fillers.values()]
        choice = self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        #this needs to be change / Multiple Tevi Games will run into an itempool overflow
        item_table[choice].quantity +=1
        return choice

