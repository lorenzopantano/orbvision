from fastapi import FastAPI

app = FastAPI(
    title="OrbitalVision API",
    version="0.1.0",
    description="Backend for orbital data visualization and analysis"
)

# Include API Routes
# app.include_router(tle.router, prefix="api/tle", tags=["TLE"])

@app.get("/")
def root():
    return { "message": "Welcome to OrbitalVision API 🛰️"}