import networkx as nx
from datetime import datetime
import logging

class CyberGraphEngine:
    def __init__(self):
        # Directed graph because User -> accesses -> Server is directional
        self.G = nx.DiGraph()
        logging.info("Initialized In-Memory Graph Engine")

    def add_event(self, user_id: str, resource_id: str, event_time: datetime, event_type: str):
        """
        Updates the graph with a new event. If nodes don't exist, they are created.
        """
        # Ensure nodes exist with types
        if not self.G.has_node(user_id):
            self.G.add_node(user_id, type='USER')
        if not self.G.has_node(resource_id):
            self.G.add_node(resource_id, type='RESOURCE')

        # Add or update edge
        if self.G.has_edge(user_id, resource_id):
            # Increase weight if relationship already exists
            self.G[user_id][resource_id]['weight'] += 1
            self.G[user_id][resource_id]['last_seen'] = event_time
        else:
            # Create new edge
            self.G.add_edge(user_id, resource_id, weight=1, first_seen=event_time, last_seen=event_time, type=event_type)

    def evaluate_lateral_movement_risk(self, user_id: str, target_resource: str) -> float:
        """
        Determines the structural risk of a user accessing a specific resource.
        Returns a risk score between 0.0 and 1.0.
        """
        if not self.G.has_node(user_id) or not self.G.has_node(target_resource):
            # First time user or resource seen in the graph -> Moderate risk (Cold Start)
            return 0.5 

        if self.G.has_edge(user_id, target_resource):
            # User accesses this regularly -> Low risk
            weight = self.G[user_id][target_resource]['weight']
            if weight > 5:
                return 0.05
            return 0.2

        # --- LATERAL MOVEMENT HEURISTICS ---
        
        # 1. Shortest Path Assessment
        # If the user has never accessed it, how "far" is it from their normal behavior?
        try:
            # We use an undirected version to see if they are in the same network community
            undirected_G = self.G.to_undirected()
            path_length = nx.shortest_path_length(undirected_G, source=user_id, target=target_resource)
            
            if path_length >= 3:
                # E.g., User -> Server A -> User B -> Target Resource
                # Highly suspicious hop distance.
                return 0.85
            elif path_length == 2:
                # E.g., User -> Department Server -> Target Resource
                return 0.60
                
        except nx.NetworkXNoPath:
            # The resource is in a completely disconnected component of the graph.
            # An attacker jumping to a hidden segment. Max Risk.
            return 0.95

        return 0.3 # Default fallback

    def prune_stale_edges(self, cutoff_time: datetime):
        """
        Prevents memory leaks by removing old historical connections.
        """
        edges_to_remove = []
        for u, v, data in self.G.edges(data=True):
            if data['last_seen'] < cutoff_time:
                edges_to_remove.append((u, v))
        
        self.G.remove_edges_from(edges_to_remove)
        logging.info(f"Pruned {len(edges_to_remove)} stale edges.")
