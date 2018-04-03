from typing import Dict

from rl.experience_tuple import ExperienceTupleSerializer, ExperienceTuple

from scenario.blackjack.state import BlackjackState


class BlackjackExperienceTupleSerializer(ExperienceTupleSerializer):
    """
    A specific implementation of the ExperienceTupleSerializer for the
    Blackjack scenario.
    """

    def serialize(self, experience_tuple: ExperienceTuple) -> Dict:
        start_state = self._serialize_state(experience_tuple.start_state)
        end_state = self._serialize_state(experience_tuple.end_state)
        return {
            "episode": {
                "startState": start_state,
                "actionChosen": experience_tuple.agent_action.name,
                "reward": experience_tuple.reward,
                "endState": end_state
            }
        }

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


class HumanFriendlyBlackjackExperienceTupleSerializer(
        BlackjackExperienceTupleSerializer):
    """
    A subclass of the ExperienceTupleSerializer for the Blackjack
    scenario, where the result is friendly for human readers.
    """

    def serialize(self, experience_tuple: ExperienceTuple) -> Dict:
        players_initial_score = experience_tuple.start_state.player_hand.score
        players_next_score = experience_tuple.end_state.player_hand.score
        friendly_json = {
            "playersInitialScore": players_initial_score,
            "actionChosen": experience_tuple.agent_action.name,
            "reward": experience_tuple.reward,
            "playersNextScore": players_next_score,
            "dealersScore": experience_tuple.end_state.dealer_hand.score
        }
        return friendly_json
