from data_loader import load_matches
from team_model import calculate_team_strength
from poisson_model import match_probabilities

VALUE_THRESHOLD = 1.10

matches = load_matches()

total_bets = 0
wins = 0
losses = 0
profit = 0

print("\nRunning backtest...\n")
print("Value threshold:", VALUE_THRESHOLD)

# walk-forward loop
for i in range(200, len(matches)):

    train_data = matches.iloc[i-200:i]
    match = matches.iloc[i]

    home_attack, away_attack, home_defense, away_defense, league_home_avg, league_away_avg = calculate_team_strength(train_data)

    home_team = match["Home"]
    away_team = match["Away"]

    if (
    home_team not in home_attack.index
    or away_team not in away_attack.index
    or home_team not in home_defense.index
    or away_team not in away_defense.index
):
        continue

    expected_home_goals = home_attack[home_team] * away_defense[away_team] * league_home_avg
    expected_away_goals = away_attack[away_team] * home_defense[home_team] * league_away_avg

    home_win, draw, away_win, over25, under25, btts = match_probabilities(expected_home_goals, expected_away_goals)

    home_odds = match["PSCH"]
    draw_odds = match["PSCD"]
    away_odds = match["PSCA"]

    result = match["Res"]

    home_value = home_win * home_odds
    draw_value = draw * draw_odds
    away_value = away_win * away_odds

    # välj bästa value
best_value = max(home_value, draw_value, away_value)

print("Values:",
      round(home_value,3),
      round(draw_value,3),
      round(away_value,3),
      "best:", round(best_value,3))

bet_type = None
bet_odds = None

if best_value == home_value:
    bet_type = "H"
    bet_odds = home_odds

elif best_value == draw_value:
    bet_type = "D"
    bet_odds = draw_odds

else:
    bet_type = "A"
    bet_odds = away_odds


# bet only if value is above threshold
if best_value > VALUE_THRESHOLD:

    total_bets += 1

    if result == bet_type:
        wins += 1
        profit += bet_odds - 1
    else:
        losses += 1
        profit -= 1


print("\nBacktest results\n")

print("Total bets:", total_bets)
print("Wins:", wins)
print("Losses:", losses)

print("Profit:", round(profit,2), "units")

if total_bets > 0:
    roi = (profit / total_bets) * 100
    print("ROI:", round(roi,2), "%")

print("Bet frequency:", round(total_bets / len(matches), 3))