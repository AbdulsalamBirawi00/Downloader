# Quick Deployment Guide - 100% FREE

This guide will help you deploy your bot completely free in under 10 minutes.

## Method 1: Render.com (Recommended - Easiest)

### Step 1: Get Your Bot Token

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name (e.g., "My Video Downloader")
5. Choose a username (e.g., "my_video_dl_bot")
6. **Copy the token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Upload Code to GitHub

```bash
# In your terminal (in the telegram_bot folder):

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Create a new repository on GitHub.com (click the + icon)
# Then connect it:
git remote add origin https://github.com/YOUR_USERNAME/telegram-video-bot.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** and authorize Render
4. Select your `telegram-video-bot` repository
5. Configure:
   - **Name**: `telegram-video-bot` (or anything you like)
   - **Environment**: `Python 3`
   - **Build Command**: `apt-get update && apt-get install -y ffmpeg` (for audio extraction)
   - **Start Command**: `python3 bot.py`
   - **Plan**: Select **"Free"**
6. Click **"Advanced"** and add Environment Variable:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Paste your bot token from Step 1
7. Click **"Create Web Service"**

**Note:** The build command installs ffmpeg for audio extraction. Without it, the bot will still work but only send videos.

### Step 4: Wait for Deployment

- Render will deploy your bot (takes 2-3 minutes)
- Once it says "Live", your bot is running!
- Open Telegram and send `/start` to your bot

**Done! Your bot is now running 24/7 for free!**

---

## Method 2: Railway.app (Also Easy)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Add environment variable:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
6. Railway will automatically detect Python and deploy!

**Note:** Railway free tier gives you $5/month credit. Should be enough for this bot.

---

## Method 3: Replit (Simplest - No GitHub Needed)

1. Go to [replit.com](https://replit.com) and sign up
2. Click **"Create Repl"**
3. Choose **"Python"** template
4. Name it `telegram-video-bot`
5. Delete the default `main.py`
6. Upload all your files:
   - `bot.py`
   - `downloaders.py`
   - `requirements.txt`
7. Click the **"Secrets"** tab (lock icon)
8. Add secret:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
9. In the main file selector, select `bot.py`
10. Click **"Run"**

Your bot is now running!

**To keep it running 24/7 on Replit:**
- Replit free tier may sleep after inactivity
- Consider Replit's "Always On" feature (paid) or use Render/Railway instead

---

## Method 4: PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Go to **"Files"** tab
4. Upload your bot files
5. Open **"Bash"** console
6. Run:
```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
python3 bot.py
```

**To keep running 24/7:**
- Free tier doesn't support always-on apps
- You'll need to keep the console open
- Or upgrade to paid tier ($5/month) for scheduled tasks

---

## Method 5: Google Cloud Run (Free Tier)

More advanced but completely free:

1. Install Google Cloud CLI
2. Create new project on [console.cloud.google.com](https://console.cloud.google.com)
3. Enable Cloud Run API
4. Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
CMD ["python3", "bot.py"]
```

5. Deploy:
```bash
gcloud run deploy telegram-bot \
  --source . \
  --region us-central1 \
  --set-env-vars TELEGRAM_BOT_TOKEN=your_token_here \
  --allow-unauthenticated
```

---

## Comparison Table

| Platform | Free Tier | Always On | Ease | Best For |
|----------|-----------|-----------|------|----------|
| **Render.com** | ✅ Yes | ✅ Yes* | ⭐⭐⭐⭐⭐ | **Recommended** |
| **Railway.app** | ✅ $5/mo credit | ✅ Yes | ⭐⭐⭐⭐⭐ | Great alternative |
| **Replit** | ✅ Yes | ⚠️ May sleep | ⭐⭐⭐⭐ | Quick testing |
| **PythonAnywhere** | ✅ Limited | ❌ No | ⭐⭐⭐ | Learning |
| **Google Cloud** | ✅ Yes | ✅ Yes | ⭐⭐ | Advanced users |

*Render free tier may sleep after 15 minutes of inactivity but wakes up automatically

---

## Testing Your Bot

1. Open Telegram
2. Search for your bot username
3. Click "Start" or send `/start`
4. Send a video URL, for example:
   - Instagram: `https://www.instagram.com/reel/xxxxx/`
   - YouTube: `https://youtu.be/xxxxx`
   - Facebook: `https://www.facebook.com/xxxxx`
5. Wait for the bot to download and send the video!

---

## Troubleshooting

### Bot not responding?

1. Check deployment logs on your platform
2. Verify `TELEGRAM_BOT_TOKEN` is set correctly
3. Make sure bot is running (check platform dashboard)

### Downloads failing?

1. Make sure URL is public (not private/age-restricted)
2. Check bot logs for specific errors
3. Platforms may block after many requests

### Need help?

- Check the main README.md file
- Review deployment platform documentation
- Verify all files are uploaded correctly

---

**Congratulations! Your bot is now deployed and running for free! 🎉**
