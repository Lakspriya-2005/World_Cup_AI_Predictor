from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import math
import random


app = Flask(__name__)
CORS(app)


# ============================================================
# DATA
# ============================================================

TEAM_FEATURES_PATH = "../data/team_features.csv"

team_features = pd.read_csv(TEAM_FEATURES_PATH)

print("Team features loaded successfully!")
print("Total records:", len(team_features))


# ============================================================
# TEAM FEATURES
# ============================================================

def get_team_features(team):

    matches = team_features[
        (team_features["home_team"] == team) |
        (team_features["away_team"] == team)
    ]

    if matches.empty:
        return None

    latest = matches.iloc[-1]

    if latest["home_team"] == team:

        return {
            "win_rate": float(latest["home_win_rate"]),
            "draw_rate": float(latest["home_draw_rate"]),
            "loss_rate": float(latest["home_loss_rate"]),
            "avg_goals_for": float(latest["home_avg_goals_for"]),
            "avg_goals_against": float(latest["home_avg_goals_against"]),
            "recent_form": float(latest["home_recent_form"]),
            "elo": float(latest["home_elo"])
        }

    return {
        "win_rate": float(latest["away_win_rate"]),
        "draw_rate": float(latest["away_draw_rate"]),
        "loss_rate": float(latest["away_loss_rate"]),
        "avg_goals_for": float(latest["away_avg_goals_for"]),
        "avg_goals_against": float(latest["away_avg_goals_against"]),
        "recent_form": float(latest["away_recent_form"]),
        "elo": float(latest["away_elo"])
    }


# ============================================================
# PURE PYTHON PREDICTION ENGINE
# ============================================================

def calculate_prediction(home, away):

    # --------------------------------------------------------
    # 1. ELO
    # --------------------------------------------------------

    elo_difference = home["elo"] - away["elo"]

    home_elo_probability = 1 / (
        1 + math.pow(10, -elo_difference / 400)
    )

    # --------------------------------------------------------
    # 2. RECENT FORM
    # --------------------------------------------------------

    form_difference = (
        home["recent_form"] - away["recent_form"]
    ) / 15

    # --------------------------------------------------------
    # 3. WIN RATE
    # --------------------------------------------------------

    win_rate_difference = (
        home["win_rate"] - away["win_rate"]
    )

    # --------------------------------------------------------
    # 4. GOAL DIFFERENCE
    # --------------------------------------------------------

    goal_difference = (
        home["avg_goals_for"]
        - away["avg_goals_for"]
    )

    # --------------------------------------------------------
    # 5. COMBINED STRENGTH
    # --------------------------------------------------------

    strength_score = (
        home_elo_probability * 0.55
        + (0.5 + form_difference * 0.5) * 0.20
        + (0.5 + win_rate_difference * 0.5) * 0.15
        + (0.5 + goal_difference / 5) * 0.10
    )

    strength_score = max(
        0.05,
        min(0.95, strength_score)
    )

    # --------------------------------------------------------
    # 6. DRAW PROBABILITY
    # --------------------------------------------------------

    draw_probability = 0.28 - (
        abs(elo_difference) / 1000
    )

    draw_probability = max(
        0.15,
        min(0.30, draw_probability)
    )

    # --------------------------------------------------------
    # 7. FINAL PROBABILITIES
    # --------------------------------------------------------

    remaining_probability = 1 - draw_probability

    home_probability = (
        strength_score * remaining_probability
    )

    away_probability = (
        remaining_probability - home_probability
    )

    # --------------------------------------------------------
    # 8. NORMALIZE
    # --------------------------------------------------------

    total = (
        home_probability
        + draw_probability
        + away_probability
    )

    home_probability /= total
    draw_probability /= total
    away_probability /= total

    probabilities = {
        "H": round(home_probability * 100, 2),
        "D": round(draw_probability * 100, 2),
        "A": round(away_probability * 100, 2)
    }

    # --------------------------------------------------------
    # 9. PREDICTION
    # --------------------------------------------------------

    prediction = max(
        probabilities,
        key=probabilities.get
    )

    result_map = {
        "H": "Home Win",
        "D": "Draw",
        "A": "Away Win"
    }

    return {
        "prediction": prediction,
        "result": result_map[prediction],
        "probabilities": probabilities
    }


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "World Cup AI Predictor API is running!",
        "status": "success",
        "engine": "Pure Python AI Prediction Engine"
    })


# ============================================================
# TEAM LIST
# ============================================================

@app.route("/teams", methods=["GET"])
def get_teams():

    home_teams = set(
        team_features["home_team"].dropna()
    )

    away_teams = set(
        team_features["away_team"].dropna()
    )

    teams = sorted(
        home_teams.union(away_teams)
    )

    return jsonify({
        "teams": teams
    })


# ============================================================
# TEAM ANALYSIS
# ============================================================

