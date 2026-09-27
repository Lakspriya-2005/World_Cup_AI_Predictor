import {
  Activity,
  Target,
  Trophy,
  Users,
  Brain,
  BarChart3
} from "lucide-react";

function Dashboard() {
  return (
    <div className="dashboard-page">

      {/* HEADER */}
      <div className="dashboard-header">
        <div>
          <h1>World Cup AI Dashboard</h1>
          <p>
            AI-powered football prediction and tournament analytics.
          </p>
        </div>

        <div className="dashboard-status">
          <Activity size={17} />
          <span>AI Model Online</span>
        </div>
      </div>

      {/* STAT CARDS */}
      <div className="dashboard-stats">

        <div className="dashboard-card">
          <div className="dashboard-card-icon">
            <Target size={22} />
          </div>

          <div>
            <span>Model Accuracy</span>
            <h2>55.04%</h2>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="dashboard-card-icon">
            <Users size={22} />
          </div>

          <div>
            <span>Teams Available</span>
            <h2>195+</h2>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="dashboard-card-icon">
            <Trophy size={22} />
          </div>

          <div>
            <span>Tournament Teams</span>
            <h2>16</h2>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="dashboard-card-icon">
            <Brain size={22} />
          </div>

          <div>
            <span>Prediction Engine</span>
            <h2>AI</h2>
          </div>
        </div>

      </div>

      {/* MAIN CONTENT */}
      <div className="dashboard-grid">

        {/* ABOUT MODEL */}
        <div className="dashboard-panel">

          <div className="panel-header">
            <div>
              <h2>AI Prediction Engine</h2>
              <p>
                Current prediction system overview
              </p>
            </div>

            <BarChart3 size={22} />
          </div>

          <div className="model-info">

            <div className="info-row">
              <span>Historical Matches</span>
              <strong>49,547</strong>
            </div>

            <div className="info-row">
              <span>Features Used</span>
              <strong>15</strong>
            </div>

            <div className="info-row">
              <span>Prediction Classes</span>
              <strong>Win / Draw / Loss</strong>
            </div>

            <div className="info-row">
              <span>Model Accuracy</span>
              <strong>55.04%</strong>
            </div>

            <div className="info-row">
              <span>Elo Rating System</span>
              <strong>Enabled</strong>
            </div>

          </div>

        </div>

        {/* FEATURES */}
        <div className="dashboard-panel">

          <div className="panel-header">
            <div>
              <h2>Platform Features</h2>
              <p>
                Available prediction modules
              </p>
            </div>
          </div>

          <div className="feature-list">

            <div className="feature-item">
              <div className="feature-icon">
                ⚽
              </div>

              <div>
                <strong>Match Predictor</strong>
                <span>
                  Predict home win, draw or away win.
                </span>
              </div>
            </div>

            <div className="feature-item">
              <div className="feature-icon">
                🏆
              </div>

              <div>
                <strong>Tournament Simulator</strong>
                <span>
                  Simulate groups and knockout stages.
                </span>
              </div>
            </div>

            <div className="feature-item">
              <div className="feature-icon">
                📊
              </div>

              <div>
                <strong>Team Analysis</strong>
                <span>
                  Explore team form and Elo statistics.
                </span>
              </div>
            </div>

          </div>

        </div>

      </div>

      {/* PIPELINE */}
      <div className="dashboard-panel pipeline-panel">

        <div className="panel-header">
          <div>
            <h2>AI Prediction Pipeline</h2>
            <p>
              From historical data to match prediction
            </p>
          </div>
        </div>

        <div className="pipeline">

          <div className="pipeline-step">
            <div className="pipeline-number">01</div>
            <strong>Historical Data</strong>
            <span>49K+ international matches</span>
          </div>

          <div className="pipeline-arrow">→</div>

          <div className="pipeline-step">
            <div className="pipeline-number">02</div>
            <strong>Feature Engineering</strong>
            <span>Form, goals and Elo ratings</span>
          </div>

          <div className="pipeline-arrow">→</div>

          <div className="pipeline-step">
            <div className="pipeline-number">03</div>
            <strong>AI Prediction</strong>
            <span>Win / Draw / Loss</span>
          </div>

          <div className="pipeline-arrow">→</div>

          <div className="pipeline-step">
            <div className="pipeline-number">04</div>
            <strong>Result</strong>
            <span>Prediction probabilities</span>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;