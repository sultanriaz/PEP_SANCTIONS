import pandas as pd
import sys
import os
import pathlib
project_root = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))
from src.matcher import find_matches
from src.scorer import calculate_risk_score


class PEPSanctionsScreeningAgent:
    def __init__(self, watchlist_path: str):
        self.watchlist_df = pd.read_csv(watchlist_path)

    def screen_customer(self, customer: dict) -> dict:
        matches = find_matches(customer["name"], self.watchlist_df)

        if not matches:
            return {
                "customer": customer,
                "status": "No Match",
                "risk_score": 0,
                "matches": [],
                "explanation": "No sufficiently similar watchlist record was found."
            }

        scored_matches = [
            calculate_risk_score(customer, match)
            for match in matches
        ]

        top_match = max(scored_matches, key=lambda x: x["risk_score"])

        return {
            "customer": customer,
            "status": top_match["decision"],
            "risk_score": top_match["risk_score"],
            "top_match": top_match,
            "matches": scored_matches,
            "explanation": self.generate_explanation(customer, top_match)
        }

    def generate_explanation(self, customer: dict, match: dict) -> str:
        return (
            f"Customer '{customer['name']}' matched with watchlist record "
            f"'{match['matched_name']}' from {match['source']} list. "
            f"Name similarity score is {match['name_score']}. "
            f"Final risk score is {match['risk_score']}. "
            f"Decision: {match['decision']}."
        )