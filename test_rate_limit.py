"""
Quick script to test rate limiting on the API
Run this to verify rate limits are working
"""
import requests
import time

# Change this to your URL
BASE_URL = "http://localhost:5000"  # Local testing
# BASE_URL = "https://spanish-vocab.onrender.com"  # Production testing

def test_rate_limit():
    """Send 15 requests to trigger rate limit (limit is 10/minute)"""
    print("Testing rate limit (10 requests per minute)...\n")

    for i in range(1, 16):
        response = requests.post(
            f"{BASE_URL}/api/mark-learned",
            json={"word_id": 1, "learned": True},
            headers={"Content-Type": "application/json"}
        )

        status = response.status_code
        emoji = "✅" if status == 200 or status == 404 else "❌"

        print(f"Request {i:2d}: {emoji} Status {status}")

        if status == 429:
            print(f"  → Rate limited! Response: {response.text[:100]}")
        elif status == 404:
            print(f"  → Expected (word not practiced yet)")

        time.sleep(0.5)  # Small delay between requests

    print("\n✅ Test complete!")
    print("If you see 429 status codes above, rate limiting is working!")

if __name__ == "__main__":
    test_rate_limit()
