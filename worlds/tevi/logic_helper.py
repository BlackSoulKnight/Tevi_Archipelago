"""
This module defines helper methods used for evaluating rule lambdas.
Its probably a little haphazardly sorted.. but the method names are descriptive
enough for it not to be confusing.
"""
from BaseClasses import CollectionState, MultiWorld
from .TeviToApNames import TeviToApNames
from .Options import TeviOptions
from worlds.AutoWorld import LogicMixin
from typing import Dict

class TeviLogicMixing(LogicMixin):
    def init_mixin(self,multiworld: MultiWorld):
        self._tevi_is_in_race = {
            player:0 for player in multiworld.get_game_players("Tevi")
        }
    def copy_mixin(self, new_state: CollectionState) -> CollectionState:
        new_state._tevi_is_in_race = {
            player: race for player, race in self._tevi_is_in_race.items()
        }
        return new_state

class TeviLogic():

    def has_item_levelX(item:str,state: CollectionState, player:int):
        """Player has Item Level X"""
        split = item.split(" ")
        level = 1
        if len(split) > 1:
            level = int(split[1])
        item = split[0]
        if "AREABOMB" in item:
            return state.has(TeviToApNames[item],player,level) and state.has(TeviToApNames["ITEM_LINEBOMB"],player,1)
        if "AirSlide" in item:
            return state.has(TeviToApNames[item],player,level) and state.has(TeviToApNames["ITEM_SLIDE"],player,1)
        if "BOMBFUEL" in item:
            return state.has(TeviToApNames[item],player,level) and state.has(TeviToApNames["ITEM_LINEBOMB"],player,1)
        if "ITEM_Rotater" in item:
            return state.has(TeviToApNames[item],player,level) and state.has(TeviToApNames["ITEM_KNIFE"],player,1)
        if "ITEM_BombLengthExtend" in item:
            return state.has(TeviToApNames[item],player,level) and state.has(TeviToApNames["ITEM_LINEBOMB"],player,1)
        if "EVENT" in item:
            return state.has(item,player,level)
        return state.has(TeviToApNames[item],player,level)

    def can_reach_goal(state:CollectionState,player:int,goalCount:int):
        return state.has(TeviToApNames["STACKABLE_COG"],player,goalCount)


    def has_Chapter_reached(chapter:int,state:CollectionState,player:int):
        """Check if enough Bosses are kille to be in Chapter X"""
        counter = 0
        boss_killed = state.count("EVENT_BOSS",player)
        if(boss_killed >= 1):
            counter +=1
        if(boss_killed >= 3):
            counter +=1
        if(boss_killed >= 5):
            counter +=1
        if(boss_killed >= 7):
            counter +=1
        if(boss_killed >= 10):
            counter +=1
        if(boss_killed >= 13):
            counter +=1
        if(boss_killed >= 16):
            counter +=1
        if(boss_killed >= 20):
            counter +=1
        return counter >= chapter

    def can_use_ChargeShot(state: CollectionState, player:int):
        return state.has(TeviToApNames["ITEM_ORB"],player,2)

    def can_destroy_MoneyBlocks(state: CollectionState, player:int):
        """Check if Money Blocks can be destroyed by the Player"""
        return state.has(TeviToApNames["ITEM_LINEBOMB"],player) or state.has(TeviToApNames["ITEM_KNIFE"],player)

    def can_upgrade_Compass(state:CollectionState, player:int):
        return state.has("EVENT_Memine",player,3)

    def completed_Memine(state:CollectionState, player:int):
        return state.has("EVENT_Memine",player,6)

    def can_Upgrade_Items(state:CollectionState,player:int,option_VanillaCraft:bool):
        """Check if enough Material can be collected"""
        #No Logic was made yet for this so we check the basic needs to reach everyting
        return (option_VanillaCraft or TeviLogic.has_all_Movement(state,player)) and state.has(TeviToApNames["ITEM_LINEBOMB"],player)

    def can_Upgrade_OrbType(state:CollectionState,player:int):
        return TeviLogic.has_all_Movement(state,player) and state.has(TeviToApNames["ITEM_LINEBOMB"],player)

    def can_Upgrade_Core(state:CollectionState,player:int):
        return TeviLogic.has_all_Movement(state,player) and state.has_all([TeviToApNames["ITEM_LINEBOMB"],TeviToApNames["ITEM_AREABOMB"],TeviToApNames["ITEM_BombLengthExtend"]],player)

    def has_all_Movement(state:CollectionState,player:int):
        return state.has_all([TeviToApNames["ITEM_DOUBLEJUMP"],
                            TeviToApNames["ITEM_AirDash"],
                            TeviToApNames["ITEM_WALLJUMP"],
                            TeviToApNames["ITEM_JETPACK"],
                            TeviToApNames["ITEM_SLIDE"],
                            TeviToApNames["ITEM_HIJUMP"],
                            TeviToApNames["ITEM_WATERMOVEMENT"]],player)

    def can_use_SpinnerBash(state:CollectionState,player:int):
        return state.has(TeviToApNames["ITEM_KNIFE"],player)

    def can_finish_Memine(state:CollectionState,player:int):
        return state.has(TeviToApNames["ITEM_LINEBOMB"],player) and TeviLogic.can_use_ChargeShot(state,player) and TeviLogic.has_all_Movement(state,player)

    def can_use_VenaBomb(state:CollectionState,player:int):
        void = state.has_all([TeviToApNames["Useable_VenaBombSmall"],"EVENT_Fire"],player)
        cloud = state.has_all([TeviToApNames["Useable_VenaBombBig"],"EVENT_Fire","EVENT_Light"],player)
        calico = state.has_all([TeviToApNames["Useable_VenaBombDispel"],"EVENT_Water","EVENT_Earth"],player)
        tabby = state.has_all([TeviToApNames["Useable_VenaBombHealBlock"],"EVENT_Dark","EVENT_Earth"],player)
        return void or cloud or calico or tabby

    def has_fast_item(state:CollectionState,player:int):
        return state.has_any([TeviToApNames["Useable_VenaBombBunBun"]],player)

    def can_use_travelSystem(state:CollectionState,player:int,travelItem):
        return state._tevi_is_in_race[player] == False and state.has(travelItem,player)
    
    def can_complete_race(state:CollectionState,player:int,race:str):
        if len(race) in [12,14]:
            return TeviLogic.has_item_levelX(race,state,player)
        state._tevi_is_in_race[player] = True
        possible = state.can_reach_location(race,player)
        state._tevi_is_in_race[player] = False
        return possible

    def trick_RabbitJump(state:CollectionState,player:int,options:TeviOptions):
        return options.RJump.value>0 and TeviLogic.has_fast_item(state,player)

    def trick_RabbitWalljump(state:CollectionState,player:int,options:TeviOptions):
        return options.RWalljump.value>0 and TeviLogic.has_fast_item(state,player)

    def trick_HiddenP(state:CollectionState,player:int,options:TeviOptions):
        return options.hiddenP.value>0
    def trick_EarlyDream(state:CollectionState,player:int,options:TeviOptions):
        return options.earlydream.value>0 and TeviLogic.has_item_levelX("ITEM_KNIFE",state,player)

    def trick_ckick(state:CollectionState,player:int,options:TeviOptions):
        return options.cKick.value >0

    def trick_backflip(state:CollectionState,player:int,options:TeviOptions):
        return options.backflip>0 and state.has(TeviToApNames["ITEM_KNIFE"],player)

    def trick_barrierSkip(state:CollectionState,player:int,options:TeviOptions):
        val = options.barrierSkip.value
        if val >1:
            return state.has_any([TeviToApNames["ITEM_AirDash"],TeviToApNames["ITEM_SLIDE"]],player)
        if val >0:
            return state.has(TeviToApNames["ITEM_AirDash"],player)
        return lambda _ :False

    def trick_ADCKick(state:CollectionState,player:int,options:TeviOptions):
        return options.adcKick >0 and state.has(TeviToApNames["ITEM_AirDash"],player)