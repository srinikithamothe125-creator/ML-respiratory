from app import app

def test_home():
    app.testing=True
    with app.test_client() as c:
        assert c.get('/').status_code == 200
        assert c.get('/recommend').status_code == 200
        assert c.get('/crops').status_code == 200
        assert c.get('/soil-guide').status_code == 200
        assert c.get('/health').json['status'] == 'ok'

def test_api_recommend():
    app.testing=True
    with app.test_client() as c:
        r=c.post('/api/recommend', json={'soil_type':'Loamy','ph':6.5,'season':'Rabi','water':'Medium','nitrogen':40,'phosphorus':20,'potassium':30})
        assert r.status_code == 200
        assert len(r.json['recommendations']) == 3
