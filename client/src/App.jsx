import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import MatchPredictor from "./components/MatchPredictor";
import Tournament from "./pages/Tournament";
import Teams from "./pages/Teams";
import Dashboard from "./pages/Dashboard";
import TeamComparison from "./pages/TeamComparison";
import ScorePrediction from "./pages/ScorePrediction";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        mobileOpen={mobileOpen}
        setMobileOpen={setMobileOpen}
      />

      <div className="main-content">
        <Navbar setMobileOpen={setMobileOpen} />

        <main className="page-content">

          {activePage === "Dashboard" && (
            <Dashboard />
          )}

          {activePage === "Match Predictor" && (
            <MatchPredictor />
          )}

          {activePage === "Tournament" && (
            <Tournament />
          )}

          {activePage === "Team Analysis" && (
            <Teams />
          )}

          {activePage === "Team Comparison" && (
            <TeamComparison />
          )}

          {activePage === "Score Prediction" && (
            <ScorePrediction />
          )}

        </main>
      </div>
    </div>
  );
}

export default App;