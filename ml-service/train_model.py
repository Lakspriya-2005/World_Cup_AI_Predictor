import pandas as pd
from collections import defaultdict, deque
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("../data/processed_matches.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# ==========================================
# 2. TEAM STATISTICS
# ==========================================

team_stats = defaultdict(lambda: {
    "matches": 0,
    "wins": 0,
    "draws": 0,
    "losses": 0,
    "goals_for": 0,
    "goals_against": 0,
    "recent_results": deque(maxlen=5)
})

# Elo ratings
elo_ratings = defaultdict(lambda: 1500.0)

K_FACTOR = 20


def get_team_features(team):

    stats = team_stats[team]

    if stats["matches"] == 0:
        return {
            "win_rate": 0.0,
            "draw_rate": 0.0,
            "loss_rate": 0.0,
            "avg_goals_for": 0.0,
            "avg_goals_against": 0.0,
            "recent_form": 0.0
        }

    matches = stats["matches"]

    return {
        "win_rate": stats["wins"] / matches,
        "draw_rate": stats["draws"] / matches,
        "loss_rate": stats["losses"] / matches,
        "avg_goals_for": stats["goals_for"] / matches,
        "avg_goals_against": stats["goals_against"] / matches,
        "recent_form": sum(stats["recent_results"]) / 15
    }


def expected_result(home_rating, away_rating):

    return 1 / (1 + 10 ** ((away_rating - home_rating) / 400))


# ==========================================
# 3. FEATURE ENGINEERING
# ==========================================

feature_rows = []

print("Creating advanced team features...")

for _, row in df.iterrows():

    home_team = row["home_team"]
    away_team = row["away_team"]

    # --------------------------------------
    # Features BEFORE current match
    # --------------------------------------

    home_features = get_team_features(home_team)
    away_features = get_team_features(away_team)

    home_elo = elo_ratings[home_team]
    away_elo = elo_ratings[away_team]

    elo_difference = home_elo - away_elo

    feature_rows.append({

        "date": row["date"],

        "home_team": home_team,
        "away_team": away_team,

        "home_win_rate": home_features["win_rate"],
        "away_win_rate": away_features["win_rate"],

        "home_draw_rate": home_features["draw_rate"],
        "away_draw_rate": away_features["draw_rate"],

        "home_loss_rate": home_features["loss_rate"],
        "away_loss_rate": away_features["loss_rate"],

        "home_avg_goals_for": home_features["avg_goals_for"],
        "away_avg_goals_for": away_features["avg_goals_for"],

        "home_avg_goals_against": home_features["avg_goals_against"],
        "away_avg_goals_against": away_features["avg_goals_against"],

        "home_recent_form": home_features["recent_form"],
        "away_recent_form": away_features["recent_form"],

        "home_elo": home_elo,
        "away_elo": away_elo,

        "elo_difference": elo_difference,

        "result": row["result"]
    })

    # --------------------------------------
    # UPDATE TEAM STATISTICS
    # --------------------------------------

    home_goals = row["home_score"]
    away_goals = row["away_score"]

    home_stats = team_stats[home_team]
    away_stats = team_stats[away_team]

    home_stats["matches"] += 1
    away_stats["matches"] += 1

    home_stats["goals_for"] += home_goals
    home_stats["goals_against"] += away_goals

    away_stats["goals_for"] += away_goals
    away_stats["goals_against"] += home_goals

    # --------------------------------------
    # UPDATE RESULT STATISTICS
    # --------------------------------------

    if row["result"] == "H":

        home_stats["wins"] += 1
        away_stats["losses"] += 1

        home_stats["recent_results"].append(3)
        away_stats["recent_results"].append(0)

    elif row["result"] == "A":

        home_stats["losses"] += 1
        away_stats["wins"] += 1

        home_stats["recent_results"].append(0)
        away_stats["recent_results"].append(3)

    else:

        home_stats["draws"] += 1
        away_stats["draws"] += 1

        home_stats["recent_results"].append(1)
        away_stats["recent_results"].append(1)

    # --------------------------------------
    # UPDATE ELO
    # --------------------------------------

    expected_home = expected_result(home_elo, away_elo)

    if row["result"] == "H":
        actual_home = 1

    elif row["result"] == "D":
        actual_home = 0.5

    else:
        actual_home = 0

    actual_away = 1 - actual_home

    elo_ratings[home_team] = (
        home_elo + K_FACTOR * (actual_home - expected_home)
    )

    elo_ratings[away_team] = (
        away_elo + K_FACTOR * (actual_away - (1 - expected_home))
    )


# ==========================================
# 4. CREATE FEATURE DATAFRAME
# ==========================================

features_df = pd.DataFrame(feature_rows)

features_df.to_csv(
    "../data/team_features.csv",
    index=False
)

print("\nFeature engineering completed!")

print("Total matches:", len(features_df))
print("Total features:", len(features_df.columns))

print("\nFeature columns:")
print(features_df.columns.tolist())


# ==========================================
# 5. MACHINE LEARNING
# ==========================================

feature_columns = [

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

X = features_df[feature_columns]
y = features_df["result"]


# ==========================================
# 6. TIME-BASED TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(features_df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 7. RANDOM FOREST
# ==========================================

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=14,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

print("\nTraining advanced Random Forest model...")

model.fit(X_train, y_train)


# ==========================================
# 8. EVALUATION
# ==========================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n================================")
print("MODEL PERFORMANCE")
print("================================")

print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ==========================================
# 9. SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "../models/world_cup_result_model.pkl"
)

joblib.dump(
    feature_columns,
    "../models/feature_columns.pkl"
)

# Save latest Elo ratings
joblib.dump(
    dict(elo_ratings),
    "../models/elo_ratings.pkl"
)

print("\n================================")
print("MODEL SAVED")
print("================================")

print("../models/world_cup_result_model.pkl")
print("../models/feature_columns.pkl")
print("../models/elo_ratings.pkl")