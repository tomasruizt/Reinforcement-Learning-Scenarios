from enum import Enum, auto

from rl.action import DiscreteAction


class BlackjackAction(DiscreteAction, Enum):
    """The Blackjack action is either 'DRAW' or 'PASS'"""
    DRAW = auto()
    PASS = auto()
