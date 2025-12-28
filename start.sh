#!/bin/bash

# Simple startup script for the Telegram bot

echo "🤖 Telegram Video Downloader Bot"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Check if bot token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN environment variable is not set!"
    echo ""
    echo "Please set your bot token:"
    echo "  export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
    echo ""
    echo "Get your bot token from @BotFather on Telegram:"
    echo "  1. Open Telegram and search for @BotFather"
    echo "  2. Send /newbot command"
    echo "  3. Follow instructions and copy the token"
    echo ""
    exit 1
fi

echo "✅ Bot token is set"
echo ""
echo "🚀 Starting bot..."
echo "Press Ctrl+C to stop"
echo ""

# Run the bot
python3 bot.py
