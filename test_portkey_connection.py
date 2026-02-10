"""
Test Portkey Gateway Connection
Uses Anthropic SDK routed through Portkey enterprise gateway
"""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

def test_portkey_connection():
    """Test Portkey gateway connection with Claude"""

    # Check if required env vars are set
    api_key = os.getenv('PORTKEY_API_KEY')
    base_url = os.getenv('PORTKEY_BASE_URL')
    model = os.getenv('PORTKEY_MODEL', 'claude-3-5-haiku-20241022')

    if not api_key:
        print("❌ PORTKEY_API_KEY not set in .env")
        return False

    if not base_url:
        print("❌ PORTKEY_BASE_URL not set in .env")
        return False

    print(f"✓ API Key: {api_key[:10]}...")
    print(f"✓ Base URL: {base_url}")
    print(f"✓ Model: {model}")
    print("\nTesting connection...")

    try:
        # Initialize Anthropic client with Portkey gateway
        client = Anthropic(
            api_key="dummy",  # Not used, auth via x-portkey-api-key header
            base_url=base_url,
            default_headers={
                "x-portkey-api-key": api_key,
                "x-portkey-provider": "anthropic"
            }
        )

        # Make a simple test request
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": "Translate 'hola' to English and respond with just the word."
                }
            ]
        )

        result = response.content[0].text
        print(f"\n✅ Connection successful!")
        print(f"   Test response: {result}")
        print(f"   Model used: {response.model}")
        print(f"   Tokens used: Input={response.usage.input_tokens}, Output={response.usage.output_tokens}")

        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_portkey_connection()
    exit(0 if success else 1)
