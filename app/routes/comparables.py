from fastapi import APIRouter, HTTPException
from typing import List
from app.comparables.comparable_agents import find_comparables
from app.data_extraction.cook import extract_properties as extract_cook
from app.data_extraction.dallas import extract_properties as extract_dallas
from app.data_extraction.la import extract_properties as extract_la  # if done
from pydantic import BaseModel

router = APIRouter()


class Property(BaseModel):
    square_feet: float = None
    zoning: str = None
    year_built: int = None
    property_type: str = None


@router.post("/comparable")
def get_comparables(property: Property):
    # Load data from all counties (in-memory, but could be cached or DB)
    data = extract_cook() + extract_dallas()  # + extract_la() if implemented
    if not data:
        raise HTTPException(status_code=500, detail="No property data available")

    result = find_comparables(property.dict(), data)
    return {"comparables": result}
