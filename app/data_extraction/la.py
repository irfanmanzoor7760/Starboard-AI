import csv
from typing import List, Dict

CSV_PATH = "app/data/Los_Angeles_County_Housing_Element_(2021-2029)_-_Rezoning.csv"  # Update to your actual CSV path


def extract_properties(limit: int = 1000) -> List[Dict]:
    rows = []

    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= limit:
                    break

                prop = {
                    "source": "la_county",
                    "external_id": row.get("ain"),
                    "address": row.get("SiteAddress"),
                    "zoning": row.get("Zoning1"),
                    "property_type": row.get("usetype"),
                    "square_feet": None,
                    "acres": try_cast_float(row.get("Acres")),
                    "year_built": try_cast_int(row.get("MaxYear")),
                    "sale_price": None,
                    "latitude": None,
                    "longitude": None,
                    "garage": None,
                    "vacant": row.get("Vacant_Use") == "Vacant",
                    "valuation_current": try_cast_float(row.get("Realistic_Capacity")),
                    "owner_name": None,
                }

                if prop["property_type"] and "industrial" in prop["property_type"].lower():
                    rows.append(prop)

    except Exception as e:
        print(f"[LA Extractor] Failed to read CSV: {e}")

    return rows


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
