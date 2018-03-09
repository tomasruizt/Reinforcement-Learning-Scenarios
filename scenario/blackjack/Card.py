class Card:
    """
    A simple representation of a card with a name and a corresponding value.
    """

    _name_to_value_map = {str(i): [i] for i in range(2, 11)}
    _name_to_value_map.update({"A": [1, 11], "K": [10], "Q": [10], "J": [10]})

    def __init__(self, name: str):
        assert name in Card._name_to_value_map
        self.name = name
        self.value = Card._name_to_value_map[name]

    def __str__(self):
        return "Card{{name: {}, value: {}}}".format(self.name, self.value)
