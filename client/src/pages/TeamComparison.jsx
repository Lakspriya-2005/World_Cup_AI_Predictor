import { useEffect, useState } from "react";
import axios from "axios";

function TeamComparison() {
  const [teams, setTeams] = useState([]);
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [data1, setData1] = useState(null);
  const [data2, setData2] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const API_URL = "http://127.0.0.1:5000";

  useEffect(() => {
    const loadTeams = async () => {
      try {
        const response = await axios.get(`${API_URL}/teams`);
        setTeams(response.data.teams || []);
      } catch (err) {
        setError(
          "Unable to connect to ML API. Make sure Flask is running."
        );
      } finally {
        setLoading(false);
      }
    };

    loadTeams();
  }, []);

  const compareTeams = async () => {
    if (!team1 || !team2) {
      setError("Please select both teams.");
      return;
    }

    if (team1 === team2) {
      setError("Please select two different teams.");
      return;
    }

    setError("");
    setData1(null);
    setData2(null);

    try {
      const [response1, response2] = await Promise.all([
        axios.get(`${API_URL}/team-analysis/${encodeURIComponent(team1)}`),
        axios.get(`${API_URL}/team-analysis/${encodeURIComponent(team2)}`)
      ]);

      setData1(response1.data);
      setData2(response2.data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        "Unable to load team comparison."
      );
    }
  };

  const formatPercent = (value) => {
    if (value === undefined || value === null) return "N/A";
    return `${(value * 100).toFixed(1)}%`;
  };

  const formatNumber = (value) => {
    if (value === undefined || value === null) return "N/A";
    return Number(value).toFixed(2);
  };

  return (
    <div className="comparison-page">

      <div className="comparison-header">
        <div>
          <h1>⚔️ Team Comparison</h1>
          <p>
            Compare two teams using performance statistics and Elo ratings.
          </p>
        </div>
      </div>

      <div className="comparison-selector">

        <div className="comparison-field">
          <label>Team 1</label>

          <select
            value={team1}
            onChange={(e) => {
              setTeam1(e.target.value);
              setData1(null);
              setData2(null);
              setError("");
            }}
            disabled={loading}
          >
            <option value="">
              {loading ? "Loading teams..." : "Select Team"}
            </option>

            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div className="comparison-vs">
          VS
        </div>

        <div className="comparison-field">
          <label>Team 2</label>

          <select
            value={team2}
            onChange={(e) => {
              setTeam2(e.target.value);
              setData1(null);
              setData2(null);
              setError("");
            }}
            disabled={loading}
          >
            <option value="">
              {loading ? "Loading teams..." : "Select Team"}
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
        className="predict-button comparison-button"
        onClick={compareTeams}
        disabled={loading}
      >
        ⚔️ Compare Teams
      </button>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {data1 && data2 && (
        <div className="comparison-result">

          <div className="comparison-team-header">
            <div className="comparison-team">
              <div className="comparison-icon">⚽</div>
              <h2>{team1}</h2>
            </div>

            <div className="comparison-vs-large">
              VS
            </div>

            <div className="comparison-team">
              <div className="comparison-icon">⚽</div>
              <h2>{team2}</h2>
            </div>
          </div>

          <div className="comparison-table">

            <div className="comparison-row comparison-title-row">
              <span>Statistic</span>
              <strong>{team1}</strong>
              <strong>{team2}</strong>
            </div>

            <div className="comparison-row">
              <span>Elo Rating</span>
              <strong>{formatNumber(data1.elo)}</strong>
              <strong>{formatNumber(data2.elo)}</strong>
            </div>

            <div className="comparison-row">
              <span>Win Rate</span>
              <strong>{formatPercent(data1.win_rate)}</strong>
              <strong>{formatPercent(data2.win_rate)}</strong>
            </div>

            <div className="comparison-row">
              <span>Draw Rate</span>
              <strong>{formatPercent(data1.draw_rate)}</strong>
              <strong>{formatPercent(data2.draw_rate)}</strong>
            </div>

            <div className="comparison-row">
              <span>Loss Rate</span>
              <strong>{formatPercent(data1.loss_rate)}</strong>
              <strong>{formatPercent(data2.loss_rate)}</strong>
            </div>

            <div className="comparison-row">
              <span>Avg Goals Scored</span>
              <strong>
                {formatNumber(data1.avg_goals_for)}
              </strong>
              <strong>
                {formatNumber(data2.avg_goals_for)}
              </strong>
            </div>

            <div className="comparison-row">
              <span>Avg Goals Conceded</span>
              <strong>
                {formatNumber(data1.avg_goals_against)}
              </strong>
              <strong>
                {formatNumber(data2.avg_goals_against)}
              </strong>
            </div>

            <div className="comparison-row">
              <span>Recent Form</span>
              <strong>{data1.recent_form ?? "N/A"}</strong>
              <strong>{data2.recent_form ?? "N/A"}</strong>
            </div>

          </div>

        </div>
      )}

      {!data1 && !data2 && !error && (
        <div className="comparison-empty">
          <div className="empty-icon">⚔️</div>

          <h2>Compare Two Teams</h2>

          <p>
            Select two teams above to compare their performance,
            form and Elo ratings.
          </p>
        </div>
      )}

    </div>
  );
}

export default TeamComparison;