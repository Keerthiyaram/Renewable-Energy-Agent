import { useEffect, useState } from 'react';
import Dashboard from './components/Dashboard';
import DataUploadPanel from './components/DataUploadPanel';
import HealthCheck from './components/HealthCheck';
import AssetList from './components/AssetList';
import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = window.setInterval(() => setCurrentTime(new Date()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  return (
    <div className="aurora-shell">
      <aside className={`aurora-sidebar ${sidebarOpen ? 'is-open' : ''}`}>
        <div className="sidebar-brand">
          <div className="brand-mark">⚡</div>
          <div>
            <div className="brand-name">AURORA GRID</div>
            <div className="brand-subtitle">AI Renewable Energy</div>
          </div>
        </div>

        <nav className="sidebar-nav" aria-label="Sidebar navigation">
          <div className="nav-group">
            <div className="nav-label">Overview</div>
            <button className="nav-item active">Overview</button>
          </div>

          <div className="nav-group">
            <div className="nav-label">ENERGY</div>
            <button className="nav-item">Live Generation</button>
            <button className="nav-item">Generation Forecast</button>
            <button className="nav-item">Demand Forecast</button>
            <button className="nav-item">Energy Balance</button>
          </div>

          <div className="nav-group">
            <div className="nav-label">ASSETS</div>
            <button className="nav-item">Solar</button>
            <button className="nav-item">Wind</button>
            <button className="nav-item">Battery</button>
          </div>

          <div className="nav-group">
            <div className="nav-label">INTELLIGENCE</div>
            <button className="nav-item">AI Operations</button>
            <button className="nav-item">Anomalies & Performance</button>
            <button className="nav-item">Optimization</button>
          </div>

          <button className="nav-item">Weather</button>
          <button className="nav-item">Alerts</button>
          <button className="nav-item">Reports</button>
        </nav>

        <div className="sidebar-footer">
          <div className="nav-label">System Status</div>
          <div className="system-status">
            <span className="dot" aria-hidden="true" />
            All Systems Operational
          </div>
        </div>
      </aside>

      <div className="aurora-main-panel">
        <header className="aurora-header">
          <div className="header-left">
            <button
              className="menu-button"
              aria-label="Toggle sidebar"
              onClick={() => setSidebarOpen((value) => !value)}
            >
              ☰
            </button>
            <div>
              <div className="eyebrow">Good evening, Operator</div>
              <h1>Renewable Energy Operations Center</h1>
            </div>
          </div>

          <div className="header-right">
            <div className="status-badge status-badge--live">Simulation Mode</div>
            <div className="timestamp">Last updated: {currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</div>
            <button className="ghost-button">Refresh</button>
            <button className="ghost-button ghost-button--icon" aria-label="Notifications">🔔</button>
            <div className="profile-pill">AO</div>
          </div>
        </header>

        <main className="aurora-content">
          <section className="overview-hero">
            <div className="overview-hero__copy">
              <p className="section-kicker">Operations overview</p>
              <h2>Grid health is stable and renewable output is trending above plan.</h2>
            </div>
            <div className="overview-hero__stats">
              <div className="mini-stat">
                <span className="mini-stat__label">Generation mix</span>
                <strong>72%</strong>
              </div>
              <div className="mini-stat mini-stat--accent">
                <span className="mini-stat__label">Forecast confidence</span>
                <strong>92%</strong>
              </div>
              <div className="mini-stat">
                <span className="mini-stat__label">Battery reserve</span>
                <strong>84%</strong>
              </div>
            </div>
          </section>

          <HealthCheck />
          <Dashboard />
          <DataUploadPanel />
          <AssetList />
        </main>
      </div>
    </div>
  );
}

export default App;
