"""
Graph Builder module for CyberTwin AI.
Manages graph topology state, centralities calculation, and memory-safe streaming updates.
"""
from datetime import datetime, timedelta
import logging
import networkx as nx
from graph_engine.lateral_movement import CyberGraphEngine


class StreamingGraphManager:
    """
    State manager wrapping CyberGraphEngine with degree centrality tracking,
    batch event processing, and memory pruning.
    """

    def __init__(self, engine: CyberGraphEngine | None = None, retention_days: int = 30):
        self.engine = engine if engine is not None else CyberGraphEngine()
        self.retention_days = retention_days
        self.total_events_processed = 0

    def ingest_event(self, event: dict) -> float:
        """
        Ingests a raw telemetry event dict (e.g. from events.json or Redis stream),
        updates graph state, and computes lateral movement risk score.
        """
        user_id = str(event.get("user_id", "unknown_user"))
        # Use target resource, device, or geo_location as target node
        resource_id = str(event.get("device_id") or event.get("ip_address") or event.get("geo_location") or "unknown_resource")
        
        timestamp_raw = event.get("timestamp")
        if isinstance(timestamp_raw, str):
            event_time = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
        elif isinstance(timestamp_raw, datetime):
            event_time = timestamp_raw
        else:
            event_time = datetime.utcnow()

        event_type = str(event.get("event_type", "AUTHENTICATION"))

        # 1. Evaluate risk BEFORE adding edge to test current topological hop distance
        risk_score = self.engine.evaluate_lateral_movement_risk(user_id, resource_id)

        # 2. Add event to graph
        self.engine.add_event(user_id, resource_id, event_time, event_type)
        self.total_events_processed += 1

        return risk_score

    def get_high_degree_nodes(self, top_k: int = 10) -> list[tuple[str, int]]:
        """
        Calculates node degree centrality spikes (potential worm/ransomware spread).
        """
        degrees = dict(self.engine.G.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda item: item[1], reverse=True)
        return sorted_nodes[:top_k]

    def prune_old_edges(self, reference_time: datetime | None = None):
        """Removes edges older than retention_days relative to reference_time."""
        if reference_time is None:
            reference_time = datetime.utcnow()
        cutoff_time = reference_time - timedelta(days=self.retention_days)
        self.engine.prune_stale_edges(cutoff_time)
