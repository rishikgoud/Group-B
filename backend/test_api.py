#!/usr/bin/env python3
"""
Simple test to check Gemini API key and available models
"""

import os
import google.generativeai as genai

def test_api_key():
    """Test Gemini API key validity"""

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

        # Test basic connectivity
        print("\n🔌 Testing API connectivity...")

        # Try to list models
        print("📋 Listing available models...")
        models = genai.list_models()

        print("\n✅ Available models:")
        for model in models:
            print(f"  - {model.name}")
            print(f"    Description: {model.description}")
            print(f"    Supported methods: {[m.name for m in model.supported_generation_methods]}")
            print()

        # Test the basic gemini-pro model
        print("🧪 Testing gemini-pro model...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            print("  ✅ gemini-pro model created successfully")

            # Test a simple generation
            response = model.generate_content("Hello, test message")
            print("  ✅ Test generation successful")
            print(f"  📝 Response: {response.text[:100]}...")

        except Exception as e:
            print(f"  ❌ gemini-pro test failed: {e}")

    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        print("\nPossible issues:")
        print("1. API key is invalid or expired")
        print("2. API key doesn't have Gemini API access")
        print("3. Network connectivity issues")
        print("4. API key format is incorrect")
        print("\nPlease check:")
        print("- Your API key starts with 'AIza' (Google API keys)")
        print("- You have enabled the Gemini API in Google AI Studio")
        print("- Your API key has the necessary permissions")

if __name__ == "__main__":
    test_api_key()
