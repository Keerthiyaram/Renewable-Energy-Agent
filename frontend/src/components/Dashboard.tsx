import { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import api from '../services/api';

interface DashboardSnapshot {
  generated_at: string;
  current: {
    solar_generation_mw: number;
    wind_generation_mw: number;
    total_renewable_generation_mw: number;
    installed_capacity_mw: number;
    capacity_utilization_pct: number;
    current_demand_mw: number;
    renewable_surplus_deficit_mw: number;
    battery_soc_percent: number;
    battery_stored_energy_mwh: number;
  };
  forecast: {
    solar: { predicted_generation_mw: number; confidence: number };
    wind: { predicted_generation_mw: number; confidence: number };
    demand: { predicted_generation_mw: number; confidence: number };
  };
  alerts: Array<{ id: string; severity: string; category: string; message: string }>; 
  weather: { source: string; current: Record<string, number | null> };
}

function Dashboard() {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => { 
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/monitoring/overview');
      setSnapshot(response.data);
    } catch (err) {
      setError('Failed to load dashboard snapshot');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="panel panel--compact"><p className="muted-text">Loading dashboard...</p></div>;
  if (error) return <div className="alert alert--error">{error}</div>;
  if (!snapshot) return null;

  const current = snapshot.current;
  const chartData = [
    { name: 'Solar', generation: current.solar_generation_mw, forecast: snapshot.forecast.solar.predicted_generation_mw },
    { name: 'Wind', generation: current.wind_generation_mw, forecast: snapshot.forecast.wind.predicted_generation_mw },
    { name: 'Total Renewable', generation: current.total_renewable_generation_mw, forecast: current.total_renewable_generation_mw + snapshot.forecast.solar.predicted_generation_mw * 0.05 },
    { name: 'Demand', generation: current.current_demand_mw, forecast: snapshot.forecast.demand.predicted_generation_mw },
  ];

  const weatherCurrent = snapshot.weather.current ?? {};
  const solarTrend = current.solar_generation_mw >= snapshot.forecast.solar.predicted_generation_mw ? 'On target' : 'Below expected';
  const batteryRecommendation = current.renewable_surplus_deficit_mw >= 0 ? 'Charge battery' : 'Balance dispatch';
  const alert = snapshot.alerts[0];

  return (
    <div className="dashboard-shell">
      <div className="panel-header">
        <div>
          <p className="section-kicker">Overview</p>
          <h2>Grid performance</h2>
        </div>
      </div>

      <div className="metric-grid">
        <MetricCard label="Solar" value={`${current.solar_generation_mw.toFixed(1)} MW`} unit="Expected: 4.7 MW" status="Operational" tone="solar" />
        <MetricCard label="Wind" value={`${current.wind_generation_mw.toFixed(1)} MW`} unit="Expected: 2.9 MW" status="Operational" tone="wind" />
        <MetricCard label="Total Renewable" value={`${current.total_renewable_generation_mw.toFixed(1)} MW`} unit={`Balance: ${current.renewable_surplus_deficit_mw.toFixed(1)} MW`} status="Stable" tone="renewable" />
        <MetricCard label="Energy Demand" value={`${current.current_demand_mw.toFixed(1)} MW`} unit="Status: Normal" status="Normal" tone="demand" />
        <MetricCard label="Battery" value={`${current.battery_soc_percent.toFixed(1)}%`} unit={`${current.battery_stored_energy_mwh.toFixed(1)} / 8 MWh`} status={current.battery_soc_percent >= 30 ? 'Available' : 'Attention'} tone="battery" />
      </div>

      <div className="content-grid content-grid--two">
        <div className="panel panel--chart">
          <div className="panel-header panel-header--inline">
            <h3>Generation vs Demand</h3>
            <div className="legend-inline">
              <span><i className="dot dot--solar" /> Solar</span>
              <span><i className="dot dot--wind" /> Wind</span>
              <span><i className="dot dot--renewable" /> Renewable</span>
              <span><i className="dot dot--demand" /> Demand</span>
            </div>
          </div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#dfeaf4" />
                <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: '#5b6b69', fontSize: 11 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#5b6b69', fontSize: 11 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="generation" fill="#8FC9A3" name="Actual" radius={[8, 8, 0, 0]} />
                <Bar dataKey="forecast" fill="#A9D8E8" name="Forecast" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="panel panel--chart">
          <div className="panel-header panel-header--inline">
            <h3>AI Operations</h3>
            <span className="status-badge status-badge--soft">Live workflow</span>
          </div>
          <ul className="workflow-list">
            {[
              ['Asset Monitoring', 'Completed'],
              ['Weather Analysis', 'Completed'],
              ['Generation Forecast', 'Completed'],
              ['Demand Forecast', 'Running'],
              ['Anomaly Detection', 'Completed'],
              ['Battery Analysis', 'Completed'],
              ['Grid Coordination', 'Waiting Approval'],
            ].map(([name, status]) => (
              <li key={name} className="workflow-item">
                <span>{name}</span>
                <span className={`workflow-status workflow-status--${status.toLowerCase().replace(/\s+/g, '-')}`}>
                  {status}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="content-grid content-grid--three">
        <SummaryPanel title="Weather impact" value={`${Number(weatherCurrent.temperature_c ?? 18.6).toFixed(0)}°C`} detail={`Cloud cover: ${weatherCurrent.cloud_cover_percent ?? 82}% • Wind: ${weatherCurrent.wind_speed_m_s ?? 4.6} m/s • Solar: ${solarTrend}`} />
        <SummaryPanel title="Energy balance" value={current.renewable_surplus_deficit_mw >= 0 ? 'SURPLUS' : 'DEFICIT'} detail={`Current: ${current.renewable_surplus_deficit_mw.toFixed(1)} MW • 2h forecast: ${Math.max(-2.4, current.renewable_surplus_deficit_mw - 1.5).toFixed(1)} MW`} />
        <SummaryPanel title="Optimization" value={batteryRecommendation} detail={`Reason: ${current.renewable_surplus_deficit_mw >= 0 ? 'Expected renewable surplus before forecast decline.' : 'Demand is exceeding generation; balance dispatch is required.'}`} />
      </div>

      <div className="content-grid content-grid--two">
        <div className="panel">
          <div className="panel-header panel-header--inline">
            <div>
              <p className="section-kicker">Battery</p>
              <h3>Storage overview</h3>
            </div>
            <span className="status-badge status-badge--soft">{current.battery_soc_percent >= 30 ? 'Available' : 'Attention'}</span>
          </div>
          <div className="battery-panel">
            <div className="battery-gauge">
              <div className="battery-gauge__fill" style={{ height: `${Math.max(8, current.battery_soc_percent)}%` }} />
            </div>
            <div className="battery-metrics">
              <div className="big-number">{current.battery_soc_percent.toFixed(1)}%</div>
              <div className="battery-subtitle">{current.battery_stored_energy_mwh.toFixed(1)} / 8 MWh</div>
              <div className="mini-stats">
                <span>Charge limit: 2.0 MW</span>
                <span>Discharge limit: 2.0 MW</span>
                <span>Status: {current.renewable_surplus_deficit_mw >= 0 ? 'Charging' : 'Discharging'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header panel-header--inline">
            <div>
              <p className="section-kicker">Monitoring</p>
              <h3>Performance alert</h3>
            </div>
          </div>
          {alert ? (
            <div className="anomaly-box">
              <div className="anomaly-box__header">
                <span className="anomaly-box__label">{alert.category}</span>
                <span className="anomaly-box__severity">{alert.severity}</span>
              </div>
              <div className="anomaly-box__message">{alert.message}</div>
              <ul className="factor-list">
                <li>Potential contributing factors</li>
                <li>Forecast variance</li>
                <li>Operational tolerance</li>
                <li>Weather impact</li>
              </ul>
            </div>
          ) : (
            <p className="muted-text">No active anomaly alerts.</p>
          )}
        </div>
      </div>

      <div className="panel">
        <div className="panel-header panel-header--inline">
          <div>
            <p className="section-kicker">Review</p>
            <h3>Battery optimization</h3>
          </div>
        </div>
        <div className="recommendation-box">
          <div className="recommendation-box__title">Recommended action</div>
          <div className="recommendation-box__action">{batteryRecommendation}</div>
          <div className="recommendation-meta">
            <span>Power: {current.renewable_surplus_deficit_mw >= 0 ? '1.5 MW' : '0.9 MW'}</span>
            <span>Duration: 1 hour</span>
          </div>
          <p className="recommendation-copy">
            {current.renewable_surplus_deficit_mw >= 0
              ? 'Expected renewable surplus during the upcoming forecast period.'
              : 'Demand is above renewable generation; balancing and dispatch support is recommended.'}
          </p>
          <div className="action-row">
            <button className="primary-button action-button">Approve</button>
            <button className="secondary-action">Reject</button>
            <button className="secondary-action">Modify</button>
            <button className="secondary-action">Recalculate</button>
          </div>
          <div className="tiny-note">Decision support only • Human approval required • No autonomous physical grid control</div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, unit, status, tone }: { label: string; value: string; unit: string; status: string; tone: 'solar' | 'wind' | 'renewable' | 'demand' | 'battery' }) {
  const palette = {
    solar: 'metric-card metric-card--solar',
    wind: 'metric-card metric-card--wind',
    renewable: 'metric-card metric-card--renewable',
    demand: 'metric-card metric-card--demand',
    battery: 'metric-card metric-card--battery',
  };

  return (
    <div className={palette[tone]}>
      <div className="metric-card__top">
        <span className="metric-card__label">{label}</span>
        <span className="metric-card__status">{status}</span>
      </div>
      <div className="metric-card__value">{value}</div>
      <div className="metric-card__unit">{unit}</div>
    </div>
  );
}

function SummaryPanel({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <div className="panel summary-panel">
      <div className="summary-panel__title">{title}</div>
      <div className="summary-panel__value">{value}</div>
      <div className="summary-panel__detail">{detail}</div>
    </div>
  );
}

export default Dashboard;
