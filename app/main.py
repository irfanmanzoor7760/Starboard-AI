from fastapi import FastAPI
from app.api import endpoints
from app.routes import comparables
app = FastAPI(title="Starboard Agent API")

app.include_router(endpoints.router)
app.include_router(comparables.router, tags=["Comparables"])
