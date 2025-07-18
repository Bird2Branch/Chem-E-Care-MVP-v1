# Chem-E-Care

A unified chemical energy facility management system with AI-powered insights.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables (optional):**
   For real AI responses, you can set up your OpenRouter API key:
   
   **Option A: Use the setup script (recommended):**
   ```bash
   python setup_api_key.py
   ```
   
   **Option B: Create .env file manually:**
   Create a `.env` file in the root directory with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```
   
   **Note:** The app will work without an API key, but AI features will show mock responses.

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and go to `http://localhost:5000`

## Features

- **Unified Dashboard**: All-in-one view of facility operations
- **AI Analysis**: DeepSeek AI-powered insights and predictions
- **Event Management**: Track and orchestrate facility events
- **Alert System**: Real-time alerts with automated responses
- **Compliance Tracking**: Monitor regulatory compliance
- **Asset Management**: Track equipment health and maintenance

## Deployment

This unified Flask app can be deployed to:
- **Render** (recommended)
- **Railway**
- **Heroku**
- **PythonAnywhere**

The app serves both the frontend HTML pages and handles API requests in a single deployment.
