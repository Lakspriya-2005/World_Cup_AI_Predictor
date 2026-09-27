import random

# ============================================================
# WORLD CUP TOURNAMENT SIMULATOR
# ============================================================

# 16 teams for demonstration
teams = [
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

# ------------------------------------------------------------
# Team strength ratings
# Higher rating = stronger team
# ------------------------------------------------------------

ratings = {
    "Brazil": 90,
    "Argentina": 91,
    "France": 90,
    "Germany": 86,
    "Spain": 88,
    "England": 87,
    "Portugal": 88,
    "Netherlands": 85,
    "Belgium": 84,
    "Italy": 84,
    "Croatia": 82,
    "Uruguay": 83,
    "Colombia": 81,
    "Japan": 78,
    "USA": 76,
    "Mexico": 75
}


# ------------------------------------------------------------
# Simulate a match
# ------------------------------------------------------------

def simulate_match(team1, team2):

    rating1 = ratings[team1]
    rating2 = ratings[team2]

    # Convert ratings into win probabilities
    total = rating1 + rating2

    probability1 = rating1 / total
    probability2 = rating2 / total

    random_value = random.random()

    if random_value < probability1:
        return team1
    else:
        return team2


# ------------------------------------------------------------
# Group Stage
# ------------------------------------------------------------

def group_stage():

    groups = {
        "Group A": teams[0:4],
        "Group B": teams[4:8],
        "Group C": teams[8:12],
        "Group D": teams[12:16]
    }

    qualified = []

    print("\n" + "=" * 60)
    print("                 GROUP STAGE")
    print("=" * 60)

    for group_name, group_teams in groups.items():

        points = {team: 0 for team in group_teams}

        print(f"\n{group_name}")
        print("-" * 30)

        # Each team plays every other team
        for i in range(len(group_teams)):
            for j in range(i + 1, len(group_teams)):

                team1 = group_teams[i]
                team2 = group_teams[j]

                winner = simulate_match(team1, team2)

                points[winner] += 3

                print(f"{team1} vs {team2} -> {winner}")

        # Sort teams by points
        table = sorted(
            points.items(),
            key=lambda x: x[1],
            reverse=True
        )

        print("\nPoints Table:")

        for position, (team, point) in enumerate(table, 1):
            print(f"{position}. {team} - {point} pts")

        # Top 2 qualify
        qualified.extend([table[0][0], table[1][0]])

    return qualified


# ------------------------------------------------------------
# Knockout Stage
# ------------------------------------------------------------

def knockout_stage(qualified):

    print("\n" + "=" * 60)
    print("                 QUARTER FINALS")
    print("=" * 60)

    quarter_winners = []

    for i in range(0, len(qualified), 2):

        team1 = qualified[i]
        team2 = qualified[i + 1]

        winner = simulate_match(team1, team2)

        print(f"{team1} vs {team2} -> {winner}")

        quarter_winners.append(winner)

    # --------------------------------------------------------
    # Semi Finals
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("                 SEMI FINALS")
    print("=" * 60)

    semi_winners = []

    for i in range(0, len(quarter_winners), 2):

        team1 = quarter_winners[i]
        team2 = quarter_winners[i + 1]

        winner = simulate_match(team1, team2)

        print(f"{team1} vs {team2} -> {winner}")

        semi_winners.append(winner)

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("                    FINAL")
    print("=" * 60)

    team1 = semi_winners[0]
    team2 = semi_winners[1]

    champion = simulate_match(team1, team2)

    print(f"\n{team1} vs {team2}")
    print(f"🏆 CHAMPION: {champion}")

    return champion


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    print("\n" + "=" * 60)
    print("          ⚽ WORLD CUP AI TOURNAMENT SIMULATOR")
    print("=" * 60)

    print("\nTeams:")
    for team in teams:
        print("-", team)

    qualified = group_stage()

    print("\n" + "=" * 60)
    print("              QUALIFIED TEAMS")
    print("=" * 60)

    for team in qualified:
        print("✓", team)

    champion = knockout_stage(qualified)

    print("\n" + "=" * 60)
    print("              🏆 TOURNAMENT RESULT")
    print("=" * 60)

    print(f"\nPredicted Champion: {champion}")

    print("\nSimulation completed successfully! 🎉")


if __name__ == "__main__":
    main()