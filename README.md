# Geron Mamasafe - Maternal, Neonatal, and Child Health AI Assistant

A comprehensive AI-powered health education and monitoring system connected via WhatsApp and SMS for maternal, neonatal, and child healthcare.

## 🌟 Overview

Geron Mamasafe is designed to reduce maternal and child mortality by providing:
- **24/7 AI Health Assistant** accessible via WhatsApp/SMS
- **Daily Health Education** messages tailored to pregnancy stage and child's age
- **Danger Signs Detection** with immediate guidance on when and where to seek care
- **Risk Stratification** for early identification of high-risk pregnancies and children
- **Healthcare Facility Referral** guidance (Primary → Secondary → Tertiary)

## 🎯 Key Features

### For Mothers
- ✅ **AI Consultation** - Ask health questions anytime via WhatsApp/SMS
- ✅ **Daily Health Education** - Personalized messages based on pregnancy stage
- ✅ **Danger Signs Alert** - Learn warning signs and when to seek care
- ✅ **Risk Assessment** - Automatic risk stratification
- ✅ **Facility Guidance** - Know which level of care to visit

### For Health Providers
- ✅ **Mother & Child Registration** - Simple phone-based registration
- ✅ **Risk Dashboard** - Identify high-risk patients
- ✅ **Consultation History** - View all AI interactions
- ✅ **Alert System** - Get notified of critical cases

### Coverage Areas
- 🤰 **Maternal Health** - All pregnancy stages (first, second, third trimester, postpartum, labor)
- 👶 **Neonatal Health** - Newborn care (0-28 days)
- 👧 **Child Health** - Children under 5 years (infants, toddlers, preschool)

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python FastAPI (async)
- **Database**: PostgreSQL (async)
- **Messaging**: Twilio (WhatsApp Business API + SMS)
- **AI Engine**: OpenAI GPT-4 / Anthropic Claude (configurable)
- **Task Scheduling**: APScheduler + Celery
- **Authentication**: JWT tokens

### Project Structure

```
geron-mamasafe/
├── backend/
│   ├── app/
│   │   ├── api/              # REST API endpoints
│   │   │   ├── mothers.py
│   │   │   ├── children.py
│   │   │   ├── consultations.py
│   │   │   ├── webhooks.py    # WhatsApp/SMS webhooks
│   │   │   ├── health_centers.py
│   │   │   └── providers.py
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── scheduler.py
│   │   ├── models/           # Database models
│   │   │   └── models.py
│   │   ├── schemas/          # Pydantic schemas
│   │   │   └── schemas.py
│   │   ├── services/         # Business logic
│   │   │   ├── ai_consultation.py
│   │   │   ├── twilio_service.py
│   │   │   ├── message_scheduler.py
│   │   │   ├── risk_stratification.py
│   │   │   └── danger_signs_db.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/                 # React dashboard (to be built)
├── docs/                     # Documentation
└── scripts/                  # Deployment scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis (for task queue)
- Twilio Account (WhatsApp Business API)
- OpenAI or Anthropic API key

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Set up database**
```bash
# Create PostgreSQL database
createdb geron_mamasafe

# Run migrations (or let app create tables on first run)
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access API documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📱 WhatsApp/SMS Integration

### Twilio Setup

1. **Create Twilio Account**
   - Sign up at https://www.twilio.com
   - Get WhatsApp Business API access

2. **Configure Twilio Credentials**
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886  # Twilio sandbox
   TWILIO_PHONE_NUMBER=+1234567890  # Your SMS number
   ```

3. **Set Webhook URL**
   - WhatsApp: `https://your-domain.com/api/v1/webhooks/whatsapp`
   - SMS: `https://your-domain.com/api/v1/webhooks/sms`

### Testing with Sandbox

Twilio provides a WhatsApp sandbox for testing:
1. Send `join <your-sandbox-code>` to +14155238886
2. You'll receive a confirmation message
3. Start sending health queries!

## 🤖 AI Configuration

### OpenAI (GPT-4)
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4
```

### Anthropic (Claude)
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key
```

## 📊 Database Models

### Core Entities
- **HealthCenter** - Healthcare facilities (primary, secondary, tertiary)
- **Mother** - Registered mothers/patients
- **Child** - Children under 5
- **HealthProvider** - Healthcare staff
- **Message** - All sent/received messages
- **Consultation** - AI conversation history
- **Alert** - Critical notifications
- **DangerSign** - Knowledge base of danger signs
- **DailyMessageTemplate** - Educational message templates

