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
    
    if not events:
        return jsonify({'result': 'No events to analyze. Please add some events first.'})
    
    # Create a detailed prompt for event analysis
    prompt = f"""energy consultant, analyze these recent events from a chemical energy facility dashboard:

EVENTS DATA:
{events}

Please provide a comprehensive analysis including:
1isk assessment and severity levels
2. Operational trends and patterns
3. Compliance implications
4. Recommended immediate actions
5. Long-term strategic recommendations

Focus on actionable insights that would help facility managers make informed decisions. Be specific about risks, costs, and compliance impacts."""

    result = gemini_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/report', methods=['POST'])
def report():
    events = request.json.get('events', [])
    compliance = request.json.get('compliance')
    cost = request.json.get('cost')
    
    prompt = f"""Generate a professional compliance and cost analysis report for a chemical energy facility:

FACILITY DATA:
- Compliance Rate: {compliance}%
- Current Cost: ${cost}M
- Recent Events: {events}

Please provide:
1. Executive Summary
2. Compliance Analysis (trends, gaps, recommendations)
3Cost Analysis (budget vs actual, efficiency metrics)
4. Risk Assessment
5. Action Items and Timeline
6. Regulatory Compliance Status

Format as a professional report with clear sections and actionable recommendations."""

    result = gemini_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/predict', methods=['POST'])
def predict():
    assets = request.json.get('assets', [])
    
    if not assets:
        return jsonify({'result': 'No assets to analyze. Please check asset data.'})
    
    prompt = f"""fictive maintenance AI specialist, analyze these energy facility assets:

ASSETS DATA:
{assets}

Please provide:
1. Asset Health Assessment (for each asset)
2. Failure Risk Predictions (probability and timeline)
3. Maintenance Priority Ranking
4. Recommended Maintenance Schedule
5. Cost-Benefit Analysis of Preventive vs Reactive Maintenance
6. Resource Allocation Recommendations7l Asset Protection Strategies

Include specific timelines, risk scores, and cost estimates where possible. Focus on preventing costly failures and optimizing maintenance budgets."""

    result = gemini_query(prompt)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
