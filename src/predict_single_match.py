from data_loader import load_matches
from team_model import calculate_team_strength
from poisson_model import match_probabilities
from odds_api import get_live_odds, get_allsvenskan_matches


matches = load_matches()


# =========================
# NORMALIZE
# =========================
def normalize_team_name(name):
    return (
        name.lower()
        .replace("å", "a")
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("-", " ")
        .replace(".", "")
        .replace("ff", "")
        .replace("fk", "")
        .replace("if", "")
        .replace("bk", "")
        .strip()
    )


# =========================
# TEAM DATABASE
# =========================
teams = sorted(set(matches["Home"]).union(set(matches["Away"])))

team_lookup = {
    normalize_team_name(team): team
    for team in teams
}


# =========================
# SHOW LIVE MATCHES
# =========================
live_matches = get_allsvenskan_matches()

if not live_matches:
    print("No live/upcoming Allsvenskan matches found.")
    quit()

print("\nLIVE / UPCOMING ALLSVENSKAN MATCHES:\n")

for i, game in enumerate(live_matches, start=1):
    print(f"{i}. {game['home_team']} vs {game['away_team']}")

choice = int(input("\nSelect match number: ")) - 1

selected_match = live_matches[choice]

api_home = selected_match["home_team"]
api_away = selected_match["away_team"]


# =========================
# MATCH INTERNAL DB TEAM NAMES
# =========================
home_team = None
away_team = None

for team in teams:
    if normalize_team_name(team) in normalize_team_name(api_home):
        home_team = team
    if normalize_team_name(team) in normalize_team_name(api_away):
        away_team = team

if not home_team or not away_team:
    print("\nCould not map teams from API to database.")
    quit()


print("\nYou selected:")
print("Home:", home_team)
print("Away:", away_team)


# =========================
# TEAM STRENGTH
# =========================
(
    home_attack,
    away_attack,
    home_defense,
    away_defense,
    league_home_avg,
    league_away_avg
) = calculate_team_strength(matches)


# =========================
# EXPECTED GOALS
# =========================
expected_home_goals = (
    home_attack[home_team]
    * away_defense[away_team]
    * league_home_avg
)

expected_away_goals = (
    away_attack[away_team]
    * home_defense[home_team]
    * league_away_avg
)


print("\nExpected Goals:")
print("Home Goals:", round(expected_home_goals, 2))
print("Away Goals:", round(expected_away_goals, 2))


# =========================
# PROBABILITIES
# =========================
home_win, draw, away_win, over25, under25, btts = match_probabilities(
    expected_home_goals,
    expected_away_goals
)

print("\nMatch Probabilities:")
print("Home Win:", round(home_win * 100, 2), "%")
print("Draw:", round(draw * 100, 2), "%")
print("Away Win:", round(away_win * 100, 2), "%")

print("\nGoals Markets:")
print("Over 2.5:", round(over25 * 100, 2), "%")
print("Under 2.5:", round(under25 * 100, 2), "%")
print("BTTS:", round(btts * 100, 2), "%")


# =========================
# LIVE ODDS
# =========================
home_odds, draw_odds, away_odds = get_live_odds(api_home, api_away)

if home_odds is None:
    print("\nCould not find live odds.")
    quit()


print("\nMarket Odds:")
print("Home Odds:", home_odds)
print("Draw Odds:", draw_odds)
print("Away Odds:", away_odds)


# =========================
# VALUE
# =========================
home_value = home_win * home_odds
draw_value = draw * draw_odds
away_value = away_win * away_odds

print("\nValue Ratings:")
print("Home Value:", round(home_value, 3))
print("Draw Value:", round(draw_value, 3))
print("Away Value:", round(away_value, 3))


best_value = max(home_value, draw_value, away_value)

VALUE_THRESHOLD = 1.05


# =========================
# FINAL DECISION
# =========================
if best_value >= VALUE_THRESHOLD:

    print("\nPotential Value Bet Found!")

    if best_value == home_value:
        print("Best Bet: HOME WIN")

    elif best_value == draw_value:
        print("Best Bet: DRAW")

    else:
        print("Best Bet: AWAY WIN")

else:
    print("\nNo strong value bet.")