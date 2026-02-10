# LLM Setup Guide for Phase 4

## Quick Comparison

| Option | Cost per 1000 words | Speed | Setup Difficulty | Recommendation |
|--------|-------------------|-------|------------------|----------------|
| **GPT-4o Mini (OpenAI)** | ~$0.05 | ⚡⚡⚡ Fast | ✅ Easy | **Best for learning** |
| GPT-3.5 Turbo | ~$0.10 | ⚡⚡⚡ Fast | ✅ Easy | Good alternative |
| Claude Haiku 3.5 | ~$0.10 | ⚡⚡⚡ Fast | 🔐 Need enterprise access | If you have access |

---

## Recommended: OpenAI Direct (No Portkey)

### Why?
- **Simplest setup** - Just need one API key
- **Cheapest option** - GPT-4o Mini is very affordable
- **Excellent quality** - Perfect for vocabulary tagging
- **Built-in rate limiting** - No need for Portkey
- **Great for learning** - Easy to understand and debug

### Setup Steps:

#### 1. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it (starts with `sk-proj-...`)

#### 2. Add to .env file
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
LLM_PROVIDER=openai
```

#### 3. Test Connection
```bash
python3 scripts/test_openai_connection.py
```

You should see:
```
✅ Connection successful!
   Test response: Hello
   Model used: gpt-4o-mini
   Tokens used: Input=15, Output=1
   Estimated cost: $0.000003
```

#### 4. Verify in App
The app runs on port 8080:
```bash
python3 run.py
# Visit: http://localhost:8080
```

---

## Why Not Portkey?

For this learning project, we're using OpenAI directly because:
- ✅ **Simpler:** One API key, no proxy layer
- ✅ **Cheaper:** No additional costs
- ✅ **Faster:** Direct connection
- ✅ **Easier to debug:** Clearer error messages

Portkey is great for production apps with multiple providers, but adds unnecessary complexity for learning.

---

## Cost Estimates

### For 10,000 vocabulary words processed:

**GPT-4o Mini:**
- Input: ~150,000 tokens @ $0.15/1M = $0.02
- Output: ~300,000 tokens @ $0.60/1M = $0.18
- **Total: ~$0.20**

**GPT-3.5 Turbo:**
- Input: ~150,000 tokens @ $0.50/1M = $0.08
- Output: ~300,000 tokens @ $1.50/1M = $0.45
- **Total: ~$0.53**

**Claude Haiku 3.5:**
- Input: ~150,000 tokens @ $0.80/1M = $0.12
- Output: ~300,000 tokens @ $4.00/1M = $1.20
- **Total: ~$1.32**

---

## Rate Limiting Strategy

### OpenAI's Built-in Limits (Free tier):
- **3 requests per minute** (low tier)
- **200 requests per minute** (after you add $5+ credit)

### Our App-Level Protection:
```python
@limiter.limit("10 per minute")  # Per user
def process_words():
    ...
```

This prevents:
- Users from spamming the endpoint
- Accidental high bills
- Hitting API rate limits

---

## Next Steps

1. ✅ Get OpenAI API key from https://platform.openai.com/api-keys
2. ✅ Add to `.env` file: `OPENAI_API_KEY=sk-proj-...`
3. ✅ Test: `python3 scripts/test_openai_connection.py`
4. ✅ Run app: `python3 run.py` (localhost:8080)
5. ✅ Start implementing Phase 4!

---

## Need Help?

If you see errors:
- **401 Unauthorized:** Check your API key is correct
- **429 Rate Limit:** Wait a minute or add credits to your OpenAI account
- **Connection Error:** Check your internet connection

Good luck! 🚀
