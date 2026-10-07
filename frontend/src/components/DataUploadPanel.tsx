import { ChangeEvent, useState } from 'react';
import { uploadApi } from '../services/api';

function DataUploadPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [assetType, setAssetType] = useState('solar');
  const [capacityMw, setCapacityMw] = useState(10);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selected = event.target.files?.[0] ?? null;
    setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please choose a CSV or Excel file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await uploadApi.upload(file, assetType, capacityMw);
      setResult(response);
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <p className="section-kicker">Input</p>
          <h3>Data Ingestion</h3>
        </div>
      </div>

      <div className="upload-grid">
        <label className="field">
          <span>Asset type</span>
          <select value={assetType} onChange={(e) => setAssetType(e.target.value)}>
            <option value="solar">solar</option>
            <option value="wind">wind</option>
            <option value="battery">battery</option>
          </select>
        </label>

        <label className="field">
          <span>Capacity (MW)</span>
          <input
            type="number"
            value={capacityMw}
            onChange={(e) => setCapacityMw(Number(e.target.value) || 0)}
            min="0.1"
            step="0.1"
          />
        </label>

        <label className="field">
          <span>File</span>
          <input type="file" accept=".csv,.xlsx,.xls" onChange={handleChange} />
        </label>
      </div>

      <button
        onClick={handleUpload}
        disabled={loading || !file}
        className="primary-button"
      >
        {loading ? 'Uploading...' : 'Upload and Validate'}
      </button>

      {error && <div className="alert alert--error">{error}</div>}

      {result && (
        <div className="upload-summary">
          <div className="upload-summary__title">Upload summary</div>
          <div>Accepted rows: {result.processing_summary?.accepted ?? 0}</div>
          <div>Rejected rows: {result.processing_summary?.rejected ?? 0}</div>
          <div>Duplicate count: {result.duplicate_count ?? 0}</div>
          <div>File: {result.filename}</div>
          {result.validation_errors?.length > 0 && (
            <div className="upload-summary__errors">
              Errors: {result.validation_errors.map((item: any) => item.errors?.join(', ') ?? JSON.stringify(item)).join(' | ')}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default DataUploadPanel;
