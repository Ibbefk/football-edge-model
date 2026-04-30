import requests

API_KEY = "c14e0300dcb5d2628397991be537a344"

SPORT = "soccer_sweden_allsvenskan"
REGIONS = "eu"
MARKETS = "h2h"


# =========================
# GET ALL LIVE / UPCOMING MATCHES
# =========================
def get_allsvenskan_matches():

    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": "decimal"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return []

    return response.json()


# =========================
# NORMALIZE TEAM NAMES
# =========================
def normalize_name(name):

    return (
        name.lower()
        .replace("å", "a")
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("if", "")
        .replace("ff", "")
        .replace("fk", "")
        .replace("bk", "")
        .replace("-", " ")
        .replace(".", "")
        .strip()
    )


# =========================
# GET BEST LIVE ODDS
# =========================
def get_live_odds(home_team, away_team):

    matches = get_allsvenskan_matches()

    target_home = normalize_name(home_team)
    target_away = normalize_name(away_team)

    for match in matches:

        api_home = normalize_name(match["home_team"])
        api_away = normalize_name(match["away_team"])

        if target_home in api_home and target_away in api_away:

            best_home_odds = 0
            best_draw_odds = 0
            best_away_odds = 0

            bookmakers = match.get("bookmakers", [])

            for bookmaker in bookmakers:

                markets = bookmaker.get("markets", [])

                for market in markets:

                    if market["key"] != "h2h":
                        continue

                    outcomes = market.get("outcomes", [])

                    for outcome in outcomes:

                        outcome_name = normalize_name(outcome["name"])
                        price = outcome["price"]

                        # Home
                        if outcome_name == api_home:
                            if price > best_home_odds:
                                best_home_odds = price

                        # Away
                        elif outcome_name == api_away:
                            if price > best_away_odds:
                                best_away_odds = price

                        # Draw
                        elif outcome["name"].lower() == "draw":
                            if price > best_draw_odds:
                                best_draw_odds = price

            return best_home_odds, best_draw_odds, best_away_odds

    print("\nMatch not found in live odds.")
    return None, None, None