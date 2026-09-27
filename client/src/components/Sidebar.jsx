import {
  LayoutDashboard,
  Trophy,
  Target,
  Users,
  GitCompare,
  X
} from "lucide-react";

function Sidebar({ activePage, setActivePage, mobileOpen, setMobileOpen }) {
  const menuItems = [
    {
      name: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Match Predictor",
      icon: Target,
    },
    {
      name: "Score Prediction",
      icon: Target,
    },
    {
      name: "Tournament",
      icon: Trophy,
    },
    {
      name: "Team Analysis",
      icon: Users,
    },
    { 
      name: "Team Comparison",
      icon: GitCompare,
    },
  ];

  return (
    <>
      {mobileOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside className={`sidebar ${mobileOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div>
            <div className="sidebar-title">WC AI</div>
            <div className="sidebar-subtitle">Predictor</div>
          </div>

          <button
            className="close-sidebar"
            onClick={() => setMobileOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <nav className="sidebar-menu">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`menu-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => {
                  setActivePage(item.name);
                  setMobileOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <span>AI Model</span>
          <strong>55.04% Accuracy</strong>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;