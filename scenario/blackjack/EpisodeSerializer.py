from typing import Dict, Counter

from rl.episode import DiscreteEpisode

from scenario.blackjack.state_representation import BlackjackStateRepresentation
from scenario.blackjack.Card import Card


class EpisodeSerializer:

    @staticmethod
    def to_json(episode: DiscreteEpisode):
        return {
            "episode": {
                "start state": {
                    # action space is constant: draw or pass
                    # "action space": episode.start_state.action_space,
                    "state representation": EpisodeSerializer._serialize_state_representation(
                        episode.start_state.representation)
                },
                "action chosen": episode.action_chosen.name,
                "reward": episode.reward,
                "end state": {
                    # "action space": episode.end_state.action_space
                    "state representation": EpisodeSerializer._serialize_state_representation(
                        episode.end_state.representation)
                }
            }
        }

    @staticmethod
    def _serialize_state_representation(representation: BlackjackStateRepresentation) -> Dict:
        return {
            "player cards": EpisodeSerializer._serialize_cards(representation.player_cards),
            "opponent cards": EpisodeSerializer._serialize_cards(representation.opponent_cards),
            "current bet": representation.current_bet,
            "passed": representation.passed
        }

    @staticmethod
    def _serialize_cards(cards_counter: Counter[Card]):
        serialized_cards_list = []
        for card, quantity in cards_counter.items():
            serialized_cards_list.append({
                "card": card.name,
                "possible values": card.possible_values,
                "quantity": quantity
            })
        return serialized_cards_list