@app.route("/team-analysis/<team_name>", methods=["GET"])
def team_analysis(team_name):

    try:

        team_data = get_team_features(team_name)

        if team_data is None:

            return jsonify({
                "error": f"Team '{team_name}' not found"
            }), 404

        return jsonify({
            "team": team_name,
            "elo": team_data["elo"],
            "win_rate": team_data["win_rate"],
            "draw_rate": team_data["draw_rate"],
            "loss_rate": team_data["loss_rate"],
            "avg_goals_for": team_data["avg_goals_for"],
            "avg_goals_against": team_data["avg_goals_against"],
            "recent_form": team_data["recent_form"]
        })

    except Exception as error:

        print("Team analysis error:", error)

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# MATCH PREDICTION
# ============================================================

@app.route("/predict-match", methods=["POST"])
def predict_match():

    try:

        data = request.get_json()

        home_team = data.get("home_team")
        away_team = data.get("away_team")

        if not home_team or not away_team:

            return jsonify({
                "error": "Both teams are required."
            }), 400

        if home_team == away_team:

            return jsonify({
                "error": "Home and away teams cannot be the same."
            }), 400

        home = get_team_features(home_team)
        away = get_team_features(away_team)

        if home is None:

            return jsonify({
                "error": f"Team not found: {home_team}"
            }), 404

        if away is None:

            return jsonify({
                "error": f"Team not found: {away_team}"
            }), 404

        prediction = calculate_prediction(
            home,
            away
        )

        # ====================================================
        # EXPLANATION FACTORS
        # ====================================================

        elo_difference = home["elo"] - away["elo"]

        form_difference = (
            home["recent_form"]
            - away["recent_form"]
        )

        win_rate_difference = (
            home["win_rate"]
            - away["win_rate"]
        )

        goal_difference = (
            home["avg_goals_for"]
            - away["avg_goals_for"]
        )

        # Determine which team has advantage
        if elo_difference > 0:
            elo_advantage = home_team
        elif elo_difference < 0:
            elo_advantage = away_team
        else:
            elo_advantage = "Equal"

        if form_difference > 0:
            form_advantage = home_team
        elif form_difference < 0:
            form_advantage = away_team
        else:
            form_advantage = "Equal"

        if win_rate_difference > 0:
            win_rate_advantage = home_team
        elif win_rate_difference < 0:
            win_rate_advantage = away_team
        else:
            win_rate_advantage = "Equal"

        if goal_difference > 0:
            goal_advantage = home_team
        elif goal_difference < 0:
            goal_advantage = away_team
        else:
            goal_advantage = "Equal"

        # ====================================================
        # RETURN PREDICTION + EXPLANATION
        # ====================================================

        return jsonify({

            "home_team": home_team,

            "away_team": away_team,

            "prediction": prediction["prediction"],

            "result": prediction["result"],

            "probabilities": prediction["probabilities"],

            "team_data": {

                "home_elo": round(
                    home["elo"],
                    2
                ),

                "away_elo": round(
                    away["elo"],
                    2
                ),

                "elo_difference": round(
                    elo_difference,
                    2
                ),

                "home_recent_form": round(
                    home["recent_form"],
                    2
                ),

                "away_recent_form": round(
                    away["recent_form"],
                    2
                )

            },

            # =================================================
            # EXPLAINABLE AI
            # =================================================

            "explanation": {

                "elo_factor": {

                    "home": round(
                        home["elo"],
                        2
                    ),

                    "away": round(
                        away["elo"],
                        2
                    ),

                    "difference": round(
                        elo_difference,
                        2
                    ),

                    "advantage": elo_advantage

                },

                "form_factor": {

                    "home": round(
                        home["recent_form"],
                        2
                    ),

                    "away": round(
                        away["recent_form"],
                        2
                    ),

                    "difference": round(
                        form_difference,
                        2
                    ),

                    "advantage": form_advantage

                },

                "win_rate_factor": {

                    "home": round(
                        home["win_rate"] * 100,
                        2
                    ),

                    "away": round(
                        away["win_rate"] * 100,
                        2
                    ),

                    "difference": round(
                        win_rate_difference * 100,
                        2
                    ),

                    "advantage": win_rate_advantage

                },

                "goal_factor": {

                    "home_avg_goals": round(
                        home["avg_goals_for"],
                        2
                    ),

                    "away_avg_goals": round(
                        away["avg_goals_for"],
                        2
                    ),

                    "difference": round(
                        goal_difference,
                        2
                    ),

                    "advantage": goal_advantage

                },

                "weights": {

                    "elo": "55%",

                    "recent_form": "20%",

                    "win_rate": "15%",

                    "goal_difference": "10%"

                }

            }

        })

    except Exception as error:

        print("Prediction error:", error)

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# SCORE PREDICTION
# ============================================================

