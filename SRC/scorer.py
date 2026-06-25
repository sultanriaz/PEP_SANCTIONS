

def dob_score(input_dob, watchlist_dob):
    # If either date is missing or "nan", no match
    if not input_dob or not watchlist_dob or str(watchlist_dob) == "nan":
        return 0

    # If the dates are exactly the same (as strings), give 20 points
    if str(input_dob) == str(watchlist_dob):
        return 20
    else:
        return 0


def country_score(input_country, watchlist_country):
    # If either country is missing, no match
    if not input_country or not watchlist_country:
        return 0

    # If countries are the same (ignoring case), give 10 points
    if input_country.lower() == str(watchlist_country).lower():
        return 10
    else:
        return 0


def list_type_score(list_type):
    # Convert to string and lowercase
    list_type = str(list_type).lower()

    # Higher risk types get more points
    if list_type == "sanctions":
        return 20
    if list_type == "pep":
        return 15
    if list_type == "adverse media":
        return 10

    # Any other list type (Watchlist, HRI, etc.) gets a base of 5
    return 5


def calculate_risk_score(customer, match):
    # Name component: 50% of the fuzzy name score
    name_component = match["name_score"] * 0.5

    # Date of birth component: 20 points if they match
    dob_component = dob_score(customer.get("dob"), match.get("dob"))

    # Country component: 10 points if they match
    country_component = country_score(customer.get("country"), match.get("country"))

    # List type component: points based on how serious the list is
    list_component = list_type_score(match.get("list_type"))

    # Add everything up and round to 2 decimals
    total_score = name_component + dob_component + country_component + list_component
    total_score = round(total_score, 2)

    # Make a decision based on the total risk score
    if total_score >= 85:
        decision = "High-Risk Match"
    elif total_score >= 65:
        decision = "Possible Match"
    else:
        decision = "Low-Risk / Review"

    # Return a dictionary with the final result
    return {
        "watchlist_id": match["id"],
        "matched_name": match["matched_name"],
        "name_score": match["name_score"],
        "risk_score": total_score,
        "decision": decision,
        "list_type": match["list_type"],
        "source": match["source"]
    }