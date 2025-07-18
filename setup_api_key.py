#!/usr/bin/env python3
"""
Helper script to set up the OpenRouter API key
"""

import os
from pathlib import Path

def setup_api_key():
    print("=== Chem-E-Care API Key Setup ===")
    print()
    
    # Check if .env file exists
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENROUTER_API_KEY' in content:
                print("✅ API key is already configured")
                return
    else:
        print("📝 Creating .env file...")
    
    print()
    print("To get real AI responses, you need an OpenRouter API key:")
    print("1. Go to https://openrouter.ai/")
    print("2. Sign up and get your API key")
    print("3. Enter it below:")
    print()
    
    api_key = input("Enter your OpenRouter API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Write to .env file
        with open(env_file, 'w') as f:
            f.write(f"OPENROUTER_API_KEY={api_key}\n")
        print("✅ API key saved to .env file")
        print("🎉 You can now run 'python app.py' to get real AI responses!")
    else:
        print("⏭️  Skipping API key setup")
        print("💡 You can still run the app, but AI features will show mock responses")
        print("💡 To add the API key later, run this script again or edit the .env file")

if __name__ == "__main__":
    setup_api_key() 