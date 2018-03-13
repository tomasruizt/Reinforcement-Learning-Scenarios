import random

from scenario.blackjack.cards_deck import PokerCardsDeck, Card


class InfiniteDeck(PokerCardsDeck):
    """A Poker cards deck with infinite cards. The probabilities of
    drawing any of the possible cards remain steady at 1 in 13"""

    def __init__(self):
        self._possible_cards_names = {str(i) for i in range(2, 11)}
        self._possible_cards_names.update({"J", "Q", "K", "A"})

    def draw_card(self):
        """Returns one of the possible 13 poker cards at random."""
        card_name = random.sample(self._possible_cards_names, 1)[0]  # unpack
        return Card(card_name)

    def cards_remain(self) -> bool:
        """True, because this deck always has cards remaining."""
        return True
