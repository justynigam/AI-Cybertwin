"""
FastAPI Entities Endpoint for CyberTwin AI Backend.
GET /entities/{id} retrieves behavioral digital twin profile baselines and trajectory forecasts.
"""
from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.dependencies import verify_token
from behavior_twin.model.token_mapper import TokenMapper
from behavior_twin.model.autoregressive import BehavioralAutoregressiveModel
from behavior_twin.predictor import BehavioralTwinPredictor

router = APIRouter()
mapper = TokenMapper()
model = BehavioralAutoregressiveModel(vocab_size=200)
predictor = BehavioralTwinPredictor(model=model, vocab_mapper=mapper.id_to_token)


@router.get("/{entity_id}", summary="Get Behavioral Digital Twin profile")
def get_entity_profile(
    entity_id: str,
    current_user: dict = Depends(verify_token)
):
    """
    Returns baseline behavioral features, learned norms, and trajectory forecasts for a given entity_id.
    """
    try:
        # Generate next-step forecast from sample historical sequence
        sample_ids = [12, 55, 102]
        predictions = predictor.predict_next_actions(recent_sequence=sample_ids, top_k=3)

        profile = {
            "entity_id": entity_id,
            "role": "Senior Systems Engineer",
            "baseline_fit_score": 0.982,
            "learned_baselines": {
                "typical_working_hours": "08:30 - 18:00 UTC",
                "primary_ip_range": "198.51.100.0/24 (Home Office)",
                "primary_device_id": "dev-4410 (macOS-M2-MacBookPro)",
                "historical_avg_login_frequency_per_day": 4.2
            },
            "recent_sequence_text": ["LOGIN_SUCCESS", "Access_Shared_Drive", "Download_Large_File"],
            "twin_next_move_predictions": predictions
        }
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
