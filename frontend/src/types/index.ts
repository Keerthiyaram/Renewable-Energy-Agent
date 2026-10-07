export interface Asset {
  id: number
  asset_id: string
  name: string
  asset_type: string
  installed_capacity_mw: number
  location?: string
  latitude?: number
  longitude?: number
  operational_status: string
  commissioning_date?: string
  configuration?: string
  created_at: string
  updated_at?: string
}

export interface HealthStatus {
  status: string
  service: string
  environment: string
}
