#!/usr/bin/env python3
"""
Test script to list available Gemini models
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_models():
    """Test available Gemini models"""

    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please check your .env file")
        return

    print(f"🔑 API Key found: {api_key[:10]}...")
    print(f"📚 Google Generative AI version: {genai.__version__}")

    try:
        # Configure the API
        genai.configure(api_key=api_key)

        # List available models
        print("\n📋 Listing available models...")
        models = genai.list_models()

        print("\n✅ Available models:")
        for model in models:
            print(f"  - {model.name}")
            print(f"    Description: {model.description}")
            print(f"    Supported methods: {[m.name for m in model.supported_generation_methods]}")
            print()

        # Test common model names
        test_models = [
            'gemini-pro',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-pro-vision',
            'gemini-1.5-pro-vision'
        ]

        print("🧪 Testing model availability:")
        for model_name in test_models:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"  ✅ {model_name} - Available")
            except Exception as e:
                print(f"  ❌ {model_name} - {str(e)}")

    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    test_gemini_models()
