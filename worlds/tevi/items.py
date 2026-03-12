"""This module represents item definitions for Tevi"""
from typing import Dict, Optional, TYPE_CHECKING

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
    # Goal Requiment
    "Astral Gear":                                             TeviItemData("Goal",   1, ItemClassification.progression_skip_balancing,       25, 255),

    #Stat Buffs
    "Kiwi Bunny Potion":                                       TeviItemData("Stat",   2, ItemClassification.filler,                           35, 255,80),
    "Blueberry Bunny Potion":                                  TeviItemData("Stat",   3, ItemClassification.filler,                           35, 255,80),
    "Lemon Bunny Potion":                                      TeviItemData("Stat",   4, ItemClassification.filler,                           35, 255,80),
    "Cherry Bunny Potion":                                     TeviItemData("Stat",   5, ItemClassification.filler,                           35, 255,80),
    "Grape Bunny Potion":                                      TeviItemData("Stat",   6, ItemClassification.filler,                           35, 255,80),
    "Bag Expander":                                            TeviItemData("Stat",   7, ItemClassification.filler,                           5, 255,150),
    "Rainbow Bunny Potion":                                    TeviItemData("Stat",   8, ItemClassification.filler,                           15, 255,60),

    #custom items
    "500 Zennie Pack":                                         TeviItemData("Custom",  14,  ItemClassification.filler,                            1091,591,10),
    "Magitite Shard":                                          TeviItemData("Upgrade",  15,  ItemClassification.progression,                             35,70),
    "Mananite Shard":                                          TeviItemData("Upgrade",  16,  ItemClassification.progression,                             90,96),

    #Items
    "Celia":                                                   TeviItemData("Weapon",   19, ItemClassification.progression),
    "Sable":                                                   TeviItemData("Weapon",   20, ItemClassification.progression),
    "Dagger":                                                  TeviItemData("Weapon",   22, ItemClassification.progression,                      3, 255),
    "Orbitars":                                                TeviItemData("Weapon",   23, ItemClassification.progression,                      3, 255),
    "Cross Bomb":                                              TeviItemData("Weapon",   24, ItemClassification.progression,                      3, 255),
    "Cluster Bomb":                                            TeviItemData("Weapon",   25, ItemClassification.progression,                      3, 255),
    "Bomb Fuel":                                               TeviItemData("Item",   26, ItemClassification.progression,                      3, 255),
    "Rabi Boots":                                              TeviItemData("Movement",   27, ItemClassification.progression,                      1, 255),
    "Running Boots":                                           TeviItemData("Movement",   28, ItemClassification.progression,                      3, 255),
    "Slick Boots":                                             TeviItemData("Movement",   29, ItemClassification.progression,                      1, 255),
    "Parkour Boots":                                           TeviItemData("Movement",   30, ItemClassification.progression,                      3, 255),
    "Double Rabi Boots":                                       TeviItemData("Movement",   31, ItemClassification.progression,                      1, 1),
    "Jetpack":                                                 TeviItemData("Movement",   32, ItemClassification.progression,                      3, 255),
    "Hydrodynamo":                                             TeviItemData("Movement",   33, ItemClassification.progression,                      1, 255),
    "PK Recon Badge":                                          TeviItemData("Item",   34, ItemClassification.useful,                           1, 255),
    "Decay Mask":                                              TeviItemData("Item",   35, ItemClassification.progression,                      3, 255),
    "Red Module Type-B":                                       TeviItemData("Item",   36, ItemClassification.progression,                      1, 1),
    "Red Module Type-C":                                       TeviItemData("Item",   37, ItemClassification.progression,                      1, 1),
    "Blue Module Type-B":                                      TeviItemData("Item",   38, ItemClassification.progression,                      1, 1),
    "Blue Module Type-C":                                      TeviItemData("Item",   39, ItemClassification.progression,                      1, 1),
    "Decay Antidote":                                          TeviItemData("Item",   40, ItemClassification.progression,                           1, 255),
    "Combustible":                                             TeviItemData("Item",   41, ItemClassification.progression,                      3, 255),
    "Slipstream Boots":                                        TeviItemData("Movement",   42, ItemClassification.progression,                      3, 255),
    "Tartarus VIP Pass":                                      TeviItemData("Item",   43, ItemClassification.progression),
    "Valhalla VIP Pass":                                       TeviItemData("Item",   44, ItemClassification.progression),
    "Royal Emblem":                                            TeviItemData("Item",   45, ItemClassification.useful),
    "Grip Sole Boots":                                         TeviItemData("Item",   46, ItemClassification.useful),
    "Explorer's Compass":                                      TeviItemData("Item",   47, ItemClassification.progression,                      3,   3),
    "Equilibrium Ring":                                        TeviItemData("Item",   48, ItemClassification.progression,                      3,   3),
    "Modular Blueprints":                                      TeviItemData("Item",   49, ItemClassification.progression,                      3, 255),
    "Core Module Type-U":                                      TeviItemData("Item",   50, ItemClassification.useful),
    "Core Module Type-D":                                      TeviItemData("Item",   51, ItemClassification.useful),
    "Deadly Reach":                                            TeviItemData("Item",   52, ItemClassification.progression,                      3, 255),
    "Shining Bangle":                                          TeviItemData("Item",   53, ItemClassification.progression,                      3, 255),
    "Spanner of Wisdom":                                       TeviItemData("Item",   54, ItemClassification.progression,                      3,   3),
    #"Notebook":                                               TeviItemData("Item",   55, ItemClassification.progression),
    "Delicious Secret Notes":                                  TeviItemData("Item",   56, ItemClassification.useful),
    "Rapid Shots Modchip":                                     TeviItemData("Item",   57, ItemClassification.progression,                      3,   4),
    #"Backpack":                                               TeviItemData("Item",   58, ItemClassification.progression),
    "Soul Burst Module":                                       TeviItemData("Item",   59, ItemClassification.progression,                      3, 255),
    "Trinketeer's Fortune":                                    TeviItemData("Item",   60, ItemClassification.progression,                      3, 255),
    "Alterscope":                                              TeviItemData("Item",   61, ItemClassification.useful),
    "Gilded Exultation":                                       TeviItemData("Item",   62, ItemClassification.useful),
    "Vortex Gloves":                                           TeviItemData("Item",   63, ItemClassification.progression,                      3, 255),
    "Airy Powder":                                             TeviItemData("Movement",   64, ItemClassification.progression),
    "Kitty Paw Charm":                                         TeviItemData("Item",   65, ItemClassification.useful),
    "Alembic Crystal":                                         TeviItemData("Item",   66, ItemClassification.progression),

    #Quest Items
    "Crystal Flute":                                           TeviItemData("Item",   99, ItemClassification.progression),
    "Memory Box":                                              TeviItemData("Item",    100, ItemClassification.progression),
    "Frozen Fate":                                             TeviItemData("Item",    102, ItemClassification.progression),
    "Gilded Left Hand":                                        TeviItemData("Item",    106, ItemClassification.progression),
    "Gilded Right Hand":                                       TeviItemData("Item",    107, ItemClassification.progression),
    "Nap Pillow":                                              TeviItemData("Item",    109, ItemClassification.progression),
    "Library Key":                                             TeviItemData("Item",    110, ItemClassification.progression),

    #Badges
    "Palladium":                                               TeviItemData("Badge",    120, ItemClassification.filler),
    "Backstab":                                                TeviItemData("Badge",    121, ItemClassification.filler),
    "C. Count Frenzy: Hotshot":                                TeviItemData("Badge",    122, ItemClassification.filler),
    "Health Plus":                                             TeviItemData("Badge",    123, ItemClassification.useful),
    "Celia Type-B: Prism":                                     TeviItemData("Badge",    124, ItemClassification.filler),
    "Knives Out":                                              TeviItemData("Badge",    125, ItemClassification.filler),
    "Red Haze":                                                TeviItemData("Badge",    126, ItemClassification.filler),
    "Dodge Enhancer: Upper":                                   TeviItemData("Badge",    127, ItemClassification.filler),
    "Dodge Enhancer: Spiral":                                  TeviItemData("Badge",    128, ItemClassification.filler),
    #"Dodge Enhancer: Airdash":                                TeviItemData("Badge",    129, ItemClassification.useful),
    "Dodge Enhancer: Spanner":                                 TeviItemData("Badge",    130, ItemClassification.filler),
    "Dodge Enhancer: Slide":                                   TeviItemData("Badge",    131, ItemClassification.filler),
    "EP Booster: Dodge":                                       TeviItemData("Badge",    132, ItemClassification.filler),
    "Style Combo: Windmill B":                                 TeviItemData("Badge",    133, ItemClassification.filler),
    "MP Surge: Tag Out":                                       TeviItemData("Badge",    134, ItemClassification.filler),
    "MP Surge: Concuss":                                       TeviItemData("Badge",    135, ItemClassification.filler),
    "Celia Type-A: Beguile":                                   TeviItemData("Badge",    136, ItemClassification.filler),
    "Lucky 7: A":                                              TeviItemData("Badge",    137, ItemClassification.filler),
    "MP Quicken: Accelerate":                                  TeviItemData("Badge",    138, ItemClassification.filler),
    "C. Count Frenzy: Acrobatics":                             TeviItemData("Badge",    139, ItemClassification.filler),
    "Upper Slash: Vicious":                                    TeviItemData("Badge",    140, ItemClassification.filler),
    "Titanium Spanner":                                        TeviItemData("Badge",    141, ItemClassification.filler),
    "Aerial Accel":                                            TeviItemData("Badge",    142, ItemClassification.filler),
    "Sable Type-A: Fanged":                                    TeviItemData("Badge",    143, ItemClassification.filler),
    "Invictus":                                                TeviItemData("Badge",    144, ItemClassification.filler),
    "Grub Guru":                                               TeviItemData("Badge",    145, ItemClassification.filler),
    "Intrepid Explorer":                                       TeviItemData("Badge",    146, ItemClassification.filler),
    "Heavy Metal":                                             TeviItemData("Badge",    147, ItemClassification.useful),
    "MP Surge: Battle Start":                                  TeviItemData("Badge",    148, ItemClassification.filler),
    "Aplomb":                                                  TeviItemData("Badge",    149, ItemClassification.filler),
    "MP Saver: Fireworks":                                     TeviItemData("Badge",    150, ItemClassification.useful),
    "C. Count Frenzy: Uprise":                                 TeviItemData("Badge",    151, ItemClassification.filler),
    "MP Surge: Dodge":                                         TeviItemData("Badge",    152, ItemClassification.filler),
    "MP Quicken: Step Up":                                     TeviItemData("Badge",    153, ItemClassification.filler),
    "Celia Type-A: Stunning":                                  TeviItemData("Badge",    154, ItemClassification.filler),
    "Dodge Recovery":                                          TeviItemData("Badge",    155, ItemClassification.filler),
    "Combo Crasher":                                           TeviItemData("Badge",    156, ItemClassification.filler),
    "Battlecry":                                               TeviItemData("Badge",    157, ItemClassification.filler),
    "Air Combo: Focus":                                        TeviItemData("Badge",    158, ItemClassification.filler),
    "Acrobat":                                                 TeviItemData("Badge",    159, ItemClassification.filler),
    "Aerial Kinetics":                                         TeviItemData("Badge",    160, ItemClassification.filler),
    "Mana Armor":                                              TeviItemData("Badge",    161, ItemClassification.useful),
    "Deft A":                                                  TeviItemData("Badge",    162, ItemClassification.useful),
    "Deft B":                                                  TeviItemData("Badge",    163, ItemClassification.useful),
    "Quickstab: Sunder":                                       TeviItemData("Badge",    164, ItemClassification.filler),
    "Combo Time Extend A ":                                    TeviItemData("Badge",    165, ItemClassification.filler),
    "Combo Time Extend B":                                     TeviItemData("Badge",    166, ItemClassification.filler),
    "Combo Time Extend C":                                     TeviItemData("Badge",    167, ItemClassification.filler),
    "Whipcrack":                                               TeviItemData("Badge",    168, ItemClassification.filler),
    "Combo Momentum: Fever":                                   TeviItemData("Badge",    169, ItemClassification.filler),
    "Two-pronged Shot":                                        TeviItemData("Badge",    170, ItemClassification.useful),
    "Full Stop A":                                             TeviItemData("Badge",    171, ItemClassification.filler),
    "Under Score":                                             TeviItemData("Badge",    172, ItemClassification.filler),
    "Upper Slash: Augment":                                    TeviItemData("Badge",    173, ItemClassification.filler),
    "Dodge: Panic Switch":                                     TeviItemData("Badge",    174, ItemClassification.filler),
    "C. Count Frenzy: Preemptive":                             TeviItemData("Badge",    175, ItemClassification.filler),
    "Health Surge":                                            TeviItemData("Badge",    176, ItemClassification.useful),
    "Glass Knife":                                             TeviItemData("Badge",    177, ItemClassification.useful),
    "Buns of Steel":                                           TeviItemData("Badge",    178, ItemClassification.filler),
    "Combo Momentum: Dodge":                                   TeviItemData("Badge",    179, ItemClassification.filler),
    "Break Extend":                                            TeviItemData("Badge",    180, ItemClassification.filler),
    "Nasty Break-up":                                          TeviItemData("Badge",    181, ItemClassification.useful),
    "MP Surge: Break":                                         TeviItemData("Badge",    182, ItemClassification.filler),
    "Combo Momentum: Saver":                                   TeviItemData("Badge",    183, ItemClassification.filler),
    "Perseverance A":                                          TeviItemData("Badge",    184, ItemClassification.filler),
    "EP Booster: Quintuple":                                   TeviItemData("Badge",    185, ItemClassification.filler),
    "Quick Break":                                             TeviItemData("Badge",    186, ItemClassification.useful),
    "Power Drop":                                              TeviItemData("Badge",    187, ItemClassification.useful),
    "Pogo Drop":                                               TeviItemData("Badge",    188, ItemClassification.useful),
    "Double Drop":                                             TeviItemData("Badge",    189, ItemClassification.useful),
    "Crystalline Scarlet":                                     TeviItemData("Badge",    190, ItemClassification.filler),
    "Crystalline Cyan":                                        TeviItemData("Badge",    191, ItemClassification.filler),
    "Terrestrial Agility":                                     TeviItemData("Badge",    192, ItemClassification.useful),
    "Aerial Agility":                                          TeviItemData("Badge",    193, ItemClassification.filler),
    "Galvanise":                                               TeviItemData("Badge",    194, ItemClassification.useful),
    "Orbital Efficiency A":                                    TeviItemData("Badge",    195, ItemClassification.filler),
    "Orbital Efficiency B":                                    TeviItemData("Badge",    196, ItemClassification.filler),
    "Quick Bomber":                                            TeviItemData("Badge",    197, ItemClassification.filler),
    "Quickstab: Lightning":                                    TeviItemData("Badge",    198, ItemClassification.filler),
    "Quickstab: Flurry":                                       TeviItemData("Badge",    199, ItemClassification.filler),
    #"Bombastic":                                              TeviItemData("Badge",    200, ItemClassification.useful),
    "Spiral Slash: Flurry":                                    TeviItemData("Badge",    201, ItemClassification.filler),
    "Spiral Slash: Cyclone":                                   TeviItemData("Badge",    202, ItemClassification.filler),
    "Bomb Pitcher":                                            TeviItemData("Badge",    203, ItemClassification.filler),
    "Style Combo: Flash A":                                    TeviItemData("Badge",    204, ItemClassification.filler),
    "High Defence Bomber":                                     TeviItemData("Badge",    205, ItemClassification.filler),
    "Low Defence Bomber":                                      TeviItemData("Badge",    206, ItemClassification.filler),
    "Style Combo: Triple Flash S":                             TeviItemData("Badge",    207, ItemClassification.filler),
    "Style Combo: Tornado A":                                  TeviItemData("Badge",    208, ItemClassification.filler),
    "Short Fuse":                                              TeviItemData("Badge",    209, ItemClassification.filler),
    "Style Combo: Lock On A":                                  TeviItemData("Badge",    210, ItemClassification.filler),
    "Style Combo: Bunny Kick S":                               TeviItemData("Badge",    211, ItemClassification.filler),
    "Style Combo: Trickshot":                                  TeviItemData("Badge",    212, ItemClassification.filler),
    "C. Rank Frenzy: Focus A":                                 TeviItemData("Badge",    213, ItemClassification.filler),
    "C. Rank Frenzy: Focus S":                                 TeviItemData("Badge",    214, ItemClassification.filler),
    "C. Rank Frenzy: Focus MAX":                               TeviItemData("Badge",    215, ItemClassification.filler),
    "Tornado Spin: Pressure":                                  TeviItemData("Badge",    216, ItemClassification.filler),
    "Unlucky 7":                                               TeviItemData("Badge",    217, ItemClassification.filler),
    "Core Expansion: Vitalize":                                TeviItemData("Badge",    218, ItemClassification.filler),
    "Cursed 6":                                                TeviItemData("Badge",    219, ItemClassification.filler),
    "Core Expansion: Charge":                                  TeviItemData("Badge",    220, ItemClassification.filler),
    "MP Quicken: Steady":                                      TeviItemData("Badge",    221, ItemClassification.filler),
    "MP Quicken: Style":                                       TeviItemData("Badge",    222, ItemClassification.filler),
    "MP Quicken: Combo":                                       TeviItemData("Badge",    223, ItemClassification.filler),
    "MP Surge: Recovery":                                      TeviItemData("Badge",    224, ItemClassification.filler),
    "Coffee Break":                                            TeviItemData("Badge",    225, ItemClassification.useful),
    "Sable Type-B: Malediction":                               TeviItemData("Badge",    226, ItemClassification.filler),
    "Core Expansion: Dazzle":                                  TeviItemData("Badge",    227, ItemClassification.filler),
    "Dodge: Optimize":                                         TeviItemData("Badge",    228, ItemClassification.filler),
    "C. Rank Frenzy: Attack":                                  TeviItemData("Badge",    229, ItemClassification.filler),
    "C. Rank Frenzy: Defend":                                  TeviItemData("Badge",    230, ItemClassification.filler),
    "Debuff Counter":                                          TeviItemData("Badge",    231, ItemClassification.filler),
    "Crystal Boon":                                            TeviItemData("Badge",    232, ItemClassification.filler),
    "Triple Threat":                                           TeviItemData("Badge",    233, ItemClassification.filler),
    "Dogfight":                                                TeviItemData("Badge",    234, ItemClassification.filler),
    "Magic Cannon":                                            TeviItemData("Badge",    235, ItemClassification.filler),
    "Dextrous":                                                TeviItemData("Badge",    236, ItemClassification.useful),
    "Hero Call":                                               TeviItemData("Badge",    237, ItemClassification.filler),
    "Dodge: Feeling Lucky":                                    TeviItemData("Badge",    238, ItemClassification.filler),
    "Buff Rush":                                               TeviItemData("Badge",    239, ItemClassification.filler),
    "Dodge: Discharge":                                        TeviItemData("Badge",    240, ItemClassification.filler),
    "Core Expansion: Recovery":                                TeviItemData("Badge",    241, ItemClassification.filler),
    "Punisher":                                                TeviItemData("Badge",    242, ItemClassification.filler),
    "Synchronized Support II":                                 TeviItemData("Badge",    243, ItemClassification.filler),
    "Celia Type-B: Halo":                                      TeviItemData("Badge",    244, ItemClassification.filler),
    "Bounce Bonus":                                            TeviItemData("Badge",    245, ItemClassification.filler),
    "MP Reset A":                                              TeviItemData("Badge",    246, ItemClassification.filler),
    "MP Reset B":                                              TeviItemData("Badge",    247, ItemClassification.filler),
    "EP Booster: Perfectionist":                               TeviItemData("Badge",    248, ItemClassification.filler),
    "Core Expansion: Extend":                                  TeviItemData("Badge",    249, ItemClassification.filler),
    "Backflip Flurry":                                         TeviItemData("Badge",    250, ItemClassification.filler),
    "Shock Armor":                                             TeviItemData("Badge",    251, ItemClassification.filler),
    "Head Over Heels":                                         TeviItemData("Badge",    252, ItemClassification.filler),
    "Dual Combo: Flow":                                        TeviItemData("Badge",    253, ItemClassification.filler),
    "Dual Combo: Rush":                                        TeviItemData("Badge",    254, ItemClassification.filler),
    "Perseverance D":                                          TeviItemData("Badge",    255, ItemClassification.filler),
    "Perseverance B":                                          TeviItemData("Badge",    256, ItemClassification.filler),
    "EP Booster: Variety":                                     TeviItemData("Badge",    257, ItemClassification.filler),
    "MP Surge: Brawl":                                         TeviItemData("Badge",    258, ItemClassification.filler),
    "Perseverance C":                                          TeviItemData("Badge",    259, ItemClassification.filler),
    "Rapid Shots Enhance":                                     TeviItemData("Badge",    260, ItemClassification.filler),
    "EP Booster: HP":                                          TeviItemData("Badge",    261, ItemClassification.filler),
    "Sable Type-A: Ensnare":                                   TeviItemData("Badge",    262, ItemClassification.filler),
    "Celia Type-A: Meteoric":                                  TeviItemData("Badge",    263, ItemClassification.filler),
    "Sable Type-B: Backlash":                                  TeviItemData("Badge",    264, ItemClassification.filler),
    "Sable Type-C: Ignite":                                    TeviItemData("Badge",    265, ItemClassification.filler),
    "MP Quicken: Bloodlust":                                   TeviItemData("Badge",    266, ItemClassification.useful),
    "MP Quicken: Sacrifice":                                   TeviItemData("Badge",    267, ItemClassification.filler),
    "MP Saver: Rhythm":                                        TeviItemData("Badge",    268, ItemClassification.filler),
    "Swift Shots":                                             TeviItemData("Badge",    269, ItemClassification.filler),
    "Dodge: Golden Luck":                                      TeviItemData("Badge",    270, ItemClassification.filler),
    "Sable Type-A: Voracious":                                 TeviItemData("Badge",    271, ItemClassification.filler),
    "Celia Type-C: Barrage":                                   TeviItemData("Badge",    272, ItemClassification.filler),
    "Celia Type-C: Panoptic":                                  TeviItemData("Badge",    273, ItemClassification.filler),
    "Sable Type-C: Fervid":                                    TeviItemData("Badge",    274, ItemClassification.filler),
    "Blood Magic":                                             TeviItemData("Badge",    275, ItemClassification.filler),
    "The Untamed":                                             TeviItemData("Badge",    276, ItemClassification.filler),
    "MP Quicken: Melee":                                       TeviItemData("Badge",    277, ItemClassification.filler),
    "Synchronized Support I":                                  TeviItemData("Badge",    278, ItemClassification.filler),
    "Ranged Roulette":                                         TeviItemData("Badge",    279, ItemClassification.filler),
    "Lucky 7: B":                                              TeviItemData("Badge",    280, ItemClassification.filler),
    "Attenu-8":                                                TeviItemData("Badge",    281, ItemClassification.filler),
    "Supercluster Bomb":                                       TeviItemData("Badge",    282, ItemClassification.filler),
    "Crouching Bunny":                                         TeviItemData("Badge",    283, ItemClassification.filler),
    "Tornado Spin: Flurry":                                    TeviItemData("Badge",    284, ItemClassification.filler),
    "Tornado Spin: Grav Reversal":                             TeviItemData("Badge",    285, ItemClassification.filler),
    "EP Booster: Melee Menace":                                TeviItemData("Badge",    286, ItemClassification.filler),
    "Dodge: Headstrong":                                       TeviItemData("Badge",    287, ItemClassification.filler),
    "Aerial Assist":                                           TeviItemData("Badge",    288, ItemClassification.filler),
    "Lucky 7: C":                                              TeviItemData("Badge",    289, ItemClassification.filler),
    "Ballasting Off":                                          TeviItemData("Badge",    290, ItemClassification.filler),
    "Life Steal":                                              TeviItemData("Badge",    291, ItemClassification.filler),
    "MP Surge: Explosives":                                    TeviItemData("Badge",    292, ItemClassification.filler),
    "EP Booster: MP":                                          TeviItemData("Badge",    293, ItemClassification.filler),
    "Mana Flare":                                              TeviItemData("Badge",    294, ItemClassification.filler),
    "Double Airstrike":                                        TeviItemData("Badge",    295, ItemClassification.filler),
    "Spanner Bash: Wrecker":                                   TeviItemData("Badge",    296, ItemClassification.filler),
    "Supernova":                                               TeviItemData("Badge",    297, ItemClassification.useful),
    "Daisy Chain":                                             TeviItemData("Badge",    298, ItemClassification.filler),
    "Blood Armor":                                             TeviItemData("Badge",    299, ItemClassification.useful),
    "Even Keel":                                               TeviItemData("Badge",    300, ItemClassification.filler),
    "Enthusiastic Excavator":                                  TeviItemData("Badge",    301, ItemClassification.filler),
    "MP Surge: Soul":                                          TeviItemData("Badge",    302, ItemClassification.filler),
    "Auto Heal":                                               TeviItemData("Badge",    303, ItemClassification.filler),
    "Headbutt":                                                TeviItemData("Badge",    304, ItemClassification.filler),
    "Bulletproof Pillar S":                                    TeviItemData("Badge",    305, ItemClassification.filler),
    "Bulletproof Pillar C":                                    TeviItemData("Badge",    306, ItemClassification.filler),
    "MP Quicken: Battlescars":                                 TeviItemData("Badge",    307, ItemClassification.filler),
    "Excuse Me":                                               TeviItemData("Badge",    308, ItemClassification.filler),
    "Slash Quartet":                                           TeviItemData("Badge",    309, ItemClassification.filler),
    "Thick Pillar":                                            TeviItemData("Badge",    310, ItemClassification.filler),
    "Dominator":                                               TeviItemData("Badge",    311, ItemClassification.filler),
    "Drop Kick":                                               TeviItemData("Badge",    312, ItemClassification.filler),
    "Crystal Shrapnel":                                        TeviItemData("Badge",    313, ItemClassification.filler),
    "Slide Basher":                                            TeviItemData("Badge",    314, ItemClassification.filler),
    "Refractor":                                               TeviItemData("Badge",    315, ItemClassification.filler),
    "MP Quicken: Sugar Rush":                                  TeviItemData("Badge",    316, ItemClassification.filler),
    "Terrestrial Momentum":                                    TeviItemData("Badge",    317, ItemClassification.filler),
    "Crystal Mirror":                                          TeviItemData("Badge",    318, ItemClassification.filler),
    "Ground Control":                                          TeviItemData("Badge",    319, ItemClassification.filler),
    "Bone Breaker":                                            TeviItemData("Badge",    320, ItemClassification.filler),
    "Act Tough":                                               TeviItemData("Badge",    321, ItemClassification.filler),
    "Razor Arrow":                                             TeviItemData("Badge",    322, ItemClassification.filler),
    "Style Combo: Afterimage S":                               TeviItemData("Badge",    323, ItemClassification.useful),
    "Sigil Quicken":                                           TeviItemData("Badge",    324, ItemClassification.filler),
    "Blood Boil":                                              TeviItemData("Badge",    325, ItemClassification.filler),
    "Core Expansion: Erase":                                   TeviItemData("Badge",    326, ItemClassification.filler),
    "Crystal Healing":                                         TeviItemData("Badge",    327, ItemClassification.filler),
    "Core Expansion: Transcend":                               TeviItemData("Badge",    328, ItemClassification.filler),
    "Core Expansion: Combo":                                   TeviItemData("Badge",    329, ItemClassification.filler),
    "Supersonic":                                              TeviItemData("Badge",    330, ItemClassification.progression),
    "Crystallize":                                             TeviItemData("Badge",    331, ItemClassification.filler),
    "Hot Buzz":                                                TeviItemData("Badge",    332, ItemClassification.filler),
    "EP Booster: Shopaholic":                                  TeviItemData("Badge",    333, ItemClassification.filler),
    "EP Booster: Synthesizer":                                 TeviItemData("Badge",    334, ItemClassification.filler),
    "Muscle Memory":                                           TeviItemData("Badge",    335, ItemClassification.filler),
    "Slayer":                                                  TeviItemData("Badge",    336, ItemClassification.filler),
    "Shooting Star":                                           TeviItemData("Badge",    337, ItemClassification.filler),
    "Upper Slash: Shatter":                                    TeviItemData("Badge",    338, ItemClassification.filler),
    "Core Expansion: Radiant":                                 TeviItemData("Badge",    339, ItemClassification.filler),
    "Core Expansion: Saver":                                   TeviItemData("Badge",    340, ItemClassification.filler),
    "Overdrive":                                               TeviItemData("Badge",    341, ItemClassification.useful),
    "C. Rank Frenzy: Fierce":                                  TeviItemData("Badge",    342, ItemClassification.filler),
    "Fast Pillar":                                             TeviItemData("Badge",    343, ItemClassification.filler),
    "Spanner Bash: Bounce":                                    TeviItemData("Badge",    344, ItemClassification.filler),
    "Upper Slash: Volley":                                     TeviItemData("Badge",    345, ItemClassification.filler),
    "Electric Wind":                                           TeviItemData("Badge",    346, ItemClassification.filler),
    "Style Combo: Upper A":                                    TeviItemData("Badge",    347, ItemClassification.filler),
    "Style Combo: Power A":                                    TeviItemData("Badge",    348, ItemClassification.filler),
    "Style Combo: Aerial A":                                   TeviItemData("Badge",    349, ItemClassification.filler),
    "Slide Halt":                                              TeviItemData("Badge",    350, ItemClassification.filler),
    "Metamorphose":                                            TeviItemData("Badge",    351, ItemClassification.filler),
    "Style Combo: Backbomb S":                                 TeviItemData("Badge",    352, ItemClassification.useful),
    "C. Rank Frenzy: Starter":                                 TeviItemData("Badge",    353, ItemClassification.filler),
    "Windmill Strike":                                         TeviItemData("Badge",    354, ItemClassification.filler),
    "Orbital Slash":                                           TeviItemData("Badge",    355, ItemClassification.filler),
    "Spring Back":                                             TeviItemData("Badge",    356, ItemClassification.filler),
    "Bombard":                                                 TeviItemData("Badge",    357, ItemClassification.useful),
    "Shell Shock":                                             TeviItemData("Badge",    358, ItemClassification.filler),
    "Biscuit Delivery":                                        TeviItemData("Badge",    359, ItemClassification.filler),
    "Full Stop B":                                             TeviItemData("Badge",    360, ItemClassification.filler),
    "Magic Mixer":                                             TeviItemData("Badge",    361, ItemClassification.filler),
    "Inhale Dessert":                                          TeviItemData("Badge",    362, ItemClassification.filler),
    "Combo Assist":                                            TeviItemData("Badge",    363, ItemClassification.filler),
    "Flash Point":                                             TeviItemData("Badge",    364, ItemClassification.filler),
    "Special Action: Question Mark":                           TeviItemData("Badge",    365, ItemClassification.filler),
    "Special Action: Show Off":                                TeviItemData("Badge",    366, ItemClassification.filler),
    "Special Action: Paparazzo":                               TeviItemData("Badge",    367, ItemClassification.filler),
    "Special Action: Speechless":                              TeviItemData("Badge",    368, ItemClassification.filler),
    "Special Action: Yawn":                                    TeviItemData("Badge",    369, ItemClassification.filler),
    "Special Action: Olive Branch":                            TeviItemData("Badge",    370, ItemClassification.filler),
    "Weak Dominance A":                                        TeviItemData("Badge",    371, ItemClassification.filler),
    "Weak Dominance B":                                        TeviItemData("Badge",    372, ItemClassification.filler),
    "Armor Piercer":                                           TeviItemData("Badge",    373, ItemClassification.filler),
    "Core Expansion: Full Offense":                            TeviItemData("Badge",    374, ItemClassification.filler),
    "Range Break":                                             TeviItemData("Badge",    375, ItemClassification.filler),
    "Mana Platform":                                           TeviItemData("Badge",    376, ItemClassification.useful),
    "Go Ballistic":                                            TeviItemData("Badge",    377, ItemClassification.useful),

    #Consumeables
    "Cocoa Truffles":                                          TeviItemData("Consumeable",  380, ItemClassification.filler,0,999999,5), 
    "Fluffy Cream Puff":                                       TeviItemData("Consumeable",  381, ItemClassification.filler,0,999999,5), 
    "Vitalolly":                                               TeviItemData("Consumeable",  382, ItemClassification.filler,0,999999,5), 
    "Energy Happy Juice":                                      TeviItemData("Consumeable",  383, ItemClassification.filler,0,999999,5), 
    "Crispy Crunchsicle":                                      TeviItemData("Consumeable",  384, ItemClassification.filler,0,999999,5), 
    "Rewind Donut":                                            TeviItemData("Consumeable",  385, ItemClassification.filler,0,999999,5), 
    "Voodoo's Mewmew Cookie":                                  TeviItemData("Consumeable",  386, ItemClassification.filler,0,999999,5), 
    "Snowflake Rumi Cake":                                     TeviItemData("Consumeable",  387, ItemClassification.filler,0,999999,5), 
    "Rainbowba":                                               TeviItemData("Consumeable",  388, ItemClassification.filler,0,999999,5), 
    "Waffle of Wonder (Attempt)":                              TeviItemData("Consumeable",  389, ItemClassification.filler,0,999999,5), 
    "Mysterious Confection":                                   TeviItemData("Consumeable",  390, ItemClassification.filler,0,999999,5), 
    "Honeycloud Waffle":                                       TeviItemData("Consumeable",  391, ItemClassification.filler,1,999999,100), 
    "Toasted Meringue Waffle":                                 TeviItemData("Consumeable",  392, ItemClassification.filler,1,999999,100), 
    "Good Morning Waffle":                                     TeviItemData("Consumeable",  393, ItemClassification.filler,1,999999,100), 
    "Berry Pink Waffle":                                       TeviItemData("Consumeable",  394, ItemClassification.filler,1,999999,100), 
    "Blueberry Waffle":                                        TeviItemData("Consumeable",  395, ItemClassification.filler,1,999999,100), 
    "Whimsical Waffle of Wonder":                              TeviItemData("Consumeable",  396, ItemClassification.filler,0,999999,5), 
    #"Silver Bell":                                            TeviItemData("Consumeable",  397, ItemClassification.filler), 
    "Void Bomb":                                               TeviItemData("Consumeable",  398, ItemClassification.progression,1,999999), 
    "Cloud Bomb":                                              TeviItemData("Consumeable",  399, ItemClassification.progression,1,999999), 
    "BB Rabbit":                                               TeviItemData("Consumeable",  400, ItemClassification.progression,1,999999), 
    "Calico Bomb":                                             TeviItemData("Consumeable",  401, ItemClassification.progression,1,999999), 
    "Tabby Bomb":                                              TeviItemData("Consumeable",  402, ItemClassification.progression,1,999999), 
    #"Memorial Bookmark":                                       TeviItemData("Consumeable",  403, ItemClassification.filler,0,0,20), 
    "Burnt Dessert":                                           TeviItemData("Consumeable",  404, ItemClassification.filler,0,999999,5), 
    "Pocket Biscuit":                                          TeviItemData("Consumeable",  405, ItemClassification.filler,0,999999,5) 
    }

