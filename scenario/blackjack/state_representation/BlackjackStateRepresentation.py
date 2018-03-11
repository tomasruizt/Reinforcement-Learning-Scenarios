from typing import Counter

from scenario.blackjack.Card import Card


class BlackjackStateRepresentation:
    """
    An object containing all the state information for a single player Blackjack game against one opponent.
    """

    def __init__(self, player_cards: Counter[Card], opponent_cards: Counter[Card],
                 current_bet: int, passed: bool):
        self.player_cards = player_cards
        self.opponent_cards = opponent_cards
        self.current_bet = current_bet
        self.passed = passed
