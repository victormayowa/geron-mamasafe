# Geron Mamasafe - Setup Guide

This guide will help you set up and run the Geron Mamasafe application.

## Prerequisites

Before you begin, ensure you have:
- Python 3.10 or higher
- PostgreSQL 14+
- Redis (optional, for task queue)
- Twilio Account (for WhatsApp/SMS)
- OpenAI or Anthropic API key (for AI features)

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
cd /home/victormayowa/geron-mamasafe
```

### 2. Create Environment File

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your credentials:
```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/geron_mamasafe

# Twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=+1234567890

# AI (Choose one)
OPENAI_API_KEY=your_openai_api_key
# or
ANTHROPIC_API_KEY=your_anthropic_api_key

# Security
SECRET_KEY=your-super-secret-key-change-this
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis
- Backend API

### 4. Seed the Database

```bash
docker-compose exec backend python scripts/seed_database.py
```

### 5. Access the Application

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Manual Setup (Without Docker)

### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database

```bash
sudo -u postgres psql
CREATE DATABASE geron_mamasafe;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE geron_mamasafe TO postgres;
\q
```

### 3. Install Redis (Optional)

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### 4. Setup Python Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
nano .env
```

### 6. Run Database Migrations

The application creates tables automatically on first run. For production, use Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 7. Seed the Database

```bash
python scripts/seed_database.py
```

### 8. Start the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 9. Test the Application

Open your browser and visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Twilio WhatsApp Setup

### 1. Create Twilio Account

1. Go to https://www.twilio.com
2. Sign up for an account
3. Get your Account SID and Auth Token from the console

### 2. Enable WhatsApp Business API

1. In Twilio Console, navigate to Messaging > Try it Out > Send a WhatsApp message
2. Follow the instructions to get your sandbox code
3. Send `join <your-dandbox-code>` to +14155238886 from your WhatsApp

### 3. Configure Webhooks

In Twilio Console:
1. Go to Messaging > Settings > WhatsApp Sandbox Settings
2. Set "When a message comes in" to: `https://your-domain.com/api/v1/webhooks/whatsapp`
3. Set "Status Callback URL" to: `https://your-domain.com/api/v1/webhooks/status`

### 4. Test WhatsApp Integration

Send a message to the Twilio WhatsApp number. You should receive a response!

## API Usage Examples

### 1. Register a Health Center

```bash
curl -X POST "http://localhost:8000/api/v1/health-centers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Primary Healthcare Center",
    "code": "PHC001",
    "facility_level": "primary",
    "district": "Central",
    "state": "State",
    "phone": "+1234567890"
  }'
```

### 2. Register a Mother

```bash
curl -X POST "http://localhost:8000/api/v1/mothers/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+2348012345678",
    "whatsapp_number": "+2348012345678",
    "first_name": "Jane",
    "last_name": "Doe",
    "age": 28,
    "district": "Central",
    "pregnancy_stage": "second_trimester",
    "health_center_id": 1,
    "consent_given": true
  }'
```

### 3. Submit a Health Query

```bash
curl -X POST "http://localhost:8000/api/v1/consultations/query" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+2348012345678",
    "query": "I have a severe headache and I am seeing spots"
  }'
```

### 4. Get Risk Assessment

```bash
curl "http://localhost:8000/api/v1/mothers/1/risk-assessment"
```

## Testing WhatsApp Messages

### Test with Registered Mother

1. Register a mother with phone number via API
2. Send a WhatsApp message from that number to your Twilio WhatsApp number
3. You should receive an AI-generated response!

### Example Messages to Try

- "What are danger signs in pregnancy?"
- "I have fever and abdominal pain"
- "My baby is not feeding well"
- "When should I go to the hospital?"
- "help"

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U postgres -d geron_mamasafe
```

### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping
# Should return: PONG
```

### Twilio Error

- Verify Account SID and Auth Token are correct
- Check phone number format (include country code)
- Review Twilio logs in the console

### AI Service Error

- Verify API key is correct
- Check API quota/balance
- Review OpenAI/Anthropic dashboard logs

## Production Deployment

### 1. Environment Variables

Set all required environment variables in production:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/geron_mamasafe
SECRET_KEY=<strong-random-key>
TWILIO_ACCOUNT_SID=<production-sid>
TWILIO_AUTH_TOKEN=<production-token>
OPENAI_API_KEY=<production-key>
```

### 2. SSL Certificate

Set up SSL for production:
```bash
# Using Let's Encrypt
sudo apt install certbot
sudo certbot --nginx -d your-domain.com
```

### 3. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Gunicorn for Production

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 5. Monitoring

Set up monitoring:
- Application: Sentry, New Relic
- Database: pg_stat_statements
- Infrastructure: Prometheus + Grafana

## Next Steps

1. **Build Frontend Dashboard** - React-based UI for health providers
2. **Add More Message Templates** - Expand daily health education content
3. **Implement Multi-language Support** - Local languages
4. **Add Immunization Tracker** - Track child vaccinations
5. **Build Analytics Dashboard** - Insights and reporting
6. **Set up Push Notifications** - For critical alerts

## Support

For issues or questions:
- Check the README.md
- Review API docs at /docs
- Check logs: `docker-compose logs -f backend`

---

Happy coding! 💚 Let's improve maternal and child health together!
