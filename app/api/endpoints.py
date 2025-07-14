from fastapi import APIRouter
from app.data_extraction import cook, la, dallas

router = APIRouter()

@router.get("/extract/cook")
def extract_cook_data():
    data = cook.extract_properties(limit=1000)
    return {
        "count": len(data),
        "sample": data[:5]
    }

@router.get("/extract/la")
def extract_la_data():
    data = la.extract_properties(limit=1000)
    return {
        "count": len(data),
        "sample": data[:5]
    }

@router.get("/extract/dallas")
def extract_dallas_data():
    data = dallas.extract_properties(limit=1000)
    return {
        "count": len(data),
        "sample": data[:5]
    }
