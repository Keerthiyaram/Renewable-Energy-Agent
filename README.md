# Renewable Energy Agent System

Agentic AI decision-support platform for renewable energy and grid operations.

## Project Overview

This system provides AI-powered decision support for renewable energy operators, including:
- Solar PV and wind turbine monitoring
- Battery energy storage optimization
- Weather intelligence integration
- Generation and demand forecasting
- Anomaly detection
- Grid coordination recommendations

**IMPORTANT SAFETY REQUIREMENT:** This is a DECISION-SUPPORT system only. The system does NOT autonomously control electrical grid infrastructure, switchgear, inverters, battery systems, or power-generation equipment. All operational recommendations require human/operator approval.

## Technology Stack

### Backend
- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL (with SQLite for development)
- Pandas, NumPy, SciPy
- scikit-learn
- LangGraph for multi-agent orchestration
- PuLP for optimization
- httpx for external API calls
- ReportLab for PDF generation

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Recharts
- Axios

## Project Structure

```
renewable-energy-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   ├── api/routes/          # API endpoints
│   │   ├── agents/              # AI agents
│   │   ├── graph/               # LangGraph workflow
│   │   ├── forecasting/         # ML forecasting models
│   │   ├── anomaly/             # Anomaly detection
│   │   ├── optimization/        # Battery optimization
│   │   ├── services/            # Business logic services
│   │   ├── database/            # Database configuration
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   └── prompts/             # LLM prompts
│   ├── data/                    # Data directories
│   ├── tests/                   # pytest tests
│   ├── scripts/                 # Utility scripts
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── hooks/               # Custom hooks
│   │   ├── types/               # TypeScript types
│   │   └── utils/               # Utility functions
│   ├── package.json             # Node dependencies
│   └── vite.config.ts           # Vite configuration
├── docs/                        # Documentation
└── README.md
```

## Phase 1 Setup Instructions

This is Phase 1 of the project, which includes:
- FastAPI backend with basic configuration
- Database models (RenewableAsset, EnergyMeasurement, Battery, WorkflowRun)
- Asset CRUD API endpoints
- Basic React frontend with health check and asset list
- Database seeding script
- Pytest tests

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd renewable-energy-agent/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. (Optional) Edit `.env` to configure settings:
```env
DATABASE_URL=sqlite:///./renewable_energy.db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

7. Initialize and seed the database:
```bash
python -c "from app.database.seed import seed_database; seed_database()"
```

8. Run the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd renewable-energy-agent/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. (Optional) Edit `.env` to configure API URL:
```env
VITE_API_URL=http://localhost:8000
```

5. Run the frontend development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Running Tests

1. Backend tests:
```bash
cd renewable-energy-agent/backend
pytest tests/ -v
```

2. With coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

### API Endpoints (Phase 1)

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /assets/` - Create asset
- `GET /assets/` - List all assets
- `GET /assets/{asset_id}` - Get specific asset
- `PUT /assets/{asset_id}` - Update asset
- `DELETE /assets/{asset_id}` - Delete asset

### Database Models (Phase 1)

- **RenewableAsset**: Solar, wind, and battery assets
- **EnergyMeasurement**: Time-series energy measurements
- **Battery**: Battery storage system details
- **WorkflowRun**: Workflow execution tracking

## Development Status

**Phase 1 - COMPLETE** (Current)
- ✅ Project structure
- ✅ Database models
- ✅ Asset CRUD API
- ✅ Basic React frontend
- ✅ Health check endpoint
- ✅ Database seeding
- ✅ Pytest tests

**Phase 2 - PENDING**
- Data ingestion (CSV, Excel, REST API)
- Data validation
- Energy balance calculations
- Battery constraint validation

**Phase 3 - PENDING**
- Weather API integration (Open-Meteo)
- Weather simulation fallback

**Phase 4 - PENDING**
- Solar generation forecasting (ML model)
- Wind generation forecasting (ML model)
- Demand forecasting (ML model)
- Forecast evaluation

**Phase 5 - PENDING**
- Anomaly detection (Isolation Forest)

**Phase 6 - PENDING**
- Battery optimization (PuLP/OR-Tools)

**Phase 7 - PENDING**
- Seven specialized AI agents
- Agent prompts

**Phase 8 - PENDING**
- LangGraph workflow orchestration
- Shared state management

**Phase 9 - PENDING**
- Critic/reviewer agent

**Phase 10 - PENDING**
- Human approval workflow

**Phase 11 - PENDING**
- Dynamic replanning

**Phase 12 - PENDING**
- Complete API endpoints

**Phase 13 - PENDING**
- Full React dashboard

**Phase 14 - PENDING**
- AI Operations Center

**Phase 15 - PENDING**
- PDF report generation

**Phase 16 - PENDING**
- Eight automated test scenarios

**Phase 17 - PENDING**
- Docker configuration

**Phase 18 - PENDING**
- Deployment configuration

## Contributing

This is a phased development project. Please follow the phase sequence and ensure all tests pass before proceeding to the next phase.

## License

Proprietary - Internal Use Only
