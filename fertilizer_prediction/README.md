# SoilWise — Soil, Crop & Fertilizer Guidance

A focused Flask website for crop suitability guidance from soil type, pH, season, water availability and optional N-P-K values. It includes crop and soil guides plus optional live current weather lookup via Open-Meteo (internet required).

## Run on macOS
1. Extract the ZIP.
2. In Terminal, `cd` into the extracted `fertilizer_prediction` folder.
3. Run `python3 -m venv .venv`
4. Run `source .venv/bin/activate`
5. Run `python -m pip install -r requirements.txt`
6. Run `python app.py`
7. Open http://127.0.0.1:5000

## Pages
- Home and current weather lookup
- Soil-based crop shortlist
- Crop guide
- Soil guide
- JSON endpoint: POST `/api/recommend`
- Health endpoint: GET `/health`

## Data and limitations
`data/raw/fertilizer.csv` contains small, illustrative crop reference values used by the guidance rules. They are not official fertilizer prescriptions and should not be used to calculate field application rates. Recommendations are indicative, not a validated ML model, and must be checked against a laboratory soil test and local agricultural extension advice. Live weather uses the no-key Open-Meteo geocoding and forecast APIs and may be unavailable without internet.
