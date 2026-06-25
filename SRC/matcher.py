import pandas as pd
import sys
import pathlib
project_root = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))
from rapidfuzz import fuzz
from src.data_normalizer import normalize_name, split_aliases


def calculate_name_score(input_name, watchlist_name):
    # Clean both names
    clean_input = normalize_name(input_name)
    clean_watchlist = normalize_name(watchlist_name)
    # Calculate two different fuzzy matching scores
    token_score = fuzz.token_sort_ratio(clean_input, clean_watchlist)
    partial_score = fuzz.partial_ratio(clean_input, clean_watchlist)
    # Combine the two scores with weights
    combined = (token_score * 0.7) + (partial_score * 0.3)
    # Round to 2 decimal places and return
    return round(combined, 2)


def find_matches(input_name, watchlist_df, threshold=75):
    matches = []
    # Loop through every row in the watchlist DataFrame
    for index, row in watchlist_df.iterrows():
        # Score against the main full_name
        main_score = calculate_name_score(input_name, row["full_name"])

        # Get the aliases for this row and score each one
        alias_scores = []
        alias_text = row.get("aliases", "")
        aliases = split_aliases(alias_text)

        for alias in aliases:
            score = calculate_name_score(input_name, alias)
            alias_scores.append(score)

        # Choose the best alias score, or 0 if there are no aliases
        if alias_scores:
            best_alias_score = max(alias_scores)
        else:
            best_alias_score = 0

        # The final score for this row is the better of main_score and best_alias_score
        best_score = max(main_score, best_alias_score)

        # If the score meets the threshold, add the match to the results
        if best_score >= threshold:
            match = {
                "id": row["id"],
                "matched_name": row["full_name"],
                "list_type": row["list_type"],
                "source": row["source"],
                "country": row["country"],
                "dob": row["dob"],
                "entity_type": row["entity_type"],
                "name_score": best_score
            }
            matches.append(match)

    # Sort results by name_score, highest first
    matches_sorted = sorted(matches, key=lambda x: x["name_score"], reverse=True)

    return matches_sorted