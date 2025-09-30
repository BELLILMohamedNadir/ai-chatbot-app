#!/bin/bash

echo "🗄️ Setting up Enterprise Database Schema..."

# Add all missing columns
echo "📝 Adding missing columns..."
docker exec ai-chatbot-app_postgres_1 psql -U postgres -d chatbot_db -c "
-- Add missing columns
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS room_id INTEGER DEFAULT 1;
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS message_type VARCHAR(50);
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS model_name VARCHAR(100);

-- Make constraints optional for modern WebSocket chat
ALTER TABLE chat_messages ALTER COLUMN session_id DROP NOT NULL;
ALTER TABLE chat_messages ALTER COLUMN sender DROP NOT NULL;
ALTER TABLE chat_messages ALTER COLUMN sender SET DEFAULT 'user';

-- Create chat_rooms table if missing
CREATE TABLE IF NOT EXISTS chat_rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default room
INSERT INTO chat_rooms (id, name, description) VALUES (1, 'General', 'General chat room') ON CONFLICT (id) DO NOTHING;

-- Add foreign key constraints
ALTER TABLE chat_messages DROP CONSTRAINT IF EXISTS fk_chat_messages_room_id;
ALTER TABLE chat_messages DROP CONSTRAINT IF EXISTS fk_chat_messages_user_id;

ALTER TABLE chat_messages ADD CONSTRAINT fk_chat_messages_room_id 
FOREIGN KEY (room_id) REFERENCES chat_rooms(id) ON DELETE SET NULL;

ALTER TABLE chat_messages ADD CONSTRAINT fk_chat_messages_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
"

echo "✅ Database schema updated!"

# Setup demo account
echo "👤 Setting up demo account..."
./setup-demo.sh

echo ""
echo "🎉 Complete database setup finished!"
