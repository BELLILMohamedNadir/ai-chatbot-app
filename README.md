🤖 AI Chatbot Platform
A modern, real-time chat application powered by AI with multi-room support and WebSocket communication.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo(https://fastapi.tiangolohttps://img.shields.io/badge/Next.js-14+-black?logo=next[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue?logo=(https://www.typescriptlanghttps://img.shields.io/badge

📖 Overview
AI Chatbot Platform is a full-stack application enabling real-time communication with AI assistants. It provides secure authentication, multiple chat rooms, AI-powered responses, and persistent message history.

🎯 Key Features
🔐 Secure authentication (JWT)

💬 Real-time chat via WebSocket

🏠 Multi-room support

🤖 Mistral AI integration

👥 Online user presence

📱 Responsive UI

🔄 Auto-reconnection

🏗️ Architecture
text
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Next.js    │ ◄────► │   FastAPI    │ ◄────► │  PostgreSQL  │
│   Frontend   │  HTTP   │   Backend    │         │   Database   │
│  Port: 3000  │   WS    │  Port: 8001  │         │   Port: 5432 │
└──────────────┘         └──────────────┘         └──────────────┘
                                 │
                         ┌───────┴────────┐
                         │   Mistral AI   │
                         │      API       │
                         └────────────────┘
🚀 Quick Start
Prerequisites
Python 3.11+

Node.js 18+

PostgreSQL 15+

Mistral AI API Key (get one at https://console.mistral.ai/)

1) Clone repository
bash
git clone https://github.com/yourusername/ai-chatbot-app.git
cd ai-chatbot-app
2) Backend setup
bash
cd apps/backend

# Create virtual environment
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set MISTRAL_API_KEY, DATABASE_URL, SECRET_KEY, etc.

# Initialize database
python -c "from app.db.database import init_db; init_db()"

# Start server
uvicorn app.main:app --reload --port 8001
3) Frontend setup
bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
# NEXT_PUBLIC_WS_URL=ws://localhost:8001/api/v1

# Start dev server
npm run dev
4) Access
Frontend: http://localhost:3000

Backend API: http://localhost:8001

API Docs (Swagger): http://localhost:8001/docs

⚙️ Configuration
Backend (.env)
text
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db

# Security
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI
MISTRAL_API_KEY=your-mistral-api-key

# CORS
ALLOWED_ORIGINS=http://localhost:3000
Frontend (.env.local)
text
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8001/api/v1
📚 API Examples
Auth: Register
bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
Auth: Login
bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
Response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
WebSocket: Connect (JS)
js
const ws = new WebSocket(
  'ws://localhost:8001/api/v1/ws/chat?token=YOUR_JWT_TOKEN&room_id=1'
);

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'chat',
    message: 'Hello AI!',
    model: 'mistral-small-latest'
  }));
};

ws.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data));
};
📁 Project Structure
text
ai-chatbot-app/
├── apps/
│   └── backend/
│       ├── app/
│       │   ├── api/v1/endpoints/   # API Routes
│       │   ├── core/               # Config & Security
│       │   ├── crud/               # DB Operations
│       │   ├── models/             # SQLAlchemy Models
│       │   ├── schemas/            # Pydantic Schemas
│       │   ├── services/           # Business Logic
│       │   └── main.py             # App Entry Point
│       └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js Pages
│   │   ├── components/             # React Components
│   │   ├── hooks/                  # Custom Hooks
│   │   ├── lib/                    # Utilities
│   │   └── types/                  # TS Types
│   └── package.json
│
├── docker-compose.yml
└── README.md
🧪 Testing
bash
# Backend
cd apps/backend
pytest tests/ -v --cov

# Frontend
cd frontend
npm test
npm run test:e2e
🐳 Docker
bash
docker-compose up -d       # Build & start
docker-compose logs -f     # Logs
docker-compose down        # Stop
Services:

FastAPI backend

Next.js frontend

PostgreSQL database

Redis (optional)

🔒 Security
JWT auth, bcrypt password hashing

CORS protection

Pydantic validation

SQLAlchemy ORM

Env-based config

Rate limiting (planned)

🤝 Contributing
Fork the repo

Create a branch (git checkout -b feature/amazing-feature)

Commit (git commit -m 'Add amazing feature')

Push (git push origin feature/amazing-feature)

Open a PR

📝 License
MIT – see LICENSE

👨‍💻 Author
Mohamed Nadir BELLIL
Master 2 Software Engineering, University of Montpellier
GitHub: https://github.com/BELLILMohamedNadir