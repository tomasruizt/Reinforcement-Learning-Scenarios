from typing import Dict

from rl.episode import DiscreteEpisode

from scenario.blackjack.state import BlackjackState


class EpisodeSerializer:

    def to_json(self, episode: DiscreteEpisode):
        return {
            "episode": {
                "start state": self._serialize_state(episode.start_state),
                "action chosen": episode.agent_action.name,
                "reward": episode.reward,
                "end state": self._serialize_state(episode.end_state)
            }
        }

    @staticmethod
    def _serialize_state(state: BlackjackState) -> Dict:
        player_hand = state.player_hand
        opponent_hand = state.dealer_hand
        return {
            "player hand": {
                "cards": player_hand.card_names,
                "corresponding quantities": player_hand.quantities,
                "score": player_hand.score
            },
            "opponent hand": {
                "cards": opponent_hand.card_names,
                "corresponding quantities": opponent_hand.quantities,
                "score": opponent_hand.score
            },
            "current bet": state.current_bet,
            "passed": state.player_has_passed,
            # action space is constant: draw or pass
            # "action space": episode.start_state.action_space,
        }
