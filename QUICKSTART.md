# 🚀 Geron Mamasafe - 5-Minute Quick Start

## Prerequisites
- Docker & Docker Compose installed
- FREE Groq API key (get at https://console.groq.com)

---

## STEP 1: Get FREE Groq API Key (2 minutes)

1. Visit: **https://console.groq.com**
2. Click **"Sign Up"**
3. Verify your email
4. Click **"API Keys"** in dashboard
5. Click **"Create API Key"**
6. **Copy the key** (starts with `gsk_`)

---

## STEP 2: Configure Environment (1 minute)

```bash
# Navigate to project
cd /home/victormayowa/geron-mamasafe

# Copy env template
cp backend/.env.example backend/.env

# Edit the file
nano backend/.env
```

**Change these lines:**
```env
# AI Configuration
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here

# Twilio (use sandbox for testing)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+14155238886
```

Save and exit (`Ctrl+X`, then `Y`, then `Enter`)

---

## STEP 3: Start Application (1 minute)

```bash
# Start all services
docker-compose up -d

# Wait 30 seconds for database to initialize

# Check if running
docker-compose ps
```

You should see:
```
✅ geron_mamasafe_backend
✅ geron_mamasafe_db
✅ geron_mamasafe_redis
```

---

## STEP 4: Seed Database (30 seconds)

```bash
# Populate with danger signs and templates
docker-compose exec backend python scripts/seed_database.py
```

You should see:
```
🌱 Seeding database...
📋 Adding danger signs...
✅ Added 66 danger signs
📝 Adding daily message templates...
✅ Added 17 message templates
🏥 Adding sample health centers...
✅ Added 2 health centers

✅ Database seeding completed successfully!
```

---

## STEP 5: Test AI (30 seconds)

### Option A: Via API (Browser)

Open: **http://localhost:8000/docs**

Click on `POST /api/v1/consultations/query` → "Try it out" → Execute

### Option B: Via Terminal

```bash
curl -X POST "http://localhost:8000/api/v1/consultations/query" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+2348012345678",
    "query": "I have severe headache and blurred vision"
  }'
```

### Expected Response:

```json
{
  "success": true,
  "response": "🔴 RED - EMERGENCY! GO TO HOSPITAL IMMEDIATELY\n\n⚕️ Severe headache with blurred vision\n\n📋 What to look for:\nSevere headache accompanied by vision problems...\n\n✅ What You Should Do:\n🔴 EMERGENCY! Go to tertiary facility IMMEDIATELY...",
  "triage_severity": "red",
  "category": "danger_signs",
  "requires_follow_up": true
}
```

---

## 🎉 YOU'RE LIVE!

### What Works Now:

✅ **AI Consultation** - Ask health questions via API
✅ **Danger Signs Detection** - 66 signs with triage
✅ **Traffic Light System** - 🔴🟡🟢 responses
✅ **Risk Stratification** - Automatic assessment
✅ **Daily Message Scheduler** - Runs at 8 AM

---

## 📱 Test WhatsApp Integration

### Setup Twilio Sandbox (FREE):

1. Go to: **https://www.twilio.com**
2. Sign up (free)
3. Navigate to: **Messaging > Try it Out > Send a WhatsApp message**
4. Get your sandbox code (e.g., `join adult-name`)
5. Send that message to **+14155238886** from your WhatsApp
6. Start chatting!

### Configure Webhook:

In Twilio Console > WhatsApp Sandbox Settings:
- **When a message comes in**: `https://your-domain.com/api/v1/webhooks/whatsapp`
- **Status Callback**: `https://your-domain.com/api/v1/webhooks/status`

*(For local testing, use ngrok: `ngrok http 8000`)*

---

## 🔧 Common Commands

### View Logs:
```bash
docker-compose logs -f backend
```

### Restart:
```bash
docker-compose restart backend
```

### Stop:
```bash
docker-compose down
```

### Database Access:
```bash
docker-compose exec postgres psql -U postgres -d geron_mamasafe
```

### Test Danger Signs:
```bash
docker-compose exec backend python scripts/test_danger_signs.py
```

---

## 📊 Quick API Tests

### 1. Register Health Center
```bash
curl -X POST "http://localhost:8000/api/v1/health-centers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Primary Health Center Test",
    "code": "PHC_TEST_001",
    "facility_level": "primary",
    "district": "Test District",
    "state": "Test State"
  }'
```

### 2. Register Mother
```bash
curl -X POST "http://localhost:8000/api/v1/mothers/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+2348012345678",
    "whatsapp_number": "+2348012345678",
    "first_name": "Test",
    "last_name": "Mother",
    "age": 28,
    "district": "Test District",
    "pregnancy_stage": "second_trimester",
    "health_center_id": 1,
    "consent_given": true
  }'
```

### 3. Get Risk Assessment
```bash
curl "http://localhost:8000/api/v1/mothers/1/risk-assessment"
```

### 4. Health Check
```bash
curl "http://localhost:8000/health"
```

---

## 🆘 Troubleshooting

### Backend won't start:
```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose build backend
docker-compose up -d backend
```

### Database connection error:
```bash
# Wait 30 seconds (PostgreSQL needs time to initialize)
docker-compose logs -f postgres
```

### Groq API error:
```bash
# Verify your key in .env
cat backend/.env | grep GROQ

# Test key at: https://console.groq.com
```

### Port already in use:
```bash
# Change port in docker-compose.yml
# From: "8000:8000"
# To:   "8001:8000"
```

---

## 📚 Next Steps

1. ✅ **Read**: [FREE_AI_SETUP.md](FREE_AI_SETUP.md) - More AI options
2. ✅ **Read**: [DANGER_SIGNS_QUICK_REFERENCE.md](DANGER_SIGNS_QUICK_REFERENCE.md) - Triage guide
3. ✅ **Read**: [COMPLETE_SYSTEM_OVERVIEW.md](COMPLETE_SYSTEM_OVERVIEW.md) - Full system
4. ✅ **Test**: Register mothers and send WhatsApp messages
5. ✅ **Deploy**: To production server

---

## 💡 Pro Tips

### For Development:
```bash
# Watch logs in real-time
docker-compose logs -f

# Access backend shell
docker-compose exec backend bash

# Run Python shell
docker-compose exec backend python
```

### For Production:
- Change `SECRET_KEY` in `.env`
- Use production Twilio number (not sandbox)
- Set up SSL certificate
- Use proper PostgreSQL password
- Monitor Groq API usage

---

**🎉 You're all set! Your FREE AI health assistant is running!**

**Need help?** Check the documentation in `/docs` folder.

**Want to contribute?** See [ENHANCEMENTS.md](ENHANCEMENTS.md) for what was built.

💚 **Geron Mamasafe** - Saving lives through AI-powered health education!
