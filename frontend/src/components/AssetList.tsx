import { useState, useEffect } from 'react'
import { assetApi } from '../services/api'
import type { Asset } from '../types'

function AssetList() {
  const [assets, setAssets] = useState<Asset[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadAssets()
  }, [])

  const loadAssets = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await assetApi.getAll()
      setAssets(data)
    } catch (err) {
      setError('Failed to load assets')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="panel">
      <div className="panel-header panel-header--inline">
        <div>
          <p className="section-kicker">Portfolio</p>
          <h2>Renewable Assets</h2>
        </div>
        <button onClick={loadAssets} className="primary-button secondary-button">
          Refresh
        </button>
      </div>

      {loading && <p className="muted-text">Loading assets...</p>}
      {error && <div className="alert alert--error">{error}</div>}
      {!loading && !error && assets.length === 0 && (
        <p className="muted-text">No assets found. Create some assets to get started.</p>
      )}
      {!loading && !error && assets.length > 0 && (
        <div className="table-wrap">
          <table className="asset-table">
            <thead>
              <tr>
                <th>Asset ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Capacity (MW)</th>
                <th>Status</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {assets.map((asset) => (
                <tr key={asset.id}>
                  <td>{asset.asset_id}</td>
                  <td>{asset.name}</td>
                  <td className="capitalize">{asset.asset_type}</td>
                  <td>{asset.installed_capacity_mw}</td>
                  <td>
                    <span className={`tag ${
                      asset.operational_status === 'operational' ? 'tag--success' :
                      asset.operational_status === 'maintenance' ? 'tag--warning' :
                      'tag--danger'
                    }`}>
                      {asset.operational_status}
                    </span>
                  </td>
                  <td>{asset.location || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default AssetList
