"""This module represents option defintions for Rabi-Ribi"""
from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Toggle, Range,DeathLink

class OpenMorose(Toggle):
    """Gain access to Morose without Crossbomb"""
    display_name = "Open Morose"

class SuperBosses(Toggle):
    """Consider Tevi's Hidden Bosses in Library for the Logic"""
    display_name = "Super Bosses"

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

    This is usefull to kill Bosses faster
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

class GoalType(Choice):
    """
    Determines the requirement type to fight the Final Boss
    """ 
    display_name = "Goal Type"
    option_AstralGear = 0
    option_KillBosses = 1
  
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
    
class BarrierSkip(Choice):
    """
    Skip Cutscene Barriers with Airdash (easy) or Slide (hard) and requires 60 fps lock
    """
    display_name = "Barrier Skip"
    option_disable = 0
    option_easy = 1
    option_hard = 2
    default = 0
      
class HiddenPaths(Toggle):
    """
    Consider Hidden Paths in Free Roam for the logic
    """
    display_name = "Hidden Paths"

class EarlyDream(Toggle):
    "Skip Dreamkeeper wind with Dropkicks and Strong Air Up"
    display_name = "Dream Keeper entrance skip"


class ADCKick(Toggle):
    """
    Enter Gallery of Souls with a a precise Airdash into Walljump from Ceiling pixel 
    (very hard)
    """
    display_name = "ADCKick"




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
    goal_type: GoalType
    gear_count: GearCount
    goal_count: GoalCount
    transitionShuffle: TransitionShuffle
    RJump:RabbitJump
    RWalljump:RabbitWalljump
    backflip:Backflip
    cKick:CKick
    hiddenP:HiddenPaths
    earlydream: EarlyDream
    barrierSkip: BarrierSkip
    adcKick : ADCKick
    superBosses: SuperBosses
    
    def getOptions(self):
        return {
            "open_morose":self.open_morose.value,
            "randomize_knife":self.randomize_knife.value,
            "randomize_orb":self.randomize_orb.value,
            "randomize_item_upgrade":self.randomize_item_upgrade.value,
            "chaos_mode":self.chaos_mode.value,
            "celia_sable":self.celia_sable.value,
            "free_attack_up":self.free_attack_up.value,
            "goal_type": self.goal_type.value,
            "gear_count":self.gear_count.value,
            "goal_count":self.goal_count.value,
            "transitionShuffle":self.transitionShuffle.value,
            "RJump":self.RJump.value,
            "RWalljump":self.RWalljump.value,
            "backflip":self.backflip.value,
            "cKick":self.cKick.value,
            "hiddenP":self.hiddenP.value,
            "earlydream":self.earlydream.value,
            "barrierSkip":self.barrierSkip.value,
            "adcKick":self.adcKick.value,
            "superBosses":self.superBosses.value
        }