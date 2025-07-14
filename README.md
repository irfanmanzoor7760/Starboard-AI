# 🏢 Starboard AI Agent Challenge

This project is a multi-county industrial property intelligence system that:

* Ingests and normalizes property data from disparate APIs and CSVs
* Extracts industrial properties
* Performs automated comparable analysis across counties

Built for **Starboard AI**’s Agent Engineer Challenge.

---

## 🚀 Features

### ✅ API Discovery & Ingestion

* Integrates property data from **Cook County (API)**, **Dallas County (CSV)**, and **Los Angeles (CSV)**
* Normalizes inconsistent field names across sources
* Identifies industrial-zoned properties using zoning/property class filters

### ✅ Data Extraction System

* Parses both JSON and CSV formats
* Filters for industrial-zoned properties (`M1`, `M2`, `I-1`, `I-2`, etc.)
* Handles missing data, validation, casting
* Flags vacant properties

### ✅ Comparable Discovery Agent

* Accepts a property and finds the **top N comparable industrial properties** by:

  * Square footage
  * Zoning
  * Year built
  * Type
* Returns confidence score per comparable

---

## 🧱 Tech Stack

* **Python 3.11**
* **FastAPI** — REST API framework
* **Uvicorn** — ASGI server
* **Pandas/CSV/JSON** — Data handling
* *(Optional: PostgreSQL integration possible)*

---

## 🗂 Project Structure

```bash
.
├── app/
│   ├── api/                 # API endpoints
│   ├── comparables/         # Comparable agent logic
│   ├── data_extraction/     # County-specific extractors
│   ├── main.py              # FastAPI app init
├── data/
│   ├── dallas_county.csv
│   ├── la_county.csv
├── requirements.txt
└── README.md
```

---

## 📦 Setup & Run

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Place Data Files

Place the following in the `/data/` folder:

* `dallas_county.csv`
* `la_county.csv` *(optional if not used)*

> The Cook County data is fetched live via HTTP.

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

Visit Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Test Endpoints

### 🔹 `/extract/cook`

Returns normalized industrial properties from Cook County (API)

### 🔹 `/extract/dallas`

Returns industrial properties from Dallas County CSV

### 🔹 `/comparable`

**POST**: Send a property and get comparables

#### Example Request:

```json
{
  "square_feet": 12000,
  "zoning": "M1",
  "year_built": 2005,
  "property_type": "Manufacturing"
}
```

---
