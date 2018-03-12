class Card:
    """
    A simple representation of a card with a name and a corresponding
    value.
    """

    # The mapping from cards to their scores
    _map_names_to_scores = {str(i): i for i in range(2, 11)}
    _map_names_to_scores.update({"A": (1, 11), "K": 10, "Q": 10, "J": 10})

    def __init__(self, name: str):
        """
        Initializes the card with the input name. The name defines its
        value. Possible names include '2' to '10', 'J', 'Q', 'K' and
        'A'.
        :param name: The name of the card, which will determine its
        value.
        """
        assert name in Card._map_names_to_scores
        self.name = name
        self.value = self._map_names_to_scores[name]

    def __str__(self):
        return "Card{{name: {}, value: {}}}".format(
            self.name, self.value)
