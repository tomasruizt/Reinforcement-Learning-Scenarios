from typing import Dict

from rl.episode import DiscreteEpisode

from scenario.blackjack.state import BlackjackState


class EpisodeSerializer:

    def to_json(self, episode: DiscreteEpisode) -> Dict:
        return {
            "episode": {
                "start state": self._serialize_state(episode.start_state),
                "action chosen": episode.agent_action.name,
                "reward": episode.reward,
                "end state": self._serialize_state(episode.end_state)
            }
        }

    def to_human_friendly_json(self, episode: DiscreteEpisode) -> Dict:
        data = self.to_json(episode)["episode"]
        friendly_json = {
            "initial player score": str(data["start state"]["player hand"][
                "score"]),
            "action chosen": str(data["action chosen"]),
            "reward": str(data["reward"]),
            "next player score": str(data["end state"]["player hand"]["score"]),
            "dealer score": str(data["end state"]["opponent hand"]["score"])
        }
        return friendly_json

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
