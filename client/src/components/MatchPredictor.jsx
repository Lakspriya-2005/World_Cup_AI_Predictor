import { useEffect, useState } from "react";
import axios from "axios";

function MatchPredictor() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingTeams, setLoadingTeams] = useState(true);
  const [error, setError] = useState("");

  const API_URL = "http://127.0.0.1:5000";

  // Load teams from Flask API
  useEffect(() => {
    const loadTeams = async () => {
      try {
        const response = await axios.get(`${API_URL}/teams`);
        setTeams(response.data.teams);
      } catch (err) {
        setError(
          "Unable to connect to ML API. Make sure Flask server is running."
        );
      } finally {
        setLoadingTeams(false);
      }
    };

    loadTeams();
  }, []);

  // Predict match
  const predictMatch = async () => {
    if (!homeTeam || !awayTeam) {
      setError("Please select both teams.");
      return;
    }

    if (homeTeam === awayTeam) {
      setError("Home and Away teams cannot be the same.");
      return;
    }

    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await axios.post(
        `${API_URL}/predict-match`,
        {
          home_team: homeTeam,
          away_team: awayTeam
        }
      );

      setPrediction(response.data);

    } catch (err) {
      setError(
        err.response?.data?.error ||
        "Unable to get prediction from ML API."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="predictor-box">

      <div className="team-selection">

        <div className="team-field">
          <label>Home Team</label>

          <select
            value={homeTeam}
            onChange={(e) => {
              setHomeTeam(e.target.value);
              setPrediction(null);
              setError("");
            }}
            disabled={loadingTeams}
          >
            <option value="">
              {loadingTeams ? "Loading teams..." : "Select team"}
            </option>

            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div className="vs">VS</div>

        <div className="team-field">
          <label>Away Team</label>

          <select
            value={awayTeam}
            onChange={(e) => {
              setAwayTeam(e.target.value);
              setPrediction(null);
              setError("");
            }}
            disabled={loadingTeams}
          >
            <option value="">
              {loadingTeams ? "Loading teams..." : "Select team"}
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
        className="predict-button"
        onClick={predictMatch}
        disabled={loading || loadingTeams}
      >
        {loading ? "Analyzing..." : "Predict Match"}
      </button>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {prediction && (
        <div className="prediction-result">

          <h2>Prediction Result</h2>

          <div className="match-name">
            {prediction.home_team}
            <span> vs </span>
            {prediction.away_team}
          </div>

          <div className="result-main">
            <span>Predicted Result</span>

            <strong>
              {prediction.result}
            </strong>
          </div>

          <div className="probability-grid">

            <div>
              <span>Home Win</span>

              <strong>
                {prediction.probabilities.H ?? 0}%
              </strong>
            </div>

            <div>
              <span>Draw</span>

              <strong>
                {prediction.probabilities.D ?? 0}%
              </strong>
            </div>

            <div>
              <span>Away Win</span>

              <strong>
                {prediction.probabilities.A ?? 0}%
              </strong>
            </div>

          </div>

          <div className="team-stats">

            <div>
              <span>{prediction.home_team} Elo</span>
              <strong>
                {prediction.team_data.home_elo}
              </strong>
            </div>

            <div>
              <span>{prediction.away_team} Elo</span>
              <strong>
                {prediction.team_data.away_elo}
              </strong>
            </div>

            <div>
              <span>Elo Difference</span>
              <strong>
                {prediction.team_data.elo_difference}
              </strong>
            </div>
            <div className="explanation-card">
              <div className="explanation-header">
                <div>
                  <h3>🧠 Why this prediction?</h3>
                  <p>
                    The prediction is calculated using multiple performance factors.
                  </p>
                </div>
              </div>

              <div className="explanation-grid">

                <div className="explanation-item">
                  <div className="explanation-item-header">
                    <span>📊 Elo Rating</span>
                    <strong>55%</strong>
                  </div>

                  <div className="explanation-values">
                    <span>
                      {prediction.home_team}:{" "}
                      {prediction.explanation?.elo_factor?.home ?? "N/A"}
                    </span>

                    <span>
                      {prediction.away_team}:{" "}
                      {prediction.explanation?.elo_factor?.away ?? "N/A"}
                    </span>
                  </div>

                  <small>
                    Advantage:{" "}
                    {prediction.explanation?.elo_factor?.advantage ?? "N/A"}
                  </small>
                </div>


                <div className="explanation-item">
                  <div className="explanation-item-header">
                    <span>🔥 Recent Form</span>
                    <strong>20%</strong>
                  </div>

                  <div className="explanation-values">
                    <span>
                      {prediction.home_team}:{" "}
                      {prediction.explanation?.form_factor?.home ?? "N/A"}
                    </span>

                    <span>
                      {prediction.away_team}:{" "}
                      {prediction.explanation?.form_factor?.away ?? "N/A"}
                    </span>
                  </div>

                  <small>
                    Advantage:{" "}
                    {prediction.explanation?.form_factor?.advantage ?? "N/A"}
                  </small>
                </div>


                <div className="explanation-item">
                  <div className="explanation-item-header">
                    <span>📈 Win Rate</span>
                    <strong>15%</strong>
                  </div>

                  <div className="explanation-values">
                    <span>
                      {prediction.home_team}:{" "}
                      {prediction.explanation?.win_rate_factor?.home ?? "N/A"}%
                    </span>

                    <span>
                      {prediction.away_team}:{" "}
                      {prediction.explanation?.win_rate_factor?.away ?? "N/A"}%
                    </span>
                  </div>

                  <small>
                    Advantage:{" "}
                    {prediction.explanation?.win_rate_factor?.advantage ?? "N/A"}
                  </small>
                </div>


                <div className="explanation-item">
                  <div className="explanation-item-header">
                    <span>⚽ Goal Strength</span>
                    <strong>10%</strong>
                  </div>

                  <div className="explanation-values">
                    <span>
                      {prediction.home_team}:{" "}
                      {prediction.explanation?.goal_factor?.home_avg_goals ?? "N/A"}
                    </span>

                    <span>
                      {prediction.away_team}:{" "}
                      {prediction.explanation?.goal_factor?.away_avg_goals ?? "N/A"}
                    </span>
                  </div>

                  <small>
                    Advantage:{" "}
                    {prediction.explanation?.goal_factor?.advantage ?? "N/A"}
                  </small>
                </div>

              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}

export default MatchPredictor;