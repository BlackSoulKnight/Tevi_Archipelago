import os,re,json,pkgutil
from BaseClasses import CollectionState, Region
from .logic_helper import *
from .TeviToApNames import TeviToApNames
from typing import Dict,List




def evaluate_rule(existing_rule: str, player: int, regions: Dict[int, Dict[str, Region]], options):
    """
    This method converts a rule from the existing randomizer to a lambda which can be passed to AP.
    The existing randomizer evaluates a defined logic expression, which it seperates into 5 classes:
        - OpLit
        - OpAnd
        - OpOr
        - OpNot

    OpLit is used to evaluate a single literal statement. This can be having an item, or
    can be more complex (e.g. conjunction of literals), which is combined into a single literal
    in the existing randomizer. For the more complicated literals, Ive defined methods above to
    translate them, and placed them in the below "literal_eval_map". If its not in the below map,
    assume the literal is an item which we can check the state for.

    The other Ops are self explanatory, and are translated accordingly.

    :str existing_rule: The existing rule as an string.
    :player int: the relevant player

    :returns: An evaluatable labmda with one argument (for state)

    :raises ValueError: the passed in existing_rule is not a valid OpX object.
    """
    #convert string into a OpX objeect

    if isinstance(existing_rule, OpLit):
        literal = existing_rule.name
        literal_eval_map = {
            "True": lambda _: True,
            "None": lambda _: True,
            "False": lambda _: False,
            "Boss": lambda _: True,
            "ItemUse": lambda _: True,
            "BounceKick": lambda _: False,
            "EnemyManip": lambda _: False,
            "WindSkip": lambda _: False,
            "Hard": lambda _: False,
            "Explorer": lambda _: False
        }

        if "Coins" in literal:
            coins = int(literal.split(" ")[1])
            if coins >250:
                return lambda state: can_destroy_MoneyBlocks(state,player)
            else:
                return lambda _: True
        if "RainbowCheck" == literal:
            return lambda state: can_upgrade_Compass(state,player)
        if "AllMemine" == literal:
            return lambda state: completed_Memine(state,player)
        if "Memine" == literal:
            return lambda state: can_finish_Memine(state,player)
        if "SpinnerBash" == literal:
            return lambda state: can_use_SpinnerBash(state,player)
        if "ChargeShot" == literal:
            return lambda state: can_use_ChargeShot(state,player)
        if "Chapter" in literal:
            chapter = int(literal.split(" ")[1])
            return lambda state: has_Chapter_reached(chapter,state,player)
        if "Upgrade" in literal:
            return lambda state: can_Upgrade_Items(state,player, not options.randomize_item_upgrade.value)
        if "OpenMorose" == literal:
            return lambda _: (options.open_morose.value > 0)
        if "VenaBomb" == literal:
            return lambda state: can_use_VenaBomb(state,player)
        #tricks
        if "BarrierSkip":
            return lambda state: trick_barrierSkip(state,player,options)
        if "ADCKick":
            return lambda state: trick_ADCKick(state,player,options)
        if "BackFlip" == literal:
            return lambda state: trick_backflip(state,player,options)
        if "CKick" == literal:
            return lambda state: trick_ckick(state,player,options)
        if "HiddenP" == literal:
            return lambda state: trick_HiddenP(state,player,options)
        if "RabbitJump" == literal:
            return lambda state: trick_RabbitJump(state,player,options)
        if "RabbitWalljump" == literal:
            return lambda state: trick_RabbitWalljump(state,player,options)
        if "EarlyDream" == literal:
            return lambda state: trick_EarlyDream(state,player,options)

        #needs to changed
        if "Core" in literal:
            return lambda state: can_Upgrade_Core(state,player)
        if "Goal" == literal:
            return lambda state: can_reach_goal(state,player,options.goal_count.value)
        if literal == "I19" or literal == "I20":
            return lambda state: state.has(TeviToApNames[literal],player)

        if literal in literal_eval_map:
            return literal_eval_map[literal]

        return lambda state: has_item_levelX(literal,state,player)

    elif isinstance(existing_rule, OpNot):
        expr = evaluate_rule(existing_rule.expr, player, regions, options)
        return lambda state: not expr(state)
    elif isinstance(existing_rule, OpOr):
        expr_l = evaluate_rule(existing_rule.exprL, player, regions, options)
        expr_r = evaluate_rule(existing_rule.exprR, player, regions, options)
        return lambda state: expr_l(state) or expr_r(state)
    elif isinstance(existing_rule, OpAnd):
        expr_l = evaluate_rule(existing_rule.exprL, player, regions, options)
        expr_r = evaluate_rule(existing_rule.exprR, player, regions, options)
        return lambda state: expr_l(state) and expr_r(state)
    raise ValueError("Invalid Expression recieved.")


