import { useState, useEffect } from "react";
import { healthApi } from "../services/api";
import type { HealthStatus } from "../types";

function HealthCheck() {
    const [health, setHealth] = useState<HealthStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        checkHealth();
    }, []);

    const checkHealth = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await healthApi.check();
            setHealth(data);
        } catch (err) {
            setError("Failed to connect to backend");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="panel panel--compact">
            <div className="panel-header panel-header--inline">
                <div>
                    <p className="section-kicker">Operations</p>
                    <h2>System Health</h2>
                </div>
                <button onClick={checkHealth} className="primary-button secondary-button">
                    Refresh
                </button>
            </div>
            {loading && <p className="muted-text">Checking backend status...</p>}
            {error && <div className="alert alert--error">{error}</div>}
            {health && (
                <div className="status-grid">
                    <div className="status-row">
                        <span className="status-label">Status:</span>
                        <span
                            className={`status-pill ${
                                health.status === "healthy" ? "status-pill--success" : "status-pill--danger"
                            }`}
                        >
                            {health.status}
                        </span>
                    </div>
                    <div className="status-row">
                        <span className="status-label">Service:</span>
                        <span className="status-value">{health.service}</span>
                    </div>
                    <div className="status-row">
                        <span className="status-label">Environment:</span>
                        <span className="status-value">{health.environment}</span>
                    </div>
                </div>
            )}
        </div>
    );
}

export default HealthCheck;
