from scipy.stats import poisson

def match_probabilities(expected_home_goals, expected_away_goals):

    home_win = 0
    draw = 0
    away_win = 0
    over25 = 0
    under25 = 0
    btts = 0

    for home_goals in range(6):
        for away_goals in range(6):

            prob = poisson.pmf(home_goals, expected_home_goals) * poisson.pmf(away_goals, expected_away_goals)

            # 1X2
            if home_goals > away_goals:
                home_win += prob
            elif home_goals == away_goals:
                draw += prob
            else:
                away_win += prob

            # over / under 2.5
            if home_goals + away_goals >= 3:
                over25 += prob
            else:
                under25 += prob

            # BTTS
            if home_goals > 0 and away_goals > 0:
                btts += prob

    return home_win, draw, away_win, over25, under25, btts