@app.route("/predict-score", methods=["POST"])
def predict_score_api():

    try:

        data = request.get_json()

        home_team = data.get("home_team")
        away_team = data.get("away_team")

        if not home_team or not away_team:

            return jsonify({
                "error": "Both teams are required"
            }), 400

        if home_team == away_team:

            return jsonify({
                "error": "Home and Away teams cannot be the same"
            }), 400

        home_data = get_team_features(home_team)
        away_data = get_team_features(away_team)

        if home_data is None:

            return jsonify({
                "error": f"Team '{home_team}' not found"
            }), 404

        if away_data is None:

            return jsonify({
                "error": f"Team '{away_team}' not found"
            }), 404

        # Historical goal baseline

        home_goals = (
            home_data["avg_goals_for"] * 0.6
            + away_data["avg_goals_against"] * 0.4
        )

        away_goals = (
            away_data["avg_goals_for"] * 0.6
            + home_data["avg_goals_against"] * 0.4
        )

        # Keep predictions within reasonable range

        home_goals = max(
            0.0,
            min(5.0, home_goals)
        )

        away_goals = max(
            0.0,
            min(5.0, away_goals)
        )

        predicted_home = round(home_goals)
        predicted_away = round(away_goals)

        if predicted_home > predicted_away:

            result = f"{home_team} Win"

        elif predicted_home < predicted_away:

            result = f"{away_team} Win"

        else:

            result = "Draw"

        return jsonify({

            "home_team": home_team,

            "away_team": away_team,

            "expected_home_goals": round(
                home_goals,
                2
            ),

            "expected_away_goals": round(
                away_goals,
                2
            ),

            "predicted_home": predicted_home,

            "predicted_away": predicted_away,

            "result": result

        })

    except Exception as error:

        print(
            "Score prediction error:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# TOURNAMENT SIMULATION
# ============================================================

TOURNAMENT_TEAMS = [

    "Brazil",
    "Argentina",
    "France",
    "Germany",
    "Spain",
    "England",
    "Portugal",
    "Netherlands",
    "Belgium",
    "Italy",
    "Croatia",
    "Uruguay",
    "Colombia",
    "Japan",
    "USA",
    "Mexico"

]


def simulate_tournament_match(team1, team2):

    team1_data = get_team_features(team1)
    team2_data = get_team_features(team2)

    if team1_data is None or team2_data is None:

        return team1

    elo1 = team1_data["elo"]
    elo2 = team2_data["elo"]

    probability1 = 1 / (
        1 + math.pow(
            10,
            (elo2 - elo1) / 400
        )
    )

    # Small first-team advantage

    probability1 = min(
        0.95,
        max(
            0.05,
            probability1 + 0.03
        )
    )

    if random.random() < probability1:

        return team1

    return team2


def run_tournament():

    teams = TOURNAMENT_TEAMS.copy()

    random.shuffle(teams)

    # --------------------------------------------------------
    # GROUP STAGE
    # --------------------------------------------------------

    groups = {

        "Group A": teams[0:4],

        "Group B": teams[4:8],

        "Group C": teams[8:12],

        "Group D": teams[12:16]

    }

    qualified = []
    group_results = {}

    for group_name, group_teams in groups.items():

        points = {
            team: 0
            for team in group_teams
        }

        matches = []

        for i in range(len(group_teams)):

            for j in range(i + 1, len(group_teams)):

                team1 = group_teams[i]
                team2 = group_teams[j]

                winner = simulate_tournament_match(
                    team1,
                    team2
                )

                points[winner] += 3

                matches.append({

                    "team1": team1,

                    "team2": team2,

                    "winner": winner

                })

        table = sorted(
            points.items(),
            key=lambda x: x[1],
            reverse=True
        )

        standings = []

        for position, (team, point) in enumerate(
            table,
            1
        ):

            standings.append({

                "position": position,

                "team": team,

                "points": point

            })

        group_results[group_name] = {

            "teams": group_teams,

            "standings": standings,

            "matches": matches

        }

        qualified.extend([

            table[0][0],

            table[1][0]

        ])

    # --------------------------------------------------------
    # QUARTER FINALS
    # --------------------------------------------------------

    quarter_finals = []

    semi_finalists = []

    for i in range(
        0,
        len(qualified),
        2
    ):

        team1 = qualified[i]
        team2 = qualified[i + 1]

        winner = simulate_tournament_match(
            team1,
            team2
        )

        quarter_finals.append({

            "team1": team1,

            "team2": team2,

            "winner": winner

        })

        semi_finalists.append(winner)

    # --------------------------------------------------------
    # SEMI FINALS
    # --------------------------------------------------------

    semi_finals = []

    finalists = []

    for i in range(
        0,
        len(semi_finalists),
        2
    ):

        team1 = semi_finalists[i]
        team2 = semi_finalists[i + 1]

        winner = simulate_tournament_match(
            team1,
            team2
        )

        semi_finals.append({

            "team1": team1,

            "team2": team2,

            "winner": winner

        })

        finalists.append(winner)

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    champion = simulate_tournament_match(
        finalists[0],
        finalists[1]
    )

    final = {

        "team1": finalists[0],

        "team2": finalists[1],

        "winner": champion

    }

    return {

        "groups": group_results,

        "qualified_teams": qualified,

        "quarter_finals": quarter_finals,

        "semi_finals": semi_finals,

        "final": final,

        "champion": champion

    }


# ============================================================
# TOURNAMENT API
# ============================================================

@app.route("/tournament", methods=["GET"])
def tournament():

    try:

        result = run_tournament()

        return jsonify(result)

    except Exception as error:

        print(
            "Tournament error:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )