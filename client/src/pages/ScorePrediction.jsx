import { useEffect, useState } from "react";
import axios from "axios";

function ScorePrediction() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState("");

  const API_URL = "http://127.0.0.1:5000";

  useEffect(() => {
    const loadTeams = async () => {
      try {
        const response = await axios.get(`${API_URL}/teams`);
        setTeams(response.data.teams || []);
      } catch (err) {
        setError("Unable to connect to ML API.");
      } finally {
        setLoading(false);
      }
    };

    loadTeams();
  }, []);

  const predictScore = async () => {
    if (!homeTeam || !awayTeam) {
      setError("Please select both teams.");
      return;
    }

    if (homeTeam === awayTeam) {
      setError("Please select two different teams.");
      return;
    }

    setPredicting(true);
    setError("");
    setPrediction(null);

    try {
      const response = await axios.post(
        `${API_URL}/predict-score`,
        {
          home_team: homeTeam,
          away_team: awayTeam
        }
      );

      setPrediction(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        "Unable to get score prediction."
      );
    } finally {
      setPredicting(false);
    }
  };

  return (
    <div className="score-page">

      <div className="score-header">
        <div>
          <h1>🎯 Score Prediction</h1>
          <p>
            Predict the expected score for an international football match.
          </p>
        </div>
      </div>

      <div className="score-selector">

        <div className="score-field">
          <label>Home Team</label>

          <select
            value={homeTeam}
            onChange={(e) => {
              setHomeTeam(e.target.value);
              setPrediction(null);
              setError("");
            }}
            disabled={loading}
          >
            <option value="">
              {loading ? "Loading teams..." : "Select Home Team"}
            </option>

            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div className="score-vs">
          VS
        </div>

        <div className="score-field">
          <label>Away Team</label>

          <select
            value={awayTeam}
            onChange={(e) => {
              setAwayTeam(e.target.value);
              setPrediction(null);
              setError("");
            }}
            disabled={loading}
          >
            <option value="">
              {loading ? "Loading teams..." : "Select Away Team"}
            </option>

            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

      </div>

      <button
        className="predict-button score-button"
        onClick={predictScore}
        disabled={loading || predicting}
      >
        {predicting ? "Predicting Score..." : "🎯 Predict Score"}
      </button>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {prediction && (
        <div className="score-result">

          <div className="score-match">
            <span>{prediction.home_team}</span>

            <div className="score-display">
              <strong>
                {prediction.predicted_home}
              </strong>

              <span>-</span>

              <strong>
                {prediction.predicted_away}
              </strong>
            </div>

            <span>{prediction.away_team}</span>
          </div>

          <div className="expected-goals">

            <div className="goal-card">
              <span>
                {prediction.home_team} Expected Goals
              </span>

              <strong>
                {Number(
                  prediction.expected_home_goals
                ).toFixed(2)}
              </strong>
            </div>

            <div className="goal-card">
              <span>
                {prediction.away_team} Expected Goals
              </span>

              <strong>
                {Number(
                  prediction.expected_away_goals
                ).toFixed(2)}
              </strong>
            </div>

          </div>

          <div className="predicted-result">
            <span>Predicted Result</span>

            <strong>
              {prediction.result}
            </strong>
          </div>

          <div className="score-note">
            <span>ℹ️</span>
            <p>
              Score prediction is based on the historical goal
              baseline from the training dataset.
            </p>
          </div>

        </div>
      )}

      {!prediction && !error && (
        <div className="score-empty">
          <div className="empty-icon">🎯</div>

          <h2>Predict Match Score</h2>

          <p>
            Select two teams to estimate the expected match score.
          </p>
        </div>
      )}

    </div>
  );
}

export default ScorePrediction;