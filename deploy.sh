#!/bin/bash
# Deployment script for Spanish Vocabulary App
# This script handles deployment to EC2 server

set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Navigate to app directory
cd ~/spanish-vocab || exit 1

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Install/update Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build production CSS with Tailwind
echo "🎨 Building production CSS..."
npm run build:css:prod

# Activate Python virtual environment
echo "🐍 Activating Python virtual environment..."
source venv/bin/activate

# Install/update Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python3 -m flask db upgrade

# Restart the application
echo "🔄 Restarting application service..."
sudo systemctl restart spanish-vocab

# Wait a moment for service to start
sleep 2

# Check service status
echo "✅ Checking service status..."
sudo systemctl status spanish-vocab --no-pager

echo ""
echo "✨ Deployment completed successfully!"
echo "🌐 App is live at: https://spanish-vocab.duckdns.org"
