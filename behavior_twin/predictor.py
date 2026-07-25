import torch
import torch.nn.functional as F
import logging
from typing import List, Dict

class BehavioralTwinPredictor:
    def __init__(self, model, vocab_mapper):
        """
        model: Trained PyTorch autoregressive model (LSTM or causal Transformer).
        vocab_mapper: Dictionary converting action IDs back to human-readable strings.
        """
        self.model = model
        self.vocab_mapper = vocab_mapper # e.g., {45: 'Access HR_Database', 89: 'Execute PowerShell'}
        self.model.eval()
        logging.info("Behavioral Twin Predictive Engine Initialized.")

    def predict_next_actions(self, recent_sequence: List[int], top_k: int = 3) -> List[Dict]:
        """
        Given a sequence of recent action IDs, predicts the most likely next steps.
        """
        # Convert sequence to tensor: Shape [1, Sequence_Length]
        sequence_tensor = torch.tensor([recent_sequence], dtype=torch.long)
        
        with torch.no_grad():
            # Forward pass: get logits for the next step
            # Model output shape: [Batch, Sequence_Length, Vocab_Size]
            logits = self.model(sequence_tensor)
            
            # We only care about the prediction for the very last step in the sequence
            next_step_logits = logits[0, -1, :]
            
            # Convert logits to probabilities
            probabilities = F.softmax(next_step_logits, dim=-1)
            
            # Extract the Top-K most probable next actions
            top_probs, top_indices = torch.topk(probabilities, top_k)
            
        predictions = []
        for i in range(top_k):
            action_id = top_indices[i].item()
            confidence = top_probs[i].item()
            
            # Map back to English, fallback to 'Unknown Action' if not found
            action_name = self.vocab_mapper.get(action_id, f"Unknown_Action_{action_id}")
            
            predictions.append({
                "predicted_action": action_name,
                "probability_score": round(confidence, 4),
                "rank": i + 1
            })
            
        return predictions

# --- Usage Example ---
if __name__ == "__main__":
    from behavior_twin.model.autoregressive import BehavioralAutoregressiveModel
    from behavior_twin.model.token_mapper import TokenMapper

    mapper = TokenMapper()
    model = BehavioralAutoregressiveModel(vocab_size=200)

    twin = BehavioralTwinPredictor(model=model, vocab_mapper=mapper.id_to_token)
    next_moves = twin.predict_next_actions(recent_sequence=[12, 55, 102])
    print("\n--- Behavioral Twin Predicted Next Actions ---")
    print(next_moves)
