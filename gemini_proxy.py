import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
GEMINI_VISION_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent'

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

def gemini_vision_query(prompt, image_data):
    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}
    data = {
        'contents': [{
            'parts': [{'text': prompt}],
            'inlineData': [{
                'mimeType': 'image/jpeg',
                'data': image_data
            }]
        }]
    }
    resp = requests.post(GEMINI_VISION_URL, headers=headers, params=params, json=data)
    if resp.status_code == 200:
        try:
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return 'No response from Gemini Vision.'
    else:
        return f'Gemini Vision API error: {resp.status_code} {resp.text}'

@app.route('/api/gemini/analyze', methods=['POST'])
def analyze():
    events = request.json.get('events', [])
    
    if not events:
        return jsonify({'result': 'No events to analyze. Please add some events first.'})
    
    # Create a detailed prompt for event analysis
    prompt = f"""As an energy consultant, analyze these recent events from a chemical energy facility dashboard:

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
6. Resource Allocation Recommendations
7. Asset Protection Strategies

Include specific timelines, risk scores, and cost estimates where possible. Focus on preventing costly failures and optimizing maintenance budgets."""

    result = gemini_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/photo-analysis', methods=['POST'])
def photo_analysis():
    try:
        data = request.json
        image_data = data.get('image')  # Base64 encoded image
        asset_context = data.get('assets', [])
        
        if not image_data:
            return jsonify({'error': 'No image data provided'})
        
        # Remove data URL prefix if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        prompt = f"""Analyze this inspection photo from a chemical energy facility and provide intelligent tagging and analysis.

ASSET CONTEXT:
{asset_context}

Please provide:
1set Identification
2. Visual Inspection Findings
3. Potential Issues or Concerns
4. Compliance Implications
5. Recommended Actions
6. Risk Assessment
7. Maintenance Recommendations

Be specific about what you observe and provide actionable insights for facility management."""

        result = gemini_vision_query(prompt, image_data)
        return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'error': f'Photo analysis failed: {str(e)}'})

@app.route('/api/gemini/pdf-content', methods=['POST'])
def pdf_content():
    events = request.json.get('events', [])
    compliance = request.json.get('compliance')
    cost = request.json.get('cost')
    assets = request.json.get('assets', [])
    
    prompt = f"""Generate comprehensive content for a professional compliance report PDF for a chemical energy facility.

FACILITY DATA:
- Compliance Rate: {compliance}%
- Current Cost: ${cost}M
- Recent Events: {events}
- Assets: {assets}

Please provide a structured report with the following sections:

1. EXECUTIVE SUMMARY
   - Key findings and recommendations
   - Overall facility status

2. COMPLIANCE ANALYSIS
   - Current compliance status
   - Regulatory requirements met/missed
   - Compliance trends and gaps
   - Risk assessment

3. OPERATIONAL PERFORMANCE
   - Asset health overview
   - Event analysis and patterns
   - Performance metrics
4. COST ANALYSIS
   - Budget vs actual spending
   - Cost efficiency metrics
   - ROI on maintenance activities

5. RISK ASSESSMENT
   - Identified risks and severity
   - Mitigation strategies
   - Priority actions

6. RECOMMENDATIONS
   - Immediate actions (next 30s)
   - Short-term improvements (3-6 months)
   - Long-term strategic initiatives

7ICES
   - Detailed asset status
   - Event timeline
   - Compliance checklist

Format this as a professional report suitable for regulatory submission and executive review."""

    result = gemini_query(prompt)
    return jsonify({'result': result})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
