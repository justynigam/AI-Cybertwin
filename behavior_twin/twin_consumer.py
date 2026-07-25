"""
Twin Consumer worker for Behavioral Digital Twin microservice.
Listens for alerts and outputs future trajectory predictions for active threats.
"""
import logging
from behavior_twin.model.autoregressive import BehavioralAutoregressiveModel
from behavior_twin.model.token_mapper import TokenMapper
from behavior_twin.predictor import BehavioralTwinPredictor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class TwinAlertConsumer:
    """
    Consumes alerts and generates predictive next-move trajectories for SOC analysts.
    """

    def __init__(self, model: BehavioralAutoregressiveModel | None = None, token_mapper: TokenMapper | None = None):
        self.token_mapper = token_mapper if token_mapper is not None else TokenMapper()
        self.model = model if model is not None else BehavioralAutoregressiveModel(vocab_size=200)
        self.predictor = BehavioralTwinPredictor(model=self.model, vocab_mapper=self.token_mapper.id_to_token)

    def handle_alert(self, alert_event: dict, recent_action_tokens: list[str] | list[int], top_k: int = 3) -> dict:
        """
        Calculates projected attacker moves given an alert event and recent action history.
        """
        if recent_action_tokens and isinstance(recent_action_tokens[0], str):
            token_ids = self.token_mapper.text_sequence_to_ids(recent_action_tokens)
        else:
            token_ids = [int(t) for t in recent_action_tokens] if recent_action_tokens else [12, 55, 102]

        predicted_actions = self.predictor.predict_next_actions(token_ids, top_k=top_k)

        twin_response = {
            "alert_event_id": alert_event.get("event_id"),
            "user_id": alert_event.get("user_id", "unknown_user"),
            "current_severity": alert_event.get("severity", "HIGH"),
            "predicted_next_moves": predicted_actions
        }

        logging.info(f"Generated twin predictions for alert {alert_event.get('event_id')}: Top move={predicted_actions[0]['predicted_action']}")
        return twin_response


if __name__ == "__main__":
    consumer = TwinAlertConsumer()
    mock_alert = {"event_id": "evt-8899", "user_id": "usr-404", "severity": "CRITICAL"}
    predictions = consumer.handle_alert(mock_alert, recent_action_tokens=["LOGIN_SUCCESS", "Access_Shared_Drive", "Download_Large_File"])
    print("\n--- Twin Alert Consumer Output ---")
    print(predictions)
