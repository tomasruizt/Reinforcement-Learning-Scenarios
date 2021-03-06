from collections import Counter
from typing import Iterable, Sequence, List

from scenario.blackjack.cards_deck.card import Card


class Hand:
    """A representation of the hand and the methods to manipulate Hands"""

    def __init__(self, cards_list: Sequence[Card]):
        """
        Creates a snapshot of the hand.
        :param cards_list: The Cards that form the hand.
        """
        self._save_as_tuples(cards_list)
        self.score = self._calculate_score(cards_list)

    def add_card(self, new_card: Card):
        """
        Returns a new Hand object containing all the current cards of this
        Hand plus the input Card.
        :param new_card: The Card that will be added to the Hand.
        :return: New Hand object.
        """
        cards_list = self._get_hands_cards_list()
        cards_list.append(new_card)
        return Hand(cards_list)

    # Private Methods

    def _save_as_tuples(self, cards_list: Sequence[Card]):
        """Tuples can't be changed accidentally."""
        counter = Counter((card.name for card in cards_list))
        self.card_names, self.quantities = zip(*sorted(counter.items()))

    @staticmethod
    def _calculate_score(cards_list: Iterable[Card]) -> int:
        """Calculates the best possible score of this hand"""
        # For Aces, assume their value to be 1 at first. Then add 10 if it
        # increases the score without busting.
        score = 0
        for card in cards_list:
            card_value = 1 if card.name is "A" else card.value
            score += card_value
        card_names = (card.name for card in cards_list)
        if "A" in card_names and score <= 11:
            score += 10
        return score

    def _get_hands_cards_list(self) -> List[Card]:
        cards_list = []
        for card_name, quantity in zip(self.card_names, self.quantities):
            for _ in range(quantity):
                cards_list.append(Card(card_name))
        return cards_list

    def __eq__(self, other):
        return (self.card_names == other.card_names
                and self.quantities == other.quantities
                and self.score == other.score)
