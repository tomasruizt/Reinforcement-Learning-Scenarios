import unittest

from scenario.blackjack.cards_deck.card import Card
from scenario.blackjack.cards_deck.hand import Hand


class HandTest(unittest.TestCase):
    def test_score_single_ace_lowered(self):
        cards_list = [Card("A"), Card("10"), Card("2")]
        expected_score = 13
        expected_card_names = ("A", "10", "2")
        expected_quantities = (1, 1, 1)

        hand = Hand(cards_list)
        self.assertEqual(hand.score, expected_score)
        self.assertEqual(hand.card_names, expected_card_names)
        self.assertEqual(hand.quantities, expected_quantities)

    def test_score_multiple_aces_lowered(self):
        cards_list = [Card("A"), Card("A"), Card("A"), Card("K")]
        expected_score = 13
        expected_card_names = ("A", "K")
        expected_quantities = (3, 1)

        hand = Hand(cards_list)
        self.assertEqual(hand.score, expected_score)
        self.assertEqual(hand.card_names, expected_card_names)
        self.assertEqual(hand.quantities, expected_quantities)

    def test_score_single_ace_blackjack(self):
        cards_list = [Card("A"), Card("K")]
        expected_score = 21
        expected_card_names = ("A", "K")
        expected_quantities = (1, 1)

        hand = Hand(cards_list)
        self.assertEqual(hand.score, expected_score)
        self.assertEqual(hand.card_names, expected_card_names)
        self.assertEqual(hand.quantities, expected_quantities)

    def test_add_card_doesnt_modify_hand(self):
        cards_list = [Card("K"), Card("K")]
        new_card = Card("4")
        expected_score = 20
        expected_card_names = ("K",)
        expected_quantities = (2,)

        old_hand = Hand(cards_list)
        old_hand.add_card(new_card)
        self.assertEqual(old_hand.score, expected_score)
        self.assertEqual(old_hand.card_names, expected_card_names)
        self.assertEqual(old_hand.quantities, expected_quantities)

    def test_add_card_return_new_hand(self):
        cards_list = [Card("K"), Card("K")]
        new_card = Card("4")
        expected_score = 24
        expected_card_names = ("K", "4")
        expected_quantities = (2, 1)

        new_hand = Hand(cards_list).add_card(new_card)
        self.assertEqual(new_hand.score, expected_score)
        self.assertEqual(new_hand.card_names, expected_card_names)
        self.assertEqual(new_hand.quantities, expected_quantities)
