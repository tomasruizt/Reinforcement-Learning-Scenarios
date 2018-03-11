from collections import Counter

from scenario.blackjack.Card import Card
from scenario.blackjack.state_representation.BlackjackStateRepresentation import BlackjackStateRepresentation


class BlackjackStateRepresentationBuilder:
    """
    Auxiliary builder class to construct new representations for the blackjack states
    """

    @staticmethod
    def from_old_state_plus_new_card(
            old_state_representation: BlackjackStateRepresentation, new_card: Card) -> BlackjackStateRepresentation:
        new_player_cards = Counter(old_state_representation.player_cards)
        new_player_cards[new_card] += 1
        return BlackjackStateRepresentation(
            player_cards=new_player_cards,
            opponent_cards=old_state_representation.opponent_cards,
            current_bet=old_state_representation.current_bet,
            passed=old_state_representation.passed
        )

    @staticmethod
    def from_old_state_with_action_pass(
            old_state_representation: BlackjackStateRepresentation) -> BlackjackStateRepresentation:
        return BlackjackStateRepresentation(
            player_cards=old_state_representation.player_cards,
            opponent_cards=old_state_representation.opponent_cards,
            current_bet=old_state_representation.current_bet,
            passed=True
        )
