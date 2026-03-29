"""
This module serves as an entrypoint into the Tevi AP world.
"""

# This AP world uses Rabi-Ribi Ap world as a base, so check out that game as well

import json,pkgutil

from typing import ClassVar, Dict, Set,List,Union,Any

from BaseClasses import ItemClassification,LocationProgressType
from worlds.AutoWorld import World, WebWorld
from .items import TeviItem, event_item_table, get_traps,get_fillers,get_potential_new_item,get_item_groups,get_items_by_category,all_item_table,teleporter_table,item_table,StartIDTeleporter,StartIDTrap,TeviToApNames,ApNamesToTevi
from .Regions import RegionDef, get_all_possible_locations,get_location_group_names
from .Options import TeviOptions
from .Web import TeviWeb
from .Utility import GetAllUpgradeables
from settings import Group,FilePath
from . import ut_stuff

class TeviSettings(Group):
    class UTPoptrackerPath(FilePath):
        """Path to the user's Tevi Poptracker Pack."""
        description = "Tevi Poptracker Pack zip file"
        required = False    
    ut_poptracker_path: Union[UTPoptrackerPath, str] = UTPoptrackerPath()

class TeviWorld(World):
    """
    Description of TEVI
    """
    game: str = "Tevi"
    options_dataclass = TeviOptions
    options: TeviOptions
    settings: ClassVar[TeviSettings]
    topology_present: bool = False
    web: WebWorld = TeviWeb()
    prefilled_items:List[TeviItem] = list()
    item_name_groups: Dict[str, Set[str]] = {}
    location_name_groups: Dict[str, Set[str]] = {}
    item_name_to_id: Dict[str, int] = {name: data.code for name, data in (all_item_table).items()} 
    location_name_to_id: Dict[str, int] = get_all_possible_locations()
    removingPotions = [0,0,0,0,0]

    item_name_groups = get_item_groups()
    location_name_groups = get_location_group_names()
    ut_player:int = -1

    item_quantities: dict[str, int]
            
    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.total_locations = 0
        self.region_def = None
        self.tracker_world["map_page_setting_key"] = r"Slot:{player}:currentMap"
        self.item_quantities = {item: 0 for item, item_data in
                                (all_item_table).items()}


    def generate_early(self) -> None:
        """Set world specific generation properties"""
        #Set up the number of find able Gears
        self.item_quantities["Astral Gear"] = self.options.gear_count.value
        # Increase gear count to match goal count
        if self.options.gear_count.value < self.options.goal_count.value:
            self.options.gear_count.value = self.options.goal_count.value

        if (hasattr(self.multiworld, "re_gen_passthrough") and "Tevi" in getattr(self.multiworld, "re_gen_passthrough")):
            self.options.traverse_Mode.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["traverse_mode"]
            self.options.goal_type.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["goal_type"]
            self.options.cKick.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["cKick"]
            self.options.hiddenP.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["hiddenP"]
            self.options.earlydream.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["earlydream"]
            self.options.barrierSkip.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["barrierSkip"]
            self.options.adcKick.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["adcKick"]
            self.options.superBosses.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["superBosses"]
            self.options.open_morose.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["open_morose"]
            self.options.randomize_item_upgrade.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["randomize_item_upgrade"]



    def create_item(self, name: str) -> TeviItem:
        """Create a Tevi item for this player"""
        data = (all_item_table)[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_teleporter(self,name:str) -> TeviItem:
        data = teleporter_table[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> TeviItem:
        data = event_item_table[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        """
        Define regions and locations.
        This also defines access rules for the regions and locations.
        """
        self.region_def = RegionDef(self.multiworld, self.player, self.options)
        self.region_def.set_regions()
        self.total_locations = self.region_def.set_locations(self.location_name_to_id)
        self.region_def.set_events()
        
    def connect_entrances(self) -> None:
        self.region_def.connect_regions()
        
    def create_items(self) -> None:
        item_pool: List[TeviItem] = list()

        if self.options.traverse_Mode.value ==2:
            for name, data in teleporter_table.items():
                item_pool += [self.create_teleporter(name) for _ in range(0, data.default_quantity)]

        for name, data in item_table.items():
            if data.classification == ItemClassification.progression  \
                                      or data.classification == ItemClassification.progression_skip_balancing:
                self.item_quantities[name] = data.default_quantity

        total_locations = self.itempool_options()

        for name, data in item_table.items():
            item_pool += [self.create_item(name) for _ in range(0, self.item_quantities[name])]
            
        total_items_left = total_locations-len(item_pool)
        traps_amount = int(self.options.traps_percent.value * total_items_left / 100)
        item_list = self.get_traps(traps_amount,self.options.excludeTraps.value)
        item_pool += [self.create_item(name) for name in item_list]

        if self.options.chaos_mode.value:
            while len(item_pool) < total_locations:
                item_pool.append(self.create_item(self.get_chaos_item_name()))
        else:

            #all useful and filler items
            item_list = self.get_filler_items(total_items_left-traps_amount)
            item_pool += [self.create_item(name) for name in item_list]
        self.multiworld.itempool += item_pool

    def itempool_options(self) -> int:
        """
        Removes all item that are not required
        """
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        upgradeable = GetAllUpgradeables()



        if self.options.randomize_money.value == 0:
            self.item_quantities["500 Zennie Pack"] = 0

        if self.options.randomize_magitite.value == 0:
            self.item_quantities["Magitite Shard"] = 0
        else:
            self.item_quantities["Magitite Shard"] = self.options.magitite_amount.value


        if self.options.randomize_mananite.value == 0:
            self.item_quantities["Mananite Shard"] = 0
        else:
            self.item_quantities["Mananite Shard"] = self.options.mananite_amount.value

        start_items = self.options.start_inventory.value

        if not self.options.randomize_knife.value:
            if self.item_quantities["Dagger"] > 0:
                self.item_quantities["Dagger"] -= 1
            total_locations -=1

        self.item_quantities["Astral Gear"] = max(self.options.gear_count.value, self.options.goal_count)

        if not self.options.randomize_orb.value:
            if self.item_quantities["Orbitars"] > 0:
                self.item_quantities["Orbitars"] -= 1
            total_locations -=1

        if not self.options.randomize_item_upgrade.value:
            for item in upgradeable:
                amount = 2
                self.item_quantities[TeviToApNames[item]] = amount
                total_locations -= amount

        for item,amount in start_items.items():
            self.item_quantities[item] = max(0,item_table[item].default_quantity-amount)

        return total_locations

    def fill_slot_data(self) -> dict:
        file = pkgutil.get_data(__name__, 'archipelago.json').decode()
        file = json.loads(file)
        backup_version = file["world_version"]
        transitionData = []
        options = self.options.getOptions()
        if self.options.traverse_Mode.value == 2:
            for connection in self.region_def.randomizedEntrances:
                transitionData.append({
                    "from":connection[0],
                    "to":connection[0]
                    })
        else:
            for connection in self.region_def.randomizedEntrances:
                transitionData.append({
                    "from":connection[0],
                    "to":connection[1]
                    })
        return {
            "version":self.world_version.as_simple_string(),
            "backup_version":backup_version,
            "StartIDTeleporter":StartIDTeleporter,
            "StartIDTrap":StartIDTrap,
            "transitionData":transitionData,
            "options": options
        }

    def set_rules(self) -> None:
        """
        Set remaining rules (for now this is just the win condition). 
        """
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.can_reach_region("Illusion Palace",self.player)

    def pre_fill(self) -> None:
        start_items = self.options.start_inventory.value

        if not self.options.randomize_knife.value and not ("Dagger" in start_items and start_items["Dagger"] >= 3):
            self.multiworld.get_location("Thanatara Canyon - Dagger",self.player).place_locked_item(self.create_item("Dagger"))
            self.prefilled_items.append(self.create_item("Dagger"))
        if not self.options.randomize_orb.value and not ("Orbitars" in start_items and start_items["Orbitars"] >= 3):
            self.multiworld.get_location("Thanatara Canyon - Orbitars",self.player).place_locked_item(self.create_item("Orbitars"))
            self.prefilled_items.append(self.create_item("Orbitars"))
        if not self.options.randomize_item_upgrade.value:
            for item in GetAllUpgradeables():
                if not (TeviToApNames[item] in start_items and start_items[TeviToApNames[item]] >= 2):
                    self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #1",self.player).place_locked_item(self.create_item(TeviToApNames[item]))
                    self.prefilled_items.append(self.create_item(TeviToApNames[item]))
                if not (TeviToApNames[item] in start_items and start_items[TeviToApNames[item]] >= 1):
                    self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #2",self.player).place_locked_item(self.create_item(TeviToApNames[item]))
                    self.prefilled_items.append(self.create_item(TeviToApNames[item]))
                self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #1",self.player).progress_type = LocationProgressType.EXCLUDED
                self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #2",self.player).progress_type = LocationProgressType.EXCLUDED

    def get_pre_fill_items(self) -> List[TeviItem]:
        """"Returns all item placed in pre_fill"""
        return self.prefilled_items

    def get_chaos_item_name(self) -> str:
        fillers = get_potential_new_item(self)
        weights = [data.weight for data in fillers.values()]
        choice = self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        self.item_quantities[choice] += 1
        return choice

    
    def get_traps(self,amount = 1,ignoreList:set = None) -> List[str]:
        if amount <= 0:
            return []
        if ignoreList == None:
            ignoreList = []
        traps = get_traps(self,ignoreList)
        weights = [data.weight for data in traps.values()]
        choice_list = self.random.choices([filler for filler in traps.keys()], weights, k=amount)
        self.random.choice
        for choice in choice_list:
            self.item_quantities[choice] += 1
        return choice_list
        
    def get_filler_items(self,amount = 1) -> List[str]:
        if amount <= 0:
            return []
        filler = get_fillers(self)
        item_list = [filler for filler in filler.keys()]
        weights = [data.weight for data in filler.values()]
        result = []


        
        while(amount > 0 and len(item_list) >0):
            amount -=1
            choice = self.random.choices(item_list, weights, k=1)[0]
            self.item_quantities[choice] +=1
            result.append(choice)
            if self.item_quantities[choice] >= item_table[choice].default_quantity:
                idx = item_list.index(choice)
                item_list.pop(idx)
                weights.pop(idx)

        if len(item_list) < amount:
            leftover = amount -len(item_list)
            food = get_items_by_category("Consumeable")
            food_list = []
            food_weights = []
            for k,v in food.items():
                if v.classification == ItemClassification.progression:
                    continue
                food_list.append(k)
                food_weights.append(v.weight)
            result += self.random.choices(food_list, food_weights, k=leftover)
        return result
        
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER
        return slot_data   
    
    tracker_world = {
    "map_page_maps": ["maps/maps.jsonc"],
    "map_page_locations": [
        "locations/locations.jsonc"
],
    "map_page_setting_key": f"Slot:-1:currentMap",
    "map_page_index": ut_stuff.map_page_index,
    "external_pack_key": "ut_poptracker_path",
    "poptracker_name_mapping": ut_stuff.poptracker_data
}


