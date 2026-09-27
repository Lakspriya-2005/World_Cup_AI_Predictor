import { useState } from "react";
import axios from "axios";

function Tournament() {
  const [tournament, setTournament] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const simulateTournament = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/tournament"
      );

      setTournament(response.data);
    } catch (err) {
      setError(
        "Unable to connect to tournament API. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tournament-page">

      <div className="tournament-header">
        <div>
          <h1>🏆 Tournament Simulator</h1>
          <p>
            Simulate a complete World Cup tournament using
            team Elo strength.
          </p>
        </div>

        <button
          className="predict-button"
          onClick={simulateTournament}
          disabled={loading}
        >
          {loading ? "Simulating..." : "Simulate Tournament"}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {tournament && (
        <>
          {/* CHAMPION */}

          <div className="champion-card">
            <div className="champion-trophy">🏆</div>

            <div>
              <span>Tournament Champion</span>

              <h2>
                {tournament.champion}
              </h2>
            </div>
          </div>

          {/* GROUP STAGE */}

          <section className="tournament-section">

            <h2>Group Stage</h2>

            <div className="groups-grid">

              {Object.entries(tournament.groups).map(
                ([groupName, group]) => (

                  <div
                    className="group-card"
                    key={groupName}
                  >

                    <h3>{groupName}</h3>

                    <div className="standings">

                      <div className="standing-header">
                        <span>#</span>
                        <span>Team</span>
                        <span>Pts</span>
                      </div>

                      {group.standings.map(
                        (team) => (

                          <div
                            className="standing-row"
                            key={team.team}
                          >

                            <span>
                              {team.position}
                            </span>

                            <span>
                              {team.team}
                            </span>

                            <strong>
                              {team.points}
                            </strong>

                          </div>

                        )
                      )}

                    </div>

                  </div>

                )
              )}

            </div>

          </section>

          {/* QUALIFIED TEAMS */}

          <section className="tournament-section">

            <h2>Qualified Teams</h2>

            <div className="qualified-grid">

              {tournament.qualified_teams.map(
                (team, index) => (

                  <div
                    className="qualified-team"
                    key={`${team}-${index}`}
                  >
                    <span>✓</span>
                    {team}
                  </div>

                )
              )}

            </div>

          </section>

          {/* QUARTER FINALS */}

          <section className="tournament-section">

            <h2>Quarter Finals</h2>

            <div className="knockout-grid">

              {tournament.quarter_finals.map(
                (match, index) => (

                  <div
                    className="match-card"
                    key={index}
                  >

                    <span>
                      {match.team1}
                    </span>

                    <strong>VS</strong>

                    <span>
                      {match.team2}
                    </span>

                    <div className="winner">
                      Winner: {match.winner}
                    </div>

                  </div>

                )
              )}

            </div>

          </section>

          {/* SEMI FINALS */}

          <section className="tournament-section">

            <h2>Semi Finals</h2>

            <div className="knockout-grid">

              {tournament.semi_finals.map(
                (match, index) => (

                  <div
                    className="match-card"
                    key={index}
                  >

                    <span>
                      {match.team1}
                    </span>

                    <strong>VS</strong>

                    <span>
                      {match.team2}
                    </span>

                    <div className="winner">
                      Winner: {match.winner}
                    </div>

                  </div>

                )
              )}

            </div>

          </section>

          {/* FINAL */}

          <section className="tournament-section">

            <h2>Final</h2>

            <div className="final-card">

              <span>
                {tournament.final.team1}
              </span>

              <strong>VS</strong>

              <span>
                {tournament.final.team2}
              </span>

              <div className="final-winner">
                🏆 {tournament.final.winner}
              </div>

            </div>

          </section>

          {/* SIMULATE AGAIN */}

          <div className="simulate-again">

            <button
              className="predict-button"
              onClick={simulateTournament}
              disabled={loading}
            >
              🔄 Simulate Again
            </button>

          </div>
        </>
      )}

      {!tournament && !loading && !error && (
        <div className="tournament-empty">

          <div className="empty-icon">🏆</div>

          <h2>Ready to Simulate</h2>

          <p>
            Click "Simulate Tournament" to run the
            complete tournament prediction.
          </p>

        </div>
      )}

    </div>
  );
}

export default Tournament;
