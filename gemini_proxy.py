import streamlit as st
import requests
import os
import base64

# Set your Gemini API key as a Streamlit secret or environment variable
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
GEMINI_VISION_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent'

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

st.title("Chem-E-Care AI Dashboard (Streamlit)")

# --- Event Entry ---
st.header("Unified Entry Points")
events = st.text_area("Enter recent events (one per line):", height=100)
event_list = [e.strip() for e in events.split('\n') if e.strip()]

compliance = st.number_input("Compliance Rate (%)", min_value=0, max_value=100, value=92)
cost = st.number_input("Current Cost (M)", min_value=0.0, value=1.23)

# --- AI Analysis ---
st.header("AI-Powered Analysis")
if st.button("Analyze Recent Events"):
    prompt = f"""As an energy consultant, analyze these recent events from a chemical energy facility dashboard:

EVENTS DATA:
{event_list}

Please provide a comprehensive analysis including:
1. Risk assessment and severity levels
2. Operational trends and patterns
3. Compliance implications
4. Recommended immediate actions
5. Long-term strategic recommendations

Focus on actionable insights that would help facility managers make informed decisions. Be specific about risks, costs, and compliance impacts."""
    st.info("Analyzing with Gemini...")
    result = gemini_query(prompt)
    st.success(result)

if st.button("Generate AI Report"):
    prompt = f"""Generate a professional compliance and cost analysis report for a chemical energy facility:

FACILITY DATA:
- Compliance Rate: {compliance}%
- Current Cost: ${cost}M
- Recent Events: {event_list}

Please provide:
1. Executive Summary
2. Compliance Analysis (trends, gaps, recommendations)
3. Cost Analysis (budget vs actual, efficiency metrics)
4. Risk Assessment
5. Action Items and Timeline
6. Regulatory Compliance Status

Format as a professional report with clear sections and actionable recommendations."""
    st.info("Generating report with Gemini...")
    result = gemini_query(prompt)
    st.success(result)

if st.button("Predict Maintenance Needs"):
    prompt = f"""Fictive maintenance AI specialist, analyze these energy facility assets:

ASSETS DATA:
{event_list}

Please provide:
1. Asset Health Assessment (for each asset)
2. Failure Risk Predictions (probability and timeline)
3. Maintenance Priority Ranking
4. Recommended Maintenance Schedule
5. Cost-Benefit Analysis of Preventive vs Reactive Maintenance
6. Resource Allocation Recommendations
7. Asset Protection Strategies

Include specific timelines, risk scores, and cost estimates where possible. Focus on preventing costly failures and optimizing maintenance budgets."""
    st.info("Predicting with Gemini...")
    result = gemini_query(prompt)
    st.success(result)

# --- Photo Analysis ---
st.header("AI Photo Analysis")
uploaded_file = st.file_uploader("Upload Inspection Photo", type=["jpg", "jpeg", "png"])
if uploaded_file and st.button("Analyze Photo with AI"):
    image_bytes = uploaded_file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = f"""Analyze this inspection photo from a chemical energy facility and provide intelligent tagging and analysis.

Please provide:
1. Asset Identification
2. Visual Inspection Findings
3. Potential Issues or Concerns
4. Compliance Implications
5. Recommended Actions
6. Risk Assessment
7. Maintenance Recommendations

Be specific about what you observe and provide actionable insights for facility management."""
    st.info("Analyzing photo with Gemini Vision...")
    result = gemini_vision_query(prompt, image_b64)
    st.success(result) 
