# Geron Mamasafe - FREE AI Setup Guide

## 🎯 QUICK START WITH FREE AI

This system uses **FREE LLM options** to keep costs zero or minimal:

### 🥇 Option 1: Groq (FREE TIER - RECOMMENDED)
**Why Groq?** Fast, free tier includes 14,000 tokens/day (plenty for health queries)

1. **Get FREE API Key:**
   - Go to: https://console.groq.com
   - Sign up (free)
   - Create API key
   - Copy it

2. **Add to .env:**
   ```env
   AI_PROVIDER=groq
   GROQ_API_KEY=your_free_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

3. **That's it!** Start the app and it works immediately.

---

### 🥈 Option 2: Ollama (LOCAL - Completely Free)
**Why Ollama?** Runs on your computer, no internet needed, 100% free forever

1. **Install Ollama:**
   ```bash
   # Linux/Mac
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Or download from: https://ollama.ai
   ```

2. **Download Model:**
   ```bash
   ollama pull llama3.1:8b
   ```

3. **Start Ollama:**
   ```bash
   ollama serve
   ```

4. **Add to .env:**
   ```env
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b
   ```

5. **Start the app** - AI runs locally!

---

### 🥉 Option 3: HuggingFace (FREE TIER)
**Why HuggingFace?** Free tier available, many model options

1. **Get FREE API Key:**
   - Go to: https://huggingface.co
   - Sign up (free)
   - Go to Settings > Access Tokens
   - Create new token

2. **Add to .env:**
   ```env
   AI_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=your_token_here
   HUGGINGFACE_MODEL=microsoft/Phi-3-mini-4k-instruct
   ```

---

### 💰 Option 4: OpenAI (PAID - $5-20/month)
**Why OpenAI?** Most accurate, but costs money

1. **Get API Key:**
   - Go to: https://platform.openai.com
   - Sign up
   - Add credit (minimum $5)
   - Create API key

2. **Add to .env:**
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4
   ```

---

## 📊 Free Tier Comparison

| Provider | Daily Limit | Cost | Speed | Accuracy |
|----------|-------------|------|-------|----------|
| **Groq** | 14,000 tokens | FREE | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ |
| **Ollama** | Unlimited | FREE | ⚡⚡ Medium | ⭐⭐⭐⭐ |
| **HuggingFace** | Rate limited | FREE | ⚡ Medium | ⭐⭐⭐⭐ |
| OpenAI | Pay per use | $5-20/mo | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ |

**RECOMMENDATION:** Start with **Groq** (free, fast, accurate)

---

## 🚀 COMPLETE SETUP (5 MINUTES)

### 1. Get Groq API Key (FREE)
```
1. Visit: https://console.groq.com
2. Click "Sign Up"
3. Verify email
4. Click "API Keys"
5. Create new key
6. Copy it!
```

### 2. Configure Environment
```bash
cd /home/victormayowa/geron-mamasafe
cp backend/.env.example backend/.env
nano backend/.env
```

Edit these lines:
```env
# AI - Just fill Groq key, rest stays default
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here

# Twilio (for WhatsApp/SMS)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+your_number
```

### 3. Start with Docker
```bash
docker-compose up -d
```

### 4. Test AI
```bash
curl -X POST "http://localhost:8000/api/v1/consultations/query" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+2348012345678",
    "query": "I have severe headache and blurred vision"
  }'
```

You should get a response like:
```
🔴 RED - EMERGENCY! GO TO HOSPITAL IMMEDIATELY

⚕️ Severe headache with blurred vision
...
```

---

## 🆘 Troubleshooting

### Groq Error: "Rate limit exceeded"
- You've used your daily free quota
- Wait for reset (midnight UTC) or switch to Ollama

### Ollama Not Responding
- Check if running: `ollama list`
- Restart: `ollama serve`
- Check URL in .env matches Ollama port

### HuggingFace Error: "Rate limit"
- Free tier has request limits
- Wait a few minutes and retry
- Consider upgrading to Pro ($9/mo) or switch to Groq

---

## 💡 Pro Tips

### For Production in Nigeria:
1. **Use Groq** for main AI (free, fast)
2. **Keep Ollama as backup** (if Groq fails)
3. **Monitor usage** in Groq console
4. **Cache common responses** to save tokens

### For Zero Budget:
- Use **Ollama only** (100% free, runs on your server)
- Needs minimum 8GB RAM
- No API keys needed ever!

### For Best Performance:
- Start with **Groq free tier**
- If you exceed limits, switch to **Ollama**
- Only pay for **OpenAI** if needed (>500 queries/day)

---

## 📱 Testing WhatsApp Integration

### Twilio Sandbox (FREE)
1. Go to Twilio Console
2. Navigate to Messaging > Try it Out > Send WhatsApp message
3. Get your sandbox code
4. Send `join your-code` to +14155238886 from your WhatsApp
5. Start messaging!

### Test Messages:
```
"I have fever and abdominal pain"
"My baby is not feeding well"
"What are danger signs in pregnancy?"
"I'm 8 months pregnant and having severe headache"
"My child has fast breathing"
```

You'll get traffic light triage responses:
- 🔴 RED = Go to hospital immediately
- 🟡 YELLOW = Visit health center today
- 🟢 GREEN = Home care is safe

---

## 🎓 Next Steps

1. **Register Health Centers** via API
2. **Register Mothers** with phone numbers
3. **Send daily education messages** (automatic)
4. **Monitor consultations** in database
5. **Track high-risk patients** via alerts

---

**Need Help?**
- API Docs: http://localhost:8000/docs
- Logs: `docker-compose logs -f backend`
- Database: `docker-compose exec postgres psql -U postgres -d geron_mamasafe`

💚 **Free AI running for maternal health!**