teleporter_table: Dict[str,TeviItemData] = {
    "Teleporter Desert Base":                                       TeviItemData("Teleporter", 1000, ItemClassification.progression,1,1), 
    "Teleporter Canyon":                                            TeviItemData("Teleporter", 1001, ItemClassification.progression,1,1), 
    "Teleporter Oasis":                                             TeviItemData("Teleporter", 1002, ItemClassification.progression,1,1), 
    "Teleporter Morose":                                            TeviItemData("Teleporter", 1003, ItemClassification.progression,1,1), 
    "Teleporter ForestMaze":                                        TeviItemData("Teleporter", 1004, ItemClassification.progression,1,1), 
    "Teleporter Forest":                                            TeviItemData("Teleporter", 1005, ItemClassification.progression,1,1), 
    "Teleporter Mines":                                             TeviItemData("Teleporter", 1006, ItemClassification.progression,1,1), 
    "Teleporter Industry":                                          TeviItemData("Teleporter", 1007, ItemClassification.progression,1,1), 
    "Teleporter Copper Forest":                                     TeviItemData("Teleporter", 1008, ItemClassification.progression,1,1), 
    "Teleporter Anathema":                                          TeviItemData("Teleporter", 1009, ItemClassification.progression,1,1), 
    "Teleporter Gloamwood":                                         TeviItemData("Teleporter", 1010, ItemClassification.progression,1,1), 
    "Teleporter Plague":                                            TeviItemData("Teleporter", 1011, ItemClassification.progression,1,1), 
    "Teleporter Ulvosa":                                            TeviItemData("Teleporter", 1012, ItemClassification.progression,1,1), 
    "Teleporter Snow Village":                                      TeviItemData("Teleporter", 1013, ItemClassification.progression,1,1), 
    "Teleporter Sea":                                               TeviItemData("Teleporter", 1014, ItemClassification.progression,1,1), 
    "Teleporter Ocean":                                             TeviItemData("Teleporter", 1015, ItemClassification.progression,1,1), 
    "Teleporter Forgotten City":                                    TeviItemData("Teleporter", 1016, ItemClassification.progression,1,1), 
    "Teleporter Tartarus":                                          TeviItemData("Teleporter", 1017, ItemClassification.progression,1,1), 
    "Teleporter Snow City":                                         TeviItemData("Teleporter", 1018, ItemClassification.progression,1,1), 
    "Teleporter Magma Depths":                                      TeviItemData("Teleporter", 1019, ItemClassification.progression,1,1), 
    "Teleporter Dreamkeeper Outside":                               TeviItemData("Teleporter", 1020, ItemClassification.progression,1,1), 
    "Teleporter Dreamkeeper Inside":                                TeviItemData("Teleporter", 1021, ItemClassification.progression,1,1), 
    "Teleporter Deep Dream":                                        TeviItemData("Teleporter", 1022, ItemClassification.progression,1,1), 
    "Teleporter Valhalla Breath East":                              TeviItemData("Teleporter", 1023, ItemClassification.progression,1,1), 
    "Teleporter Valhalla City":                                     TeviItemData("Teleporter", 1024, ItemClassification.progression,1,1), 
    "Teleporter Heavens Valley West":                               TeviItemData("Teleporter", 1025, ItemClassification.progression,1,1), 
    "Teleporter Valhalla Breath West":                              TeviItemData("Teleporter", 1026, ItemClassification.progression,1,1), 
    "Teleporter Ruins":                                             TeviItemData("Teleporter", 1027, ItemClassification.progression,1,1), 
    "Teleporter Sinner's Hell":                                     TeviItemData("Teleporter", 1028, ItemClassification.progression,1,1), 
    "Teleporter Relicts":                                           TeviItemData("Teleporter", 1029, ItemClassification.progression,1,1), 
    "Teleporter Catacombs":                                         TeviItemData("Teleporter", 1030, ItemClassification.progression,1,1), 
    "Teleporter Lab":                                               TeviItemData("Teleporter", 1031, ItemClassification.progression,1,1), 
    "Teleporter Cloister":                                          TeviItemData("Teleporter", 1032, ItemClassification.progression,1,1), 
    "Teleporter Gallery of Mirrors":                                TeviItemData("Teleporter", 1033, ItemClassification.progression,1,1), 
    "Teleporter Gallery of Souls":                                  TeviItemData("Teleporter", 1034, ItemClassification.progression,1,1), 
    "Teleporter Blushwood":                                         TeviItemData("Teleporter", 1035, ItemClassification.progression,1,1), 
    "Teleporter Evernight Garden":                                  TeviItemData("Teleporter", 1036, ItemClassification.progression,1,1), 
}

event_item_table: Dict[str, TeviItemData] = {

}

trap_table: Dict[str,TeviItemData] = {
    "Reverse Camera":                                               TeviItemData("Trap",   2000, ItemClassification.trap,0,99999999,1), 
    "Double Time":                                                  TeviItemData("Trap",   2001, ItemClassification.trap,0,99999999,1), 
    "Yeet":                                                         TeviItemData("Trap",   2002, ItemClassification.trap,0,99999999,1), 
    "Debuff":                                                       TeviItemData("Trap",   2003, ItemClassification.trap,0,99999999,6), 
    "Taunt":                                                        TeviItemData("Trap",   2004, ItemClassification.trap,0,99999999,1), 
    "Reduce Jump Height":                                            TeviItemData("Trap",  2005, ItemClassification.trap,0,99999999,1), 
}


all_item_table = item_table|teleporter_table|trap_table