isExpr = lambda s : not type(s) is str
def parse_expression_logic(line):
    if line == "" or line == "()":
        line = "True"
    pat = re.compile('[()&|~!]')
    line = line.replace('&&', '&').replace('||', '|')
    tokens = (s.strip() for s in re.split('([()&|!~])', line))
    tokens = [s for s in tokens if s]
    # Stack-based parsing. pop from [tokens], push into [stack]
    # We push an expression into [tokens] if we want to process it next iteration.
    tokens.reverse()
    stack = []
    while len(tokens) > 0:
        next = tokens.pop()
        if isExpr(next):
            if len(stack) == 0:
                stack.append(next)
                continue
            head = stack[-1]
            if head == '&':
                stack.pop()
                exp = stack.pop()
                assert isExpr(exp)
                tokens.append(OpAnd(exp, next))
            elif head == '|':
                stack.pop()
                exp = stack.pop()
                assert isExpr(exp)
                tokens.append(OpOr(exp, next))
            elif head in '!~':
                stack.pop()
                tokens.append(OpNot(next))
            else:
                stack.append(next)
        elif next in '(&|!~':
            stack.append(next)
        elif next == ')':
            exp = stack.pop()
            assert isExpr(exp)
            assert stack.pop() == '('
            tokens.append(exp)
        else: # string literal
            # Literal parsing
                    tokens.append(OpLit(next))
    assert len(stack) == 1
    return stack[0]

class OpLit(object):
    def __init__(self, name):
        self.name = name
    def evaluate(self, variables):
        return variables[self.name]
    def __str__(self):
        return self.name
    __repr__ = __str__

class OpNot(object):
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, variables):
        return not self.expr.evaluate(variables)
    def __str__(self):
        return '(NOT %s)' % self.expr
    __repr__ = __str__

class OpOr(object):
    def __init__(self, exprL, exprR):
        self.exprL = exprL
        self.exprR = exprR
    def evaluate(self, variables):
        return self.exprL.evaluate(variables) or self.exprR.evaluate(variables)
    def __str__(self):
        return '(%s OR %s)' % (self.exprL, self.exprR)
    __repr__ = __str__

class OpAnd(object):
    def __init__(self, exprL, exprR):
        self.exprL = exprL
        self.exprR = exprR
    def evaluate(self, variables):
        return self.exprL.evaluate(variables) and self.exprR.evaluate(variables)
    def __str__(self):
        return '(%s AND %s)' % (self.exprL, self.exprR)
    __repr__ = __str__

def GetAllUpgradeables() -> List[str]:
    return [ 
        "ITEM_KNIFE",
        "ITEM_ORB",
        "ITEM_RapidShots",
        "ITEM_AttackRange",
        "ITEM_EasyStyle",
        "ITEM_LINEBOMB",
        "ITEM_AREABOMB",
        "ITEM_SPEEDUP",
        "ITEM_AirDash",
        "ITEM_WALLJUMP",
        "ITEM_JETPACK",
        "ITEM_BoostSystem",
        "ITEM_BombLengthExtend",
        "ITEM_MASK",
        "ITEM_TempRing",
        "ITEM_DodgeShot",
        "ITEM_Rotater",
        "ITEM_GoldenGlove",
        "ITEM_OrbAmulet",
        "ITEM_BOMBFUEL",
        "ITEM_Explorer"
        ]



