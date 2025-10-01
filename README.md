# 🤖 AI Chatbot Platform

A modern, real-time chat application powered by AI with multi-room support and WebSocket communication.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

---

## 📖 Overview

AI Chatbot Platform is a full-stack application enabling real-time communication with AI assistants. It provides secure authentication, multiple chat rooms, AI-powered responses, and persistent message history.

## 🎯 Key Features

- 🔐 **Secure Authentication** - JWT-based authentication
- 💬 **Real-time Chat** - WebSocket communication
- 🏠 **Multi-room Support** - Organize conversations
- 🤖 **Mistral AI Integration** - Powered by advanced AI
- 👥 **Online User Presence** - See who's online
- 📱 **Responsive UI** - Works on all devices
- 🔄 **Auto-reconnection** - Seamless connection recovery

## 🏗️ Architecture

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Next.js    │ ◄─────► │   FastAPI    │ ◄─────► │  PostgreSQL  │
│   Frontend   │  HTTP   │   Backend    │         │   Database   │
│  Port: 3000  │   WS    │  Port: 8001  │         │  Port: 5432  │
└──────────────┘         └──────────────┘         └──────────────┘
                                │
                         ┌──────┴───────┐
                         │  Mistral AI  │
                         │     API      │
                         └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Mistral AI API Key ([Get one here](https://console.mistral.ai/))

### 1. Clone Repository

```bash
git clone https://github.com/BELLILMohamedNadir/ai-chatbot-app.git
cd ai-chatbot-app
```

### 2. Backend Setup

```bash
cd apps/backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Mac/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set MISTRAL_API_KEY, DATABASE_URL, SECRET_KEY, etc.

# Initialize database
python -c "from app.db.database import init_db; init_db()"

# Start server
uvicorn app.main:app --reload --port 8001
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your API URLs

# Start dev server
npm run dev
```

### 4. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **API Docs (Swagger):** http://localhost:8001/docs

## ⚙️ Configuration

### Backend (.env)

```env
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
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8001/api/v1
```

## 📚 API Examples

### Auth: Register

```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
```

### Auth: Login

```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### WebSocket: Connect

```javascript
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
```

## 📁 Project Structure

```
ai-chatbot-app/
├── apps/
│   └── backend/
│       ├── app/
│       │   ├── api/v1/endpoints/    # API Routes
│       │   ├── core/                # Config & Security
│       │   ├── crud/                # DB Operations
│       │   ├── models/              # SQLAlchemy Models
│       │   ├── schemas/             # Pydantic Schemas
│       │   ├── services/            # Business Logic
│       │   └── main.py              # App Entry Point
│       └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js Pages
│   │   ├── components/              # React Components
│   │   ├── hooks/                   # Custom Hooks
│   │   ├── lib/                     # Utilities
│   │   └── types/                   # TS Types
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

## 🧪 Testing

```bash
# Backend
cd apps/backend
source .venv/bin/activate
pytest tests/ -v --cov

# Frontend
cd frontend
npm test
npm run test:e2e
```

## 🐳 Docker

```bash
docker-compose up -d    # Build & start
docker-compose logs -f  # View logs
docker-compose down     # Stop services
```

**Included Services:**
- FastAPI backend
- Next.js frontend
- PostgreSQL database

## 🔒 Security

- JWT authentication with bcrypt password hashing
- CORS protection
- Pydantic validation
- SQLAlchemy ORM with parameterized queries
- Environment-based configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 Author

**Mohamed Nadir BELLIL**  
Master 2 Software Engineering, University of Montpellier  
GitHub: [@BELLILMohamedNadir](https://github.com/BELLILMohamedNadir)

---

<p align="center">Made by Mohamed Nadir BELLIL</p>
