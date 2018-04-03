import unittest

from scenario.blackjack.blackjack_environment import BlackjackEnvironment


class BlackjackEnvironmentTest(unittest.TestCase):

    def test_construction(self):
        BlackjackEnvironment()
