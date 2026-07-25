"""
Behavioral Digital Twin microservice for CyberTwin AI.
Forecasts future attacker steps using autoregressive neural sequence modeling.
"""
from .predictor import BehavioralTwinPredictor
from .twin_consumer import TwinAlertConsumer

__all__ = ["BehavioralTwinPredictor", "TwinAlertConsumer"]
