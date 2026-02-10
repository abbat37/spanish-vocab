"""
Test OpenAI Connection
Run this after adding your OpenAI API key to .env
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection"""

    # Check if required env vars are set
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OPENAI_API_KEY not set in .env")
        print("   Get your API key from: https://platform.openai.com/api-keys")
        return False

    print(f"✓ API Key: {api_key[:10]}...")
    print(f"✓ Model: {model}")
    print("\nTesting connection...")

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Make a simple test request
        response = client.chat.completions.create(
            model=model,
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": "Translate 'hola' to English and respond with just the word."
                }
            ]
        )

        result = response.choices[0].message.content
        print(f"\n✅ Connection successful!")
        print(f"   Test response: {result}")
        print(f"   Model used: {response.model}")
        print(f"   Tokens used: Input={response.usage.prompt_tokens}, Output={response.usage.completion_tokens}")
        print(f"   Estimated cost: ${(response.usage.prompt_tokens * 0.15 / 1000000 + response.usage.completion_tokens * 0.60 / 1000000):.6f}")

        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False

if __name__ == '__main__':
    success = test_openai_connection()
    exit(0 if success else 1)
