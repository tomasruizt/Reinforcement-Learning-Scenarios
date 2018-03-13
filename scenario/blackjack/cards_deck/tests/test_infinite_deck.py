import unittest

from scenario.blackjack.cards_deck import Card
from scenario.blackjack.cards_deck.infinite_deck import InfiniteDeck


class InfiniteDeckTest(unittest.TestCase):

    def test_draw_card_at_least_1000_cards(self):
        deck = InfiniteDeck()
        num_of_cards = 1000
        for _ in range(num_of_cards):
            self.assertTrue(deck.cards_remain())
            self.assertIsInstance(deck.draw_card(), Card)
