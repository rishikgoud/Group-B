#!/usr/bin/env python3
"""
Comprehensive Gemini API validation and testing
"""

import os
import sys
import json
import google.generativeai as genai
from google.api_core import exceptions

def validate_api_key():
    """Comprehensive API key validation"""

    print("🔍 GEMINI API VALIDATION TEST")
    print("=" * 50)

    # Check 1: Environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("   Please check your .env file")
        return False

    print(f"✅ API Key found in environment: {api_key[:15]}...")

    # Check 2: API key format
    if not api_key.startswith('AIza'):
        print(f"❌ API Key format invalid: {api_key[:20]}...")
        print("   Google API keys should start with 'AIza'")
        return False

    if len(api_key) < 30:
        print(f"❌ API Key too short: {len(api_key)} characters")
        print("   API keys are typically 39 characters long")
        return False

    print(f"✅ API Key format valid: {len(api_key)} characters")

    # Check 3: Library version
    print(f"✅ Google Generative AI version: {genai.__version__}")

    # Check 4: API Connection
    try:
        print("\n🌐 Testing API connection...")
        genai.configure(api_key=api_key)

        # Test model listing
        print("📋 Fetching available models...")
        models = genai.list_models()

        if not models:
            print("❌ No models returned from API")
            return False

        print(f"✅ Found {len(models)} available models:")

        gemini_models = []
        for model in models:
            if 'gemini' in model.name.lower():
                gemini_models.append(model)
                print(f"   - {model.name}")
                if hasattr(model, 'supported_generation_methods'):
                    methods = [m.name for m in model.supported_generation_methods]
                    print(f"     Methods: {methods}")

        if not gemini_models:
            print("❌ No Gemini models found!")
            return False

        # Check 5: Test gemini-pro specifically
        print(f"\n🧪 Testing gemini-pro model...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            print("   ✅ gemini-pro model created successfully")

            # Test generation
            test_response = model.generate_content("Say 'Hello API test successful' in JSON format")
            print("   ✅ Test generation successful")
            print(f"   📝 Response: {test_response.text.strip()}")

            return True

        except exceptions.NotFound as e:
            print(f"   ❌ gemini-pro model not found: {e}")
            print("   This suggests your API key doesn't have access to Gemini models")
            return False
        except exceptions.PermissionDenied as e:
            print(f"   ❌ Permission denied: {e}")
            print("   Your API key doesn't have permission to use Gemini API")
            return False
        except exceptions.InvalidArgument as e:
            print(f"   ❌ Invalid request: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            return False

    except exceptions.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Your API key is invalid or expired")
        return False
    except exceptions.GoogleAPIError as e:
        print(f"❌ Google API error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main validation function"""
    print("Starting comprehensive Gemini API validation...\n")

    success = validate_api_key()

    print("\n" + "=" * 50)
    if success:
        print("🎉 VALIDATION SUCCESSFUL!")
        print("Your Gemini API setup is working correctly.")
        print("The contract analysis should work now.")
    else:
        print("❌ VALIDATION FAILED!")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Get a new API key from https://makersuite.google.com/app/apikey")
        print("2. Make sure it starts with 'AIza'")
        print("3. Enable Gemini API in Google AI Studio")
        print("4. Copy the full key (39 characters) to your .env file")
        print("5. Restart the backend server")
        print("\n📝 Your .env file should look like:")
        print("GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxx")

    return success

if __name__ == "__main__":
    main()
