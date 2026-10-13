from flask import Flask, render_template, request, jsonify
from pathlib import Path
import csv, json, urllib.parse, urllib.request
app = Flask(__name__)
BASE = Path(__file__).resolve().parent
DATA = BASE / 'data' / 'raw' / 'fertilizer.csv'
with DATA.open(newline='', encoding='utf-8') as f:
    CROP_ROWS = list(csv.DictReader(f))

SOIL_INFO = {
 'Clay': ('Holds water and nutrients well; may drain slowly.', 'Rice, wheat, cotton (if drainage is adequate)', 'Improve structure with organic matter; avoid working when very wet.'),
 'Black': ('Clay-rich soil with strong moisture retention.', 'Cotton, chickpea, some cereals', 'Check drainage and avoid over-irrigation.'),
 'Red': ('Often lower in organic matter; nutrients can leach.', 'Groundnut, millet, pulses', 'Add compost and split nutrient applications.'),
 'Sandy loam': ('Drains well but can dry out quickly.', 'Groundnut, maize, potato, vegetables', 'Use mulch and smaller, more frequent irrigation.'),
 'Loamy': ('Balanced drainage and moisture retention; broadly versatile.', 'Wheat, maize, pulses, vegetables', 'Maintain organic matter and confirm nutrients with a soil test.'),
 'Sandy': ('Fast draining and often low in nutrient retention.', 'Groundnut, millet; selected crops with careful irrigation', 'Use compost, mulch and split fertilizer applications.'),
 'Unknown': ('Soil texture not confirmed.', 'Get a soil test before choosing a crop.', 'Use a local soil-testing service to confirm texture, pH and nutrients.')
}
CROP_INFO = {
 'Rice': ('🌾','Kharif','Clay or loamy','High','Warm conditions and dependable water; avoid uncontrolled standing water where not recommended.'),
 'Wheat': ('🌾','Rabi','Loamy or clay with drainage','Medium','Cool growing season and timely irrigation.'),
 'Maize': ('🌽','Kharif / Rabi by region','Loamy or sandy loam','Medium','Warm weather, sunlight and good drainage.'),
 'Cotton': ('☁️','Kharif','Black or well-drained loamy','Medium','Long warm season; avoid waterlogging.'),
 'Groundnut': ('🥜','Kharif','Sandy loam or red','Low','Warm conditions and loose, well-drained soil.'),
 'Chickpea': ('🫘','Rabi','Loamy or black with drainage','Low','Cool, relatively dry season; avoid waterlogging.'),
 'Tomato': ('🍅','Year-round in suitable regions','Loamy or sandy loam','Medium','Full sun, steady moisture and support/staking as needed.'),
 'Potato': ('🥔','Rabi in many regions','Loamy or sandy loam','Medium','Cooler conditions and loose soil; avoid waterlogging.'),
 'Millet': ('🌱','Kharif','Red or sandy loam','Low','Often suitable for lower-rainfall conditions; local variety matters.')
}
def fnum(v, default=0):
    if v is None or str(v).strip() == '': return default
    try: return float(v)
    except (TypeError, ValueError): return default

