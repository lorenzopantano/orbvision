# OrbitalVision API

🚀 **OrbitalVision** is an open-source project to simulate and visualize satellite orbits.  
This repository contains the **backend API**, built with **Python + FastAPI**, which fetches and processes orbital data (TLEs) for the frontend visualization.

---

## 🧰 Features

- Fetch real-time TLE (Two-Line Element) satellite data from public sources (Celestrak)
- Parse and process TLE data for orbital calculations
- Provide REST API endpoints for frontend consumption
- Ready for caching, orbit propagation, and future ML/physics modules

---

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI** – High-performance web framework
- **httpx** – Async HTTP requests
- **python-dotenv** – Environment variables management
- **Uvicorn** – ASGI server

---

## ⚡ Getting Started (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/lorenzopantano/orbitalvision.git
cd orbitalvision/backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run FastAPI Server

```bash
uvicorn app.main:app --reload
