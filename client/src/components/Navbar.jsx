import { Menu, Activity } from "lucide-react";

function Navbar({ setMobileOpen }) {
  return (
    <header className="topbar">
      <button
        className="mobile-menu"
        onClick={() => setMobileOpen(true)}
      >
        <Menu size={22} />
      </button>

      <div className="page-title">
        World Cup AI Predictor
      </div>

      <div className="model-status">
        <Activity size={16} />
        <span>Model Online</span>
      </div>
    </header>
  );
}

export default Navbar;