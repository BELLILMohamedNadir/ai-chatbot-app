#!/bin/bash

echo "👤 Setting up Demo Account for Enterprise AI Chatbot..."

# Generate password hash using Python
DEMO_HASH=$(python3 -c "
import bcrypt
password = 'demo123'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(hashed.decode('utf-8'))
")

echo "🔐 Generated password hash for demo123"

# Insert demo user with proper hash
docker exec ai-chatbot-app_postgres_1 psql -U postgres -d chatbot_db -c "
INSERT INTO users (email, username, full_name, hashed_password, is_active, created_at) 
VALUES (
    'demo@example.com',
    'demo_user',
    'Demo User',
    '$DEMO_HASH',
    true,
    NOW()
) ON CONFLICT (email) DO UPDATE SET
    username = EXCLUDED.username,
    full_name = EXCLUDED.full_name,
    hashed_password = EXCLUDED.hashed_password,
    updated_at = NOW();

-- Verify demo user
SELECT id, email, username, full_name, is_active, created_at FROM users WHERE email = 'demo@example.com';
"

echo "✅ Demo account created successfully!"
echo ""
echo "📋 Demo Account Credentials:"
echo "   📧 Email: demo@example.com"
echo "   🔐 Password: demo123"
echo "   👤 Username: demo_user"
echo ""
echo "🧪 Test login:"
echo "curl -X POST http://localhost:8000/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"demo@example.com\",\"password\":\"demo123\"}'"

echo ""
echo "🌐 Frontend can now display:"
echo "   'Try Demo Account: demo@example.com / demo123'"
