"""
Event consumer for CyberTwin AI Graph Engine.
Streams events from raw json or stream channels and evaluates real-time topological risks.
"""
import os
import json
import logging
from datetime import datetime
from graph_engine.graph_builder import StreamingGraphManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class GraphEventConsumer:
    """
    Consumes security events and updates NetworkX topological state in real-time.
    """

    def __init__(self, manager: StreamingGraphManager | None = None):
        self.manager = manager if manager is not None else StreamingGraphManager()

    def process_event_stream(self, events: list[dict]) -> list[dict]:
        """
        Processes a list of event dictionaries, computing lateral movement risk for each.
        """
        results = []
        for event in events:
            risk = self.manager.ingest_event(event)
            event_result = {
                "event_id": event.get("event_id"),
                "user_id": event.get("user_id"),
                "device_id": event.get("device_id"),
                "lateral_movement_risk": risk,
                "is_attack": event.get("is_attack", False)
            }
            results.append(event_result)
        return results

    def consume_json_file(self, json_path: str) -> list[dict]:
        """Reads line-delimited JSON events file and processes stream."""
        logging.info(f"Consuming events from: {json_path}")
        events = []
        with open(json_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))

        results = self.process_event_stream(events)
        logging.info(f"Processed {len(results)} events through Graph Engine.")
        return results


if __name__ == "__main__":
    import sys
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    events_file = os.path.join(project_root, "ml", "data", "raw", "events.json")

    if os.path.exists(events_file):
        consumer = GraphEventConsumer()
        results = consumer.consume_json_file(events_file)
        high_risk_events = [r for r in results if r["lateral_movement_risk"] > 0.7]
        print(f"\n--- Graph Engine Audit Summary ---")
        print(f"Total events analyzed: {len(results)}")
        print(f"High Lateral Movement Risk alerts (> 0.7): {len(high_risk_events)}")
        if high_risk_events:
            print("Sample Alert:", high_risk_events[0])
