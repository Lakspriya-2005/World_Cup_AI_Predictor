import joblib
import numpy as np

# Load models
goal_models = joblib.load("../models/goal_models.pkl")

home_mean = goal_models["home_mean"]
away_mean = goal_models["away_mean"]


def predict_score(home_team, away_team):
    print("\n" + "=" * 45)
    print("        ⚽ SCORE PREDICTION")
    print("=" * 45)

    print(f"\n{home_team} vs {away_team}")

    # Baseline expected goals
    home_goals = home_mean
    away_goals = away_mean

    # Most likely integer score
    predicted_home = round(home_goals)
    predicted_away = round(away_goals)

    print(f"\nExpected {home_team} Goals: {home_goals:.2f}")
    print(f"Expected {away_team} Goals: {away_goals:.2f}")

    print(
        f"\nPredicted Score: "
        f"{home_team} {predicted_home} - "
        f"{predicted_away} {away_team}"
    )

    # Result based on predicted score
    if predicted_home > predicted_away:
        result = f"{home_team} Win"
    elif predicted_home < predicted_away:
        result = f"{away_team} Win"
    else:
        result = "Draw"

    print(f"Predicted Result: {result}")
    print("=" * 45)


# Interactive input
home_team = input("Enter Home Team: ")
away_team = input("Enter Away Team: ")

predict_score(home_team, away_team)