import { useEffect, useState } from "react";
import axios from "axios";

function Teams() {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [teamData, setTeamData] = useState(null);
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
          "Unable to connect to ML API. Make sure Flask server is running."
        );
      } finally {
        setLoading(false);
      }
    };

    loadTeams();
  }, []);

  const loadTeamAnalysis = async (team) => {
    setSelectedTeam(team);
    setTeamData(null);
    setError("");

    try {
      const response = await axios.get(
        `${API_URL}/teams`
      );

      const data = response.data;

      if (data.team_data && data.team_data[team]) {
        setTeamData(data.team_data[team]);
      } else if (data.teams) {
        setTeamData({
          team: team
        });
      }
    } catch (err) {
      setError("Unable to load team analysis.");
    }
  };

  return (
    <div className="team-analysis-page">

      <div className="team-analysis-header">
        <div>
          <h1>⚽ Team Analysis</h1>
          <p>
            Explore team performance, form and Elo ratings.
          </p>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="team-selector-card">

        <label>Select Team</label>

        <select
          value={selectedTeam}
          onChange={(e) =>
            loadTeamAnalysis(e.target.value)
          }
          disabled={loading}
        >
          <option value="">
            {loading
              ? "Loading teams..."
              : "Select a team"}
          </option>

          {teams.map((team) => (
            <option key={team} value={team}>
              {team}
            </option>
          ))}
        </select>

      </div>

      {selectedTeam && teamData && (
        <div className="team-analysis-result">

          <div className="team-profile-card">

            <div className="team-icon">
              ⚽
            </div>

            <div>
              <span>Team</span>
              <h2>{selectedTeam}</h2>
            </div>

          </div>

          <div className="team-stats-grid">

            <div className="team-stat-card">
              <span>Elo Rating</span>
              <strong>
                {teamData.elo ?? "N/A"}
              </strong>
            </div>

            <div className="team-stat-card">
              <span>Win Rate</span>
              <strong>
                {teamData.win_rate !== undefined
                  ? `${(teamData.win_rate * 100).toFixed(1)}%`
                  : "N/A"}
              </strong>
            </div>

            <div className="team-stat-card">
              <span>Draw Rate</span>
              <strong>
                {teamData.draw_rate !== undefined
                  ? `${(teamData.draw_rate * 100).toFixed(1)}%`
                  : "N/A"}
              </strong>
            </div>

            <div className="team-stat-card">
              <span>Loss Rate</span>
              <strong>
                {teamData.loss_rate !== undefined
                  ? `${(teamData.loss_rate * 100).toFixed(1)}%`
                  : "N/A"}
              </strong>
            </div>

            <div className="team-stat-card">
              <span>Avg Goals Scored</span>
              <strong>
                {teamData.avg_goals_for !== undefined
                  ? teamData.avg_goals_for.toFixed(2)
                  : "N/A"}
              </strong>
            </div>

            <div className="team-stat-card">
              <span>Avg Goals Conceded</span>
              <strong>
                {teamData.avg_goals_against !== undefined
                  ? teamData.avg_goals_against.toFixed(2)
                  : "N/A"}
              </strong>
            </div>

            <div className="team-stat-card">
              <span>Recent Form</span>
              <strong>
                {teamData.recent_form ?? "N/A"}
              </strong>
            </div>

          </div>

        </div>
      )}

      {!selectedTeam && !loading && (
        <div className="team-analysis-empty">

          <div className="empty-icon">
            ⚽
          </div>

          <h2>Select a Team</h2>

          <p>
            Choose a team above to view its
            performance analysis.
          </p>

        </div>
      )}

    </div>
  );
}

export default Teams;