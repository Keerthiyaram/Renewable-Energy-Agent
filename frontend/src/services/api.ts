import axios from 'axios'
import type { Asset, HealthStatus } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const healthApi = {
  check: async (): Promise<HealthStatus> => {
    const response = await api.get('/health')
    return response.data
  },
}

export const assetApi = {
  getAll: async (): Promise<Asset[]> => {
    const response = await api.get('/assets/')
    return response.data
  },

  getById: async (assetId: string): Promise<Asset> => {
    const response = await api.get(`/assets/${assetId}`)
    return response.data
  },

  create: async (asset: Omit<Asset, 'id' | 'created_at' | 'updated_at'>): Promise<Asset> => {
    const response = await api.post('/assets/', asset)
    return response.data
  },

  update: async (assetId: string, asset: Partial<Asset>): Promise<Asset> => {
    const response = await api.put(`/assets/${assetId}`, asset)
    return response.data
  },

  delete: async (assetId: string): Promise<void> => {
    await api.delete(`/assets/${assetId}`)
  },
}

export const uploadApi = {
  upload: async (file: File, assetType = 'solar', capacityMw = 10): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_URL}/energy/upload?asset_type=${encodeURIComponent(assetType)}&capacity_mw=${capacityMw}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default api
