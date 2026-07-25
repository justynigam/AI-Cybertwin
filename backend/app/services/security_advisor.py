import logging
from typing import List, Dict

class SecurityAdvisorPlaybook:
    def __init__(self):
        logging.info("AI Security Advisor initialized with standard enterprise playbooks.")

    def generate_recommendations(self, alert_context: dict) -> List[Dict]:
        """
        Takes the full context of an alert and outputs actionable recommendations.
        alert_context expects: { 'severity', 'attack_category', 'twin_predictions' }
        """
        severity = alert_context.get('severity', 'LOW')
        attack_category = alert_context.get('attack_category', 'Unknown')
        predictions = alert_context.get('twin_predictions', [])
        
        recommendations = []

        # 1. Base Actions based on Attack Classification
        if attack_category in ["Brute Force", "Credential Stuffing", "Impossible Travel"]:
            recommendations.append({
                "action_id": "FORCE_MFA",
                "title": "Force Re-Authentication (MFA)",
                "description": "Immediately invalidate active sessions and require MFA for the next login.",
                "automated": severity == "CRITICAL" # Auto-execute if critical
            })
            recommendations.append({
                "action_id": "DISABLE_ACCOUNT",
                "title": "Suspend User Account",
                "description": "Lock the account in Active Directory to stop further access.",
                "automated": False # Usually requires human approval
            })

        elif attack_category == "Lateral Movement":
            recommendations.append({
                "action_id": "ISOLATE_HOST",
                "title": "Network Isolate Device",
                "description": "Trigger EDR to quarantine the machine, blocking all traffic except to the SIEM.",
                "automated": True # Lateral movement is too fast for humans
            })

        elif attack_category == "Data Exfiltration":
            recommendations.append({
                "action_id": "BLOCK_IP",
                "title": "Block Destination IP",
                "description": "Update perimeter firewall to drop packets to the anomalous external IP.",
                "automated": True
            })

        # 2. Pre-Emptive Actions based on Behavioral Twin
        if predictions:
            top_prediction = predictions[0]['predicted_action']
            if "Database" in top_prediction or "Admin" in top_prediction:
                 recommendations.append({
                    "action_id": "DEPLOY_HONEYPOT",
                    "title": "Deploy Dynamic Honeypot",
                    "description": f"Spin up a decoy {top_prediction} resource to trap the attacker based on predicted trajectory.",
                    "automated": False
                })

        # 3. Fallback
        if not recommendations:
             recommendations.append({
                "action_id": "NOTIFY_SOC_LEAD",
                "title": "Escalate to Tier 3 SOC",
                "description": "Anomaly is highly complex. Requires immediate human forensic analysis.",
                "automated": True
            })

        return recommendations

    def execute_action(self, action_id: str, target_entity: str) -> dict:
        """
        Simulates executing the action against external APIs (AWS, Azure AD, CrowdStrike).
        """
        logging.info(f"Executing {action_id} against {target_entity}...")
        
        # In a real environment, you would use requests.post() to call external APIs here.
        # For the hackathon, we simulate a successful API response.
        
        return {
            "status": "success",
            "message": f"Successfully applied {action_id} to {target_entity}",
            "timestamp": "2026-07-25T22:43:22Z" # Current Context Time
        }
