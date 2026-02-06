-- Migration: Add user authentication schema
-- Created: 2026-02-07
-- Description: Adds users table and links user_sessions to users

-- Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for fast lookups
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Add user_id column to user_sessions if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'user_sessions' AND column_name = 'user_id'
    ) THEN
        ALTER TABLE user_sessions ADD COLUMN user_id INTEGER REFERENCES users(id);
    END IF;
END $$;

-- Create index on user_id for performance
CREATE INDEX IF NOT EXISTS ix_user_sessions_user_id ON user_sessions(user_id);

-- Display current schema for verification
SELECT 'Migration completed successfully!' AS status;
