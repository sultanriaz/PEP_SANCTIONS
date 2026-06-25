import  pathlib
import sys
import os
project_root = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))
from src.agent import PEPSanctionsScreeningAgent


def print_screening_report(result: dict):
    print("\n========== PEP + SANCTIONS SCREENING REPORT ==========\n")

    customer = result["customer"]

    print("Customer Information")
    print("--------------------")
    print(f"Name       : {customer.get('name')}")
    print(f"DOB        : {customer.get('dob')}")
    print(f"Country    : {customer.get('country')}")

    print("\nScreening Decision")
    print("------------------")
    print(f"Status     : {result.get('status')}")
    print(f"Risk Score : {result.get('risk_score')}")

    top_match = result.get("top_match")

    if top_match:
        print("\nTop Match")
        print("---------")
        print(f"Watchlist ID : {top_match.get('watchlist_id')}")
        print(f"Matched Name : {top_match.get('matched_name')}")
        print(f"Name Score   : {top_match.get('name_score')}")
        print(f"Risk Score   : {top_match.get('risk_score')}")
        print(f"Decision     : {top_match.get('decision')}")
        print(f"List Type    : {top_match.get('list_type')}")
        print(f"Source       : {top_match.get('source')}")

    print("\nTop Possible Matches")
    print("----------------------")

    matches = result.get("matches", [])[:15]

    if not matches:
        print("No matches found.")
    else:
        for index, match in enumerate(matches, start=1):
            print(f"\nMatch #{index}")
            print(f"ID          : {match.get('watchlist_id')}")
            print(f"Name        : {match.get('matched_name')}")
            print(f"Name Score  : {match.get('name_score')}")
            print(f"Risk Score  : {match.get('risk_score')}")
            print(f"Decision    : {match.get('decision')}")
            print(f"List Type   : {match.get('list_type')}")
            print(f"Source      : {match.get('source')}")

    print("\nExplanation")
    print("-----------")
    print(result.get("explanation"))

    print("\n=====================================================\n")


agent = PEPSanctionsScreeningAgent("data/watchlist.csv")

customer = {
    "name": "Sahar Khan",
    "dob": "1975-03-22",
    "country": "Pakistan"
}

result = agent.screen_customer(customer)

print_screening_report(result)