## 🎓 Danger Signs Knowledge Base

The system includes comprehensive danger signs for:

### Maternal (by pregnancy stage)
- First Trimester: Bleeding, severe pain, hyperemesis, fever
- Second Trimester: Bleeding, headaches, swelling, decreased movement
- Third Trimester: Preeclampsia, HELLP syndrome, preterm labor
- Labor: Prolonged labor, cord prolapse, meconium
- Postpartum: Hemorrhage, infection, postpartum depression

### Neonatal (0-28 days)
- Feeding difficulties, convulsions, fast breathing
- Fever, hypothermia, jaundice, cord infection

### Child (Under 5)
- Unable to drink, convulsions, pneumonia signs
- Severe malnutrition, lethargy, severe paleness

Each danger sign includes:
- Severity level (LOW, MEDIUM, HIGH, CRITICAL)
- Recommended facility level (Primary, Secondary, Tertiary)
- Urgency (immediate, same_day, within_24h, monitor)
- Home care instructions

## 🔐 Security

- JWT authentication for health providers
- Phone number verification for mothers
- Encrypted password storage (bcrypt)
- CORS configuration for frontend
- API rate limiting (configure as needed)

## 📈 Scalability

The system is designed for state-wide deployment:
- Async database operations for high concurrency
- Message queue for background tasks
- Horizontal scaling support
- Multi-tenant architecture (multiple health centers)

## 🧪 Testing

```bash
cd backend
pytest tests/ -v --cov=app
```

## 📝 API Endpoints

### Mothers
- `POST /api/v1/mothers/` - Register mother
- `GET /api/v1/mothers/` - List mothers (with filters)
- `GET /api/v1/mothers/{id}` - Get mother details
- `PUT /api/v1/mothers/{id}` - Update mother
- `GET /api/v1/mothers/{id}/risk-assessment` - Get risk assessment

### Children
- `POST /api/v1/children/` - Register child
- `GET /api/v1/children/{id}` - Get child details
- `GET /api/v1/children/mother/{mother_id}` - Get mother's children
- `GET /api/v1/children/{id}/risk-assessment` - Get child risk assessment

### Consultations
- `POST /api/v1/consultations/query` - Submit health question
- `GET /api/v1/consultations/history/{mother_id}` - Get consultation history

### Webhooks
- `POST /api/v1/webhooks/whatsapp` - WhatsApp incoming messages
- `POST /api/v1/webhooks/sms` - SMS incoming messages

### Health Centers
- `POST /api/v1/health-centers/` - Register health center
- `GET /api/v1/health-centers/` - List health centers

### Providers
- `POST /api/v1/providers/register` - Register health provider
- `POST /api/v1/providers/login` - Login provider

## 🎯 Use Cases

### Case 1: Mother Experiences Danger Sign
1. Mother sends WhatsApp message: "I have severe headache and seeing spots"
2. AI detects possible preeclampsia (CRITICAL)
3. Response: "🚨 URGENT - Go to tertiary facility immediately..."
4. Alert sent to health provider
5. Follow-up message scheduled

### Case 2: Daily Health Education
1. Scheduler runs at 8 AM daily
2. For each mother, gets stage-appropriate message
3. Sends via WhatsApp/SMS
4. Logs message in database

### Case 3: Child Health Query
1. Mother asks: "My baby is breathing fast"
2. AI checks neonatal/child danger signs
3. Provides guidance based on child's age
4. Recommends facility level based on severity

## 🌐 Deployment

### Docker (Coming Soon)
```bash
docker-compose up -d
```

### Production Checklist
- [ ] Set up PostgreSQL production database
- [ ] Configure Redis for task queue
- [ ] Set up Twilio production WhatsApp Business API
- [ ] Configure OpenAI/Anthropic API keys
- [ ] Set up SSL certificates
- [ ] Configure production environment variables
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

## 📞 Support

For questions or issues:
- Email: support@geronmamasafe.org
- Documentation: /docs
- API Reference: /docs (Swagger UI)

## 📄 License

This project is designed to improve maternal and child health outcomes.

## 🙏 Acknowledgments

Built to support mothers and reduce maternal/child mortality through:
- Health education
- Early danger sign detection
- Timely healthcare facility referral
- AI-powered 24/7 support

---

**Geron Mamasafe** - Empowering mothers with AI-driven health education and support 💚
