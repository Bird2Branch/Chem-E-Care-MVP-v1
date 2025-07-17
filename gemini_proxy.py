import os
from flask import Flask, request, jsonify, make_response
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import time

# Load environment variables from .env file (for local development).
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow all origins for debugging CORS issues

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

if not OPENROUTER_API_KEY:
    raise RuntimeError('OPENROUTER_API_KEY environment variable not set!')

def openrouter_query(prompt):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'deepseek/deepseek-chat:free',
        'messages': [
            {'role': 'user', 'content': prompt}
        ]
    }
    print("Calling OpenRouter API from openrouter_query...")
    start = time.time()
    resp = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=15)
    elapsed = time.time() - start
    print(f"OpenRouter API call finished in {elapsed:.2f} seconds with status {resp.status_code}")
    if resp.status_code == 200:
        try:
            return resp.json()['choices'][0]['message']['content']
        except Exception:
            return 'No response from OpenRouter.'
    else:
        return f'OpenRouter API error: {resp.status_code} {resp.text}'

@app.route('/api/gemini/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    events = data.get('events', [])
    if not events:
        return jsonify({'result': 'No events to analyze. Please add some events first.'})
    prompt = f"""As an energy consultant, analyze these recent events from a chemical energy facility dashboard:\n\nEVENTS DATA:\n{events}\n\nPlease provide a comprehensive analysis including:\n1. Risk assessment and severity levels\n2. Operational trends and patterns\n3. Compliance implications\n4. Recommended immediate actions\n5. Long-term strategic recommendations\n\nFocus on actionable insights that would help facility managers make informed decisions. Be specific about risks, costs, and compliance impacts."""
    result = openrouter_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/report', methods=['POST', 'OPTIONS'])
def report():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json() or {}
    events = data.get('events', [])
    compliance = data.get('compliance')
    cost = data.get('cost')
    prompt = f"""Generate a professional compliance and cost analysis report for a chemical energy facility:\n\nFACILITY DATA:\n- Compliance Rate: {compliance}%\n- Current Cost: ${cost}M\n- Recent Events: {events}\n\nPlease provide:\n1. Executive Summary\n2. Compliance Analysis (trends, gaps, recommendations)\n3. Cost Analysis (budget vs actual, efficiency metrics)\n4. Risk Assessment\n5. Action Items and Timeline\n6. Regulatory Compliance Status\n\nFormat as a professional report with clear sections and actionable recommendations."""
    result = openrouter_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    assets = data.get('assets', [])
    if not assets:
        return jsonify({'result': 'No assets to analyze. Please check asset data.'})
    prompt = f"""As a fictive maintenance AI specialist, analyze these energy facility assets:\n\nASSETS DATA:\n{assets}\n\nPlease provide:\n1. Asset Health Assessment (for each asset)\n2. Failure Risk Predictions (probability and timeline)\n3. Maintenance Priority Ranking\n4. Recommended Maintenance Schedule\n5. Cost-Benefit Analysis of Preventive vs Reactive Maintenance\n6. Resource Allocation Recommendations\n7. Asset Protection Strategies\n\nInclude specific timelines, risk scores, and cost estimates where possible. Focus on preventing costly failures and optimizing maintenance budgets."""
    result = openrouter_query(prompt)
    return jsonify({'result': result})

@app.route('/api/gemini/photo-analysis', methods=['POST'])
def photo_analysis():
    try:
        data = request.get_json() or {}
        image_data = data.get('image')  # Base64 encoded image
        asset_context = data.get('assets', [])
        if not image_data:
            return jsonify({'error': 'No image data provided'})
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        prompt = f"""Analyze this inspection photo from a chemical energy facility and provide intelligent tagging and analysis.\n\nASSET CONTEXT:\n{asset_context}\n\nPlease provide:\n1. Asset Identification\n2. Visual Inspection Findings\n3. Potential Issues or Concerns\n4. Compliance Implications\n5. Recommended Actions\n6. Risk Assessment\n7. Maintenance Recommendations\n\nBe specific about what you observe and provide actionable insights for facility management.\n\n[NOTE: The image is base64-encoded and not directly viewable by OpenRouter, so answer based on the context provided above.]"""
        result = openrouter_query(prompt)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Photo analysis failed: {str(e)}'})

@app.route('/api/gemini/pdf-content', methods=['POST'])
def pdf_content():
    data = request.get_json() or {}
    events = data.get('events', [])
    compliance = data.get('compliance')
    cost = data.get('cost')
    assets = data.get('assets', [])
    prompt = f"""Generate comprehensive content for a professional compliance report PDF for a chemical energy facility.\n\nFACILITY DATA:\n- Compliance Rate: {compliance}%\n- Current Cost: ${cost}M\n- Recent Events: {events}\n- Assets: {assets}\n\nPlease provide a structured report with the following sections:\n\n1. EXECUTIVE SUMMARY\n   - Key findings and recommendations\n   - Overall facility status\n\n2. COMPLIANCE ANALYSIS\n   - Current compliance status\n   - Regulatory requirements met/missed\n   - Compliance trends and gaps\n   - Risk assessment\n\n3. OPERATIONAL PERFORMANCE\n   - Asset health overview\n   - Event analysis and patterns\n   - Performance metrics\n4. COST ANALYSIS\n   - Budget vs actual spending\n   - Cost efficiency metrics\n   - ROI on maintenance activities\n\n5. RISK ASSESSMENT\n   - Identified risks and severity\n   - Mitigation strategies\n   - Priority actions\n\n6. RECOMMENDATIONS\n   - Immediate actions (next 30s)\n   - Short-term improvements (3-6 months)\n   - Long-term strategic initiatives\n\n7. APPENDICES\n   - Detailed asset status\n   - Event timeline\n   - Compliance checklist\n\nFormat this as a professional report suitable for regulatory submission and executive review."""
    result = openrouter_query(prompt)
    return jsonify({'result': result})

@app.route('/api/proxy', methods=['POST'])
def proxy():
    data = request.json
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not set in environment'}), 500
    try:
        print("Calling OpenRouter API from /api/proxy route...")
        start = time.time()
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            json=data,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            timeout=15
        )
        elapsed = time.time() - start
        print(f"OpenRouter API call (proxy) finished in {elapsed:.2f} seconds with status {response.status_code}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
