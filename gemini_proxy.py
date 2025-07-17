import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

if not GEMINI_API_KEY:
    raise RuntimeError('GEMINI_API_KEY environment variable not set!')

def gemini_query(prompt):
    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}
    data = {
        'contents': [{
            'parts': [{'text': prompt}]
        }]
    }
    resp = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if resp.status_code == 200:
        try:
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return 'No response from Gemini.'
    else:
        return f'Gemini API error: {resp.status_code} {resp.text}'

@app.route('/api/gemini/analyze', methods=['POST'])
def analyze():
    events = request.json.get('events', [])
    prompt = f"Analyze these recent events for risks, trends, and recommendations (short summary):\n{events}"
    result = gemini_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/report', methods=['POST'])
def report():
    events = request.json.get('events', [])
    compliance = request.json.get('compliance')
    cost = request.json.get('cost')
    prompt = f"Generate a compliance and cost report based on these events: {events}, compliance: {compliance}, cost: {cost}."
    result = gemini_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/predict', methods=['POST'])
def predict():
    assets = request.json.get('assets', [])
    prompt = f"Predict maintenance needs and risks for these assets: {assets}."
    result = gemini_query(prompt)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
