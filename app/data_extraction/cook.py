import requests
from typing import List, Dict
from datetime import datetime

ENDPOINT = "https://datacatalog.cookcountyil.gov/resource/bcnq-qi2z.json"
CURRENT_YEAR = datetime.now().year

INDUSTRIAL_CLASSES = {"235", "240", "241", "300", "310", "320", "330"}  # Example

def extract_properties(limit=1000) -> List[Dict]:
    try:
        data = requests.get(ENDPOINT, params={"$limit": limit}, timeout=10).json()
    except Exception as e:
        print(f"[Cook Extractor] Error fetching data: {e}")
        return []

    results = []

    for row in data:
        class_code = row.get("class", "")
        modeling_group = (row.get("modeling_group") or "").upper()
        use_code = str(row.get("use_1") or "")

        if not (
            any(code in class_code for code in INDUSTRIAL_CLASSES) or
            modeling_group == "MF" or
            use_code == "2"
        ):
            continue

        results.append({
            "source": "cook_county",
            "external_id": row.get("property_index_number"),
            "address": row.get("addr"),
            "zoning": class_code,
            "property_type": modeling_group,
            "square_feet": try_cast_float(row.get("bldg_sf")),
            "acres": None,
            "year_built": derive_year_built(row.get("age")),
            "sale_price": try_cast_float(row.get("most_recent_sale_price")),
            "latitude": try_cast_float(row.get("centroid_y")),
            "longitude": try_cast_float(row.get("centroid_x")),
            "garage": try_cast_int(row.get("garage_indicator")) == 1,
            "vacant": None,
            "valuation_current": None,
            "owner_name": None,
        })

    return results

def try_cast_float(val):
    try:
        return float(val)
    except:
        return None

def try_cast_int(val):
    try:
        return int(val)
    except:
        return None

def derive_year_built(age):
    try:
        return CURRENT_YEAR - int(age)
    except:
        return None