import pandas as pd
import numpy as np

def calculate_team_strength(matches):

    matches = matches.copy()

    # skapa vikter (senaste matcher väger mer)
    matches["weight"] = np.linspace(0.5, 1.0, len(matches))

    league_home_avg = np.average(matches["HG"], weights=matches["weight"])
    league_away_avg = np.average(matches["AG"], weights=matches["weight"])

    # weighted home attack
    home_attack = matches.groupby("Home").apply(
        lambda x: np.average(x["HG"], weights=x["weight"])
    ) / league_home_avg

    # weighted away attack
    away_attack = matches.groupby("Away").apply(
        lambda x: np.average(x["AG"], weights=x["weight"])
    ) / league_away_avg

    # weighted home defence
    home_defense = matches.groupby("Home").apply(
        lambda x: np.average(x["AG"], weights=x["weight"])
    ) / league_away_avg

    # weighted away defence
    away_defense = matches.groupby("Away").apply(
        lambda x: np.average(x["HG"], weights=x["weight"])
    ) / league_home_avg

    return (
        home_attack,
        away_attack,
        home_defense,
        away_defense,
        league_home_avg,
        league_away_avg
    )