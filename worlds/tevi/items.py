"""This module represents item definitions for Tevi"""
from typing import Dict, Optional, TYPE_CHECKING
import json,pkgutil,os

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import TeviWorld


class TeviItem(Item):
    """Tevi Item Definition"""
    game: str = "Tevi"

    @staticmethod
    def is_progression_item(name: str, options):
        """
        not used
        Defines if an item is considered a progression item.

        This will likely be updated as future logic changes happen.
        For now im porting the logic from the existing rando as is.
        """
        progression_items = {
            "Knife",
            "Double Juump",
            "Wall Jump",
            "Air Dash",
            "Gear",
            "Jet Pack",
            "Water Movement",
            "Air Slide",
            "High Jump",
            "Vortex Glove",
            "Cross Bomb",
            "Area Bomb",
            "Nap Pillow"
        }
        return name in progression_items


class TeviItemData():
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    default_quantity: int = 1
    max_quantity: int = 1
    weight: int = 1
    def __init__(self,category: str,
                code: Optional[int] = None,
                classification: ItemClassification = ItemClassification.filler,
                default_quantity: int = 1,
                max_quantity: int = 1,
                weight: int = 100):
        self.category= category
        self.code: Optional[int] = code
        self.classification = classification
        self.default_quantity: int = default_quantity
        self.max_quantity: int = max_quantity
        self.weight: int = weight


def get_items_by_category(category: str) -> Dict[str, TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict

def get_traps(world: "TeviWorld",ignore:set) -> Dict[str,TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in trap_table.items():
        if name not in ignore and world.item_quantities[name] < data.max_quantity:
            item_dict.setdefault(name, data)
    return item_dict

def get_fillers(world: "TeviWorld") -> Dict[str,TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if  world.item_quantities[name] < data.default_quantity:
            item_dict.setdefault(name, data)
    return item_dict

def get_potential_new_item(world: "TeviWorld") -> Dict[str, TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if world.item_quantities[name] < data.max_quantity and name != "Astral Gear":
            item_dict.setdefault(name, data)
    return item_dict


def get_potential_new_filler_item(world: "TeviWorld") -> Dict[str, TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if world.item_quantities[name] < data.max_quantity and data.classification == ItemClassification.filler:
            item_dict.setdefault(name, data)
    return item_dict

def get_item_groups():
    item_name_groups = {}
    item_name_groups["Progression"] = []
    for item,data in item_table.items():
        if data.category in item_name_groups:
            item_name_groups[data.category].add(item)
        else:
            item_name_groups[data.category] = {item}
        if data.classification == ItemClassification.progression:
            item_name_groups["Progression"] += {item}

    for item,data in teleporter_table.items():
        if data.category in item_name_groups:
            item_name_groups[data.category].add(item)
            item_name_groups["Progression"] += {item}
        else:
            item_name_groups[data.category] = {item}
    return item_name_groups


item_table: Dict[str,TeviItemData] ={
}

StartIDTeleporter = 1000
teleporter_table: Dict[str,TeviItemData] = {
}

event_item_table: Dict[str, TeviItemData] = {
}

StartIDTrap = 2000
trap_table: Dict[str,TeviItemData] = {
}

TeviToApNames = {}
ApNamesToTevi = {}

def loadItems():
    items = json.loads(pkgutil.get_data(__name__, os.path.join('resources', 'Items.json')).decode())
    for item in items:
        itemData = TeviItemData(item["Group"],item["ID"],ItemClassification.filler,item["Default_Quantity"],item["Maximum_Quantity"],item["Weight"])
        if item["Classification"] == "progression":
            itemData.classification = ItemClassification.progression
        elif item["Classification"] == "trap":
            itemData.classification = ItemClassification.trap
        elif item["Classification"] == "useful":
            itemData.classification = ItemClassification.useful

        if itemData.classification == ItemClassification.trap:
            trap_table[item["DisplayName"]] = itemData
        else:
            if "Teleporter" in item["DisplayName"]:
                teleporter_table[item["DisplayName"]] = itemData
            else:
                item_table[item["DisplayName"]] = itemData
        TeviToApNames[item["Name"]] = item["DisplayName"]
        ApNamesToTevi[item["DisplayName"]] = item["Name"]
    
loadItems()

all_item_table = item_table|teleporter_table|trap_table
