import joblib
import pandas as pd

# ==========================================
# LOAD MODEL AND DATA
# ==========================================

model = joblib.load("../models/world_cup_result_model.pkl")
feature_columns = joblib.load("../models/feature_columns.pkl")
elo_ratings = joblib.load("../models/elo_ratings.pkl")

df = pd.read_csv("../data/team_features.csv")
df["date"] = pd.to_datetime(df["date"])

# ==========================================
# GET LATEST TEAM STATISTICS
# ==========================================

def get_latest_team_stats(team):

    # Find all matches involving this team
    matches = df[
        (df["home_team"] == team) |
        (df["away_team"] == team)
    ]

    if matches.empty:
        return None

    # Latest available match
    latest = matches.sort_values("date").iloc[-1]

    if latest["home_team"] == team:

        return {
            "win_rate": latest["home_win_rate"],
            "draw_rate": latest["home_draw_rate"],
            "loss_rate": latest["home_loss_rate"],
            "avg_goals_for": latest["home_avg_goals_for"],
            "avg_goals_against": latest["home_avg_goals_against"],
            "recent_form": latest["home_recent_form"],
            "elo": elo_ratings.get(team, 1500)
        }

    else:

        return {
            "win_rate": latest["away_win_rate"],
            "draw_rate": latest["away_draw_rate"],
            "loss_rate": latest["away_loss_rate"],
            "avg_goals_for": latest["away_avg_goals_for"],
            "avg_goals_against": latest["away_avg_goals_against"],
            "recent_form": latest["away_recent_form"],
            "elo": elo_ratings.get(team, 1500)
        }


# ==========================================
# PREDICT MATCH
# ==========================================

def predict_match(home_team, away_team):

    home_stats = get_latest_team_stats(home_team)
    away_stats = get_latest_team_stats(away_team)

    if home_stats is None:
        print(f"\nTeam not found: {home_team}")
        return

    if away_stats is None:
        print(f"\nTeam not found: {away_team}")
        return

    elo_difference = home_stats["elo"] - away_stats["elo"]

    # Build model input
    match_data = {

        "home_win_rate": home_stats["win_rate"],
        "away_win_rate": away_stats["win_rate"],

        "home_draw_rate": home_stats["draw_rate"],
        "away_draw_rate": away_stats["draw_rate"],

        "home_loss_rate": home_stats["loss_rate"],
        "away_loss_rate": away_stats["loss_rate"],

        "home_avg_goals_for": home_stats["avg_goals_for"],
        "away_avg_goals_for": away_stats["avg_goals_for"],

        "home_avg_goals_against": home_stats["avg_goals_against"],
        "away_avg_goals_against": away_stats["avg_goals_against"],

        "home_recent_form": home_stats["recent_form"],
        "away_recent_form": away_stats["recent_form"],

        "home_elo": home_stats["elo"],
        "away_elo": away_stats["elo"],

        "elo_difference": elo_difference
    }

    X = pd.DataFrame([match_data])[feature_columns]

    # Prediction
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    probability_map = dict(
        zip(model.classes_, probabilities)
    )

    # ======================================
    # DISPLAY RESULT
    # ======================================

    print("\n========================================")
    print("        WORLD CUP AI PREDICTION")
    print("========================================")

    print(f"\n{home_team} vs {away_team}")

    print("\nWin probabilities:")

    print(
        f"{home_team} Win : "
        f"{probability_map.get('H', 0) * 100:.2f}%"
    )

    print(
        f"Draw         : "
        f"{probability_map.get('D', 0) * 100:.2f}%"
    )

    print(
        f"{away_team} Win : "
        f"{probability_map.get('A', 0) * 100:.2f}%"
    )

    print("\nPredicted Result:")

    if prediction == "H":
        print(f"{home_team} Win")

    elif prediction == "A":
        print(f"{away_team} Win")

    else:
        print("Draw")

    print("\nTeam Ratings:")
    print(f"{home_team} Elo: {home_stats['elo']:.0f}")
    print(f"{away_team} Elo: {away_stats['elo']:.0f}")

    print("\n========================================")


# ==========================================
# INTERACTIVE INPUT
# ==========================================

print("========================================")
print("      WORLD CUP AI MATCH PREDICTOR")
print("========================================")

print("\nEnter team names exactly as they appear")
print("in the dataset.\n")

home_team = input("Home Team: ").strip()
away_team = input("Away Team: ").strip()

predict_match(home_team, away_team)