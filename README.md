# 🏈 Fantasy Football Draft Tool

A modular service-oriented application for fantasy football player evaluation and draft strategy, integrating sportsbook odds and projection engines.

## 🚀 Project Structure

services/
├── sportsbook-ingestion/      # Scrapes sportsbook lines (e.g., player props)
├── projection-engine/         # Processes projections for fantasy players
frontend/                      # Vite + React front-end for interacting with data

---

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js + npm
- Docker & Docker Compose

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fantasy-football-draft-tool.git
cd fantasy-football-draft-tool
```

### 2. Run Backends via Docker

Make sure Docker is running, then:

```bash
docker-compose up --build sportsbook-ingestion projection-engine
```

Flask APIs for sportsbook ingestion and projections will be available at:
	•	http://localhost:5001/props/<player-name>
	•	http://localhost:5002/projections

### 3. Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

The app should be running at: http://localhost:5173


### Testing Endpoints

Example:
```bash
curl http://localhost:5001/props/jalen-hurts
```