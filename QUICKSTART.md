# Quick Start Guide

Get your bot running in 5 minutes! Now with **Audio Extraction** feature!

## Step 1: Get Bot Token (2 minutes)

1. Open Telegram
2. Search `@BotFather`
3. Send `/newbot`
4. Follow prompts
5. **Copy your token**

## Step 2: Test Locally (1 minute)

```bash
# Set your token
export TELEGRAM_BOT_TOKEN='paste_your_token_here'

# Test setup
python3 test_setup.py

# If all tests pass, run bot
python3 bot.py
```

## Step 3: Try Your Bot (1 minute)

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Send a video URL:
   - Instagram: `https://www.instagram.com/reel/xxxxx/`
   - YouTube: `https://youtu.be/xxxxx`
   - Facebook: `https://www.facebook.com/xxxxx`
5. Choose format: **📹 Video** or **🎵 Audio**
6. Get your download!

**Optional:** Install ffmpeg for audio extraction:
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows: Download from ffmpeg.org
```

## Step 4: Deploy for Free (5 minutes)

### Render.com (Recommended)

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git push -u origin main
```

2. Go to [render.com](https://render.com)
3. New Web Service → Connect GitHub
4. Select your repo
5. Settings:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - Add Environment Variable:
     - `TELEGRAM_BOT_TOKEN` = your token
6. Deploy!

**Done!** Your bot runs 24/7 for free.

## Alternative: Replit (No GitHub Needed)

1. Go to [replit.com](https://replit.com)
2. Create Python Repl
3. Upload files
4. Add Secret: `TELEGRAM_BOT_TOKEN`
5. Run!

---

## Commands

**For Bot Users:**
- `/start` - Show welcome message

**For You:**
```bash
# Local testing
./start.sh              # Linux/Mac
start.bat              # Windows

# Verify setup
python3 test_setup.py

# Run bot
python3 bot.py
```

## Files Overview

- `bot.py` - Main bot (Telegram API)
- `downloaders.py` - Video downloaders
- `test_setup.py` - Setup verification
- `start.sh/bat` - Easy startup
- `README.md` - Full documentation
- `DEPLOY.md` - Deployment guide

## Troubleshooting

**Bot not responding?**
- Check token is correct
- Verify bot is running
- Check logs for errors

**Can't download?**
- URL must be public
- Video size < 50MB
- Not age-restricted

**Need help?**
- Read `README.md`
- Read `DEPLOY.md`
- Check bot logs

---

**That's it! Happy downloading! 🎉**
