from fastapi import FastAPI
from app.api.routes import gp

app = FastAPI(
    title="OrbitalVision API",
    version="0.1.0",
    description="Backend for orbital data visualization and analysis"
)

# Include API Routes
app.include_router(gp.router, prefix="/api/gp", tags=["GP"])

# @app.get("/")
# def root():
#     return { "message": "Welcome to OrbitalVision API 🛰️"}