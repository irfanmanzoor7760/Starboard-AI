import csv
from typing import List, Dict
from datetime import datetime

CSV_PATH = "app/data/DCAD2025_BPP_DETAIL_CURRENT.csv"  # Update to your actual CSV path
CURRENT_YEAR = datetime.now().year


def extract_properties(limit=1000) -> List[Dict]:
    rows = []

    try:
        with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= limit:
                    break

                prop_class = row.get("PROPERTY_CLASS", "")

                """if not is_industrial(prop_class):
                    continue"""

                prop = {
                    "source": "dallas_county",
                    "external_id": row.get("ACCOUNT_NUM") or row.get("GIS_NUM"),
                    "address": build_address(row),
                    "zoning": prop_class,
                    "property_type": row.get("BUSINESS_TYPE"),
                    "square_feet": try_cast_float(row.get("TOT_SF")),
                    "acres": None,
                    "year_built": derive_year_built(row.get("EFFECTIVE_AGE")),
                    "sale_price": None,
                    "latitude": None,
                    "longitude": None,
                    "garage": None,
                    "vacant": is_vacant(row),
                    "valuation_current": try_cast_float(row.get("TOT_VAL_CURRENT")),
                    "owner_name": row.get("OWNER_NAME")
                }

                rows.append(prop)

    except Exception as e:
        print(f"[Dallas Extractor] Failed to read CSV: {e}")

    return rows


def is_industrial(prop_class):
    if not prop_class:
        return False
    return any(code in prop_class.upper() for code in ["I", "M", "IND", "INDUSTRIAL", "MANUF", "WARE", "PLANT", "FACILITY"])


def is_vacant(row):
    return row.get("RENDERED_CURRENT_STATUS", "").upper() == "INACTIVE" or row.get("ACCT_STATUS", "").upper() == "INACTIVE"


def derive_year_built(effective_age):
    try:
        return CURRENT_YEAR - int(effective_age)
    except:
        return None


def try_cast_float(value):
    try:
        return float(value)
    except:
        return None


def build_address(row):
    parts = [
        row.get("STREET_NUM", "").strip(),
        row.get("STREET_DIR", "").strip(),
        row.get("STREET_NAME", "").strip(),
        row.get("STREET_SUFFIX", "").strip(),
        row.get("STREET_HALF_NUM", "").strip(),
        row.get("SUITE_NUMBER", "").strip(),
        row.get("CITY", "").strip()
    ]
    return " ".join([p for p in parts if p])