def recommend(data):
    soil = data.get('soil_type','Loamy')
    ph = fnum(data.get('ph'), 6.5)
    n,p,k = (fnum(data.get(x), None) for x in ('nitrogen','phosphorus','potassium'))
    season = data.get('season','Any')
    water = data.get('water','Medium')
    candidates=[]
    for crop, info in CROP_INFO.items():
        rows=[r for r in CROP_ROWS if r['crop']==crop]
        profile=rows[0] if rows else None
        score=50
        reasons=[]
        soils=[r['soil_type'] for r in rows]
        if soil in soils: score+=22; reasons.append('soil texture is a match')
        elif soil in ('Loamy','Sandy loam') and any(s in soils for s in ('Loamy','Sandy loam')): score+=10; reasons.append('soil texture is reasonably suitable')
        else: score-=4
        if profile and fnum(profile['ph_min']) <= ph <= fnum(profile['ph_max']): score+=18; reasons.append('pH is within the listed range')
        else: score-=12; reasons.append('pH may need correction or local advice')
        if season=='Any' or season.lower() in info[1].lower() or info[1]=='Year-round': score+=8
        else: score-=5
        need=info[3]
        if water=='Any' or water==need: score+=6
        elif (water=='Low' and need=='High') or (water=='High' and need=='Low'): score-=8
        score=max(20,min(98,score))
        targets = [fnum(profile[x]) if profile else 0 for x in ('nitrogen_target','phosphorus_target','potassium_target')]
        measured=[n,p,k]
        labels=['Nitrogen (N)','Phosphorus (P)','Potassium (K)']
        gaps=[]
        for label, current, target in zip(labels, measured, targets):
            if current is None: continue
            if current < target*.75: gaps.append(f'{label} appears low compared with a general crop reference')
            elif current > target*1.25: gaps.append(f'{label} is already high compared with a general crop reference')
        fertilizer=[]
        if profile:
            for short, current, target in zip(('N','P₂O₅','K₂O'), measured, targets):
                if current is None: continue
                if current < target*.75: fertilizer.append(f'Prioritize checking {short} supply; use a soil-test-based fertilizer dose.')
                elif current > target*1.25: fertilizer.append(f'Avoid adding extra {short} until a soil test confirms need.')
        if not fertilizer:
            if all(v is None for v in measured): fertilizer=['Enter lab-tested N-P-K values to see nutrient comparison; without them, use soil-test guidance.']
            else: fertilizer=['No clear N-P-K issue detected from the entered values; confirm a balanced dose using a soil test.']
        candidates.append({'crop':crop,'emoji':info[0],'score':score,'season':info[1],'soil':info[2],'water':need,'description':info[4],'reasons':reasons,'fertilizer':fertilizer,'gaps':gaps})
    candidates.sort(key=lambda x:x['score'], reverse=True)
    return candidates[:3]

@app.route('/')
def home():
    return render_template('index.html', crops=CROP_INFO, soils=SOIL_INFO)

@app.route('/recommend', methods=['GET','POST'])
def recommend_page():
    results=None; formdata={}
    if request.method=='POST':
        formdata=request.form.to_dict()
        results=recommend(formdata)
    return render_template('recommend.html', results=results, formdata=formdata, soils=SOIL_INFO)

@app.route('/crops')
def crops(): return render_template('crops.html', crops=CROP_INFO)

@app.route('/soil-guide')
def soil_guide(): return render_template('soil.html', soils=SOIL_INFO)

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data=request.get_json(silent=True) or request.form.to_dict()
    return jsonify({'recommendations': recommend(data), 'note':'Indicative guidance only. Confirm crop and fertilizer rates with a local agricultural extension officer and soil test.'})

@app.route('/api/weather')
def weather():
    city=request.args.get('city','').strip()
    if not city: return jsonify({'error':'Enter a town or city name.'}), 400
    try:
        q=urllib.parse.urlencode({'name':city,'count':1,'language':'en','format':'json'})
        req=urllib.request.Request('https://geocoding-api.open-meteo.com/v1/search?'+q, headers={'User-Agent':'SoilWise/1.0'})
        with urllib.request.urlopen(req, timeout=6) as r: geo=json.load(r)
        places=geo.get('results') or []
        if not places: return jsonify({'error':'Location not found. Try a nearby town.'}),404
        place=places[0]
        q=urllib.parse.urlencode({'latitude':place['latitude'],'longitude':place['longitude'],'current':'temperature_2m,relative_humidity_2m,precipitation,weather_code','timezone':'auto'})
        req=urllib.request.Request('https://api.open-meteo.com/v1/forecast?'+q, headers={'User-Agent':'SoilWise/1.0'})
        with urllib.request.urlopen(req, timeout=6) as r: wx=json.load(r)
        return jsonify({'place':', '.join(x for x in [place.get('name'),place.get('admin1'),place.get('country')] if x), 'current':wx.get('current',{}), 'units':wx.get('current_units',{})})
    except Exception:
        return jsonify({'error':'Live weather is temporarily unavailable. Check your internet connection and try again.'}), 502

@app.route('/health')
def health(): return jsonify({'status':'ok','service':'SoilWise crop and fertilizer guidance'})

if __name__=='__main__': app.run(debug=True, host='127.0.0.1', port=5000)
