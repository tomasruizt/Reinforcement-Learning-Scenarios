from typing import Dict

from rl.episode import DiscreteEpisode

from scenario.blackjack.state import BlackjackState


class EpisodeSerializer:

    def __init__(self, episode: DiscreteEpisode):
        self._episode = episode

    def to_json(self) -> Dict:
        start_state = self._serialize_state(self._episode.start_state)
        end_state = self._serialize_state(self._episode.end_state)
        return {
            "episode": {
                "startState": start_state,
                "actionChosen": self._episode.agent_action.name,
                "reward": self._episode.reward,
                "endState": end_state
            }
        }

    def to_human_friendly_json(self) -> Dict:
        players_initial_score = self._episode.start_state.player_hand.score
        players_next_score = self._episode.end_state.player_hand.score
        friendly_json = {
            "playersInitialScore": players_initial_score,
            "actionChosen": self._episode.agent_action.name,
            "reward": self._episode.reward,
            "playersNextScore": players_next_score,
            "dealersScore": self._episode.end_state.dealer_hand.score
        }
        return friendly_json

    @staticmethod
    def _serialize_state(state: BlackjackState) -> Dict:
        player_hand = state.player_hand
        dealer_hand = state.dealer_hand
        return {
            "playersHand": {
                "cards": player_hand.card_names,
                "correspondingQuantities": player_hand.quantities,
                "score": player_hand.score
            },
            "dealersHand": {
                "cards": dealer_hand.card_names,
                "correspondingQuantities": dealer_hand.quantities,
                "score": dealer_hand.score
            },
            "currentBet": state.current_bet,
            "passed": state.player_has_passed,
            # action space is constant: draw or pass
            # "action space": episode.start_state.action_space,
        }
