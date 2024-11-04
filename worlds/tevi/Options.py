"""This module represents option defintions for Rabi-Ribi"""
from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Toggle, Range,DeathLink

class OpenMorose(Toggle):
    """Gain access to Morose without Crossbomb"""
    display_name = "Open Morose"

class RandomizeKnife(Toggle):
    """If set to false, the Knife is at the default location"""
    display_name = "Randomize Knife"

class TransitionShuffle(Toggle):
    """Shuffles every Map transition"""
    display_name = "Map Shuffle"

class RandomizeOrb(Toggle):
    """If set to false, the Orb is at the default location"""
    display_name = "Randomize Orb"

class RandomizedItemUpgrades(Toggle):
    """
    If set to true, all Item upgrades in the Crafting Menu have random new Item
    and the Item upgrades are in a different Location i.e. on the overworld.     
    """
    display_name = "Randomized Item Upgrades"

class CeliaSableUnlocked(Toggle):
    """If this flag is true, Celia and Sable are already unlocked"""
    display_name = "Unlock Celia and Sable "

class FreeAttackUp(Range):
    """
    Start the Game with X amount of Atk Ups

    This is usefull if Bosses 
    """
    range_start = 0
    range_end = 220
    default = 0
    
class ItemChaos(Toggle):
    """
    Item Chaos rerolls every non Progressive Item into a new Item.
    The new Item can be any type of Item as long as it can be stacked,
    this include even Item like High Jump.
    """
    display_name = "Chaos mode"

class GearCount(Range):
    """
    The Amount of Gears found in the Game
    """
    range_start = 1
    range_end = 25
    default = 20

class GoalCount(Range):
    """
    The Amount of Gears required to Finish the Game
    If this Number is greater than Gear count,
    it is reduced to the Number of Gear count
    """
    range_start = 1
    range_end = 25
    default = 16

class RabbitJump(Toggle):
    """
    Using a Item with 200% item use to reach ledges after a Walljump
    """
    display_name = "Rabbit Jump"
class RabbitWalljump(Toggle):
    """
    Using a Item with 200% item use to Climb a Wall (Higher FPS is easier)
    """
    display_name = "Rabbit Walljump"

class Backflip(Toggle):
    """
    Backflip enables a early mini double jump
    """
    display_name = "Backflip"
class CKick(Toggle):
    """
    Use a dropkick against a ceiling to reverse movement Direction
    """
    display_name = "Ceiling kick"
    
class HiddenP(Toggle):
    """
    Have the knowledge of all hidden Paths in Free Roam 
    """
    display_name = "Hidden Paths"

class EarlyDream(Toggle):
    "Skip Dreamkeeper wind with Dropkicks and Strong Air Up"
    display_name = "Dream Keeper entrance skip"




@dataclass
class TeviOptions(PerGameCommonOptions):
    """Tevi Options Definition"""
    open_morose: OpenMorose
    randomize_knife: RandomizeKnife
    randomize_orb: RandomizeOrb
    randomize_item_upgrade: RandomizedItemUpgrades
    chaos_mode: ItemChaos
    celia_sable: CeliaSableUnlocked
    free_attack_up : FreeAttackUp
    gear_count: GearCount
    goal_count: GoalCount
    transitionShuffle: TransitionShuffle
    RJump:RabbitJump
    RWalljump:RabbitWalljump
    backflip:Backflip
    cKick:CKick
    hiddenP:HiddenP
    earlydream: EarlyDream