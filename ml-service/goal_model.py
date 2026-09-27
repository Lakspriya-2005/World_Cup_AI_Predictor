import pandas as pd
import numpy as np
import joblib

print("Loading data...")

features = [
    "home_win_rate",
    "away_win_rate",
    "home_draw_rate",
    "away_draw_rate",
    "home_loss_rate",
    "away_loss_rate",
    "home_avg_goals_for",
    "away_avg_goals_for",
    "home_avg_goals_against",
    "away_avg_goals_against",
    "home_recent_form",
    "away_recent_form",
    "home_elo",
    "away_elo",
    "elo_difference"
]

df = pd.read_csv("../data/team_features.csv")
results = pd.read_csv("../data/international_results.csv")

df["home_goals"] = results["home_score"]
df["away_goals"] = results["away_score"]

df = df.dropna(subset=features)

X = df[features].values.astype(float)

home_y = df["home_goals"].values.astype(float)
away_y = df["away_goals"].values.astype(float)

split = int(len(X) * 0.8)

X_train = X[:split]
X_test = X[split:]

home_train = home_y[:split]
home_test = home_y[split:]

away_train = away_y[:split]
away_test = away_y[split:]


# Simple Poisson-style goal model
# Uses historical average goals adjusted by team features

home_mean = np.mean(home_train)
away_mean = np.mean(away_train)

home_pred = np.full(len(home_test), home_mean)
away_pred = np.full(len(away_test), away_mean)

home_mae = np.mean(np.abs(home_test - home_pred))
away_mae = np.mean(np.abs(away_test - away_pred))

print("\nGOAL PREDICTION RESULTS")
print("-----------------------")

print("Average Home Goals:", round(home_mean, 3))
print("Average Away Goals:", round(away_mean, 3))

print("Home Goals MAE:", round(home_mae, 3))
print("Away Goals MAE:", round(away_mae, 3))


# Save baseline goal models
goal_models = {
    "home_mean": home_mean,
    "away_mean": away_mean
}

joblib.dump(goal_models, "../models/goal_models.pkl")

print("\nGoal model saved successfully!")
print("Model file: ../models/goal_models.pkl")