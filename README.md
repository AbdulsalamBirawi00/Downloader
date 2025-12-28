# Telegram Video Downloader Bot

A Telegram bot that downloads videos from Instagram, YouTube, and Facebook using **only Python standard library** - no third-party packages required!

## Features

- ✅ Download Instagram Reels and Posts
- ✅ Download YouTube Videos and Shorts
- ✅ Download Facebook Videos
- ✅ **Choose format: Video or Audio**
- ✅ Pure Python - No external dependencies
- ✅ Free deployment options
- ✅ Easy to use - just send a URL

## Requirements

- Python 3.7 or higher
- Telegram Bot Token (free from [@BotFather](https://t.me/BotFather))
- **ffmpeg** (optional, required for audio extraction only)

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to choose a name and username
4. Copy the **bot token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Set Up the Bot Token

Set your bot token as an environment variable:

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

**Windows (Command Prompt):**
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
```

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

### 3. Install ffmpeg (Optional - for Audio Extraction)

If you want to extract audio from videos, install ffmpeg:

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add to PATH
3. Or use Chocolatey: `choco install ffmpeg`

**Verify installation:**
```bash
ffmpeg -version
```

**Note:** If ffmpeg is not installed, the bot will still work but will send videos when audio is requested.

### 4. Run the Bot Locally

```bash
python3 bot.py
```

The bot will start and wait for messages. Send `/start` to your bot on Telegram to begin!

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send any video URL from:
   - Instagram: `https://www.instagram.com/reel/xxxxx/`
   - YouTube: `https://youtu.be/xxxxx` or `https://www.youtube.com/watch?v=xxxxx`
   - Facebook: `https://www.facebook.com/xxxxx` or `https://fb.watch/xxxxx`
4. **Choose format:** Click either:
   - **📹 Video** - Download full video with sound
   - **🎵 Audio** - Extract and download audio only (MP3)
5. Wait for the bot to download and send you the file!

## Free Deployment Options

### Option 1: Render.com (Recommended - Easiest)

Render offers free tier hosting that's perfect for this bot.

1. Create account at [render.com](https://render.com)
2. Create a new **Web Service**
3. Connect your GitHub repository (you'll need to push this code to GitHub first)
4. Configure:
   - **Environment**: **Docker** (Use Docker, not Python!)
   - **Dockerfile Path**: `./Dockerfile`
5. Add environment variable:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
6. Deploy!

**Why Docker?** The Dockerfile automatically installs ffmpeg for audio extraction. Using Docker ensures all dependencies are properly installed.

**Note:** Render free tier may sleep after inactivity. The bot will wake up when Telegram sends an update.

### Option 2: Railway.app

Railway offers a generous free tier.

1. Create account at [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Add environment variable `TELEGRAM_BOT_TOKEN`
4. Deploy automatically!

### Option 3: PythonAnywhere

Free tier available with some limitations.

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files to PythonAnywhere
3. Open a Bash console
4. Set environment variable: `export TELEGRAM_BOT_TOKEN='your_token'`
5. Run: `python3 bot.py`
6. Keep the console open or set up a scheduled task

### Option 4: Replit

Free hosting with Replit (may sleep after inactivity).

1. Create account at [replit.com](https://replit.com)
2. Create new Python Repl
3. Upload your files
4. Add Secret (environment variable):
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
5. Click Run!

### Option 5: Google Cloud Run (Free Tier)

Google Cloud offers free tier that includes Cloud Run.

1. Create Google Cloud account
2. Create new project
3. Enable Cloud Run API
4. Deploy using `gcloud` CLI or console
5. Set environment variable for bot token

### Option 6: GitHub + Workflows (Advanced)

Run the bot using GitHub Actions (limited free minutes per month).

Create `.github/workflows/bot.yml`:

```yaml
name: Telegram Bot
on:
  schedule:
    - cron: '*/5 * * * *'  # Run every 5 minutes
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run bot
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        run: python3 bot.py &
        timeout-minutes: 5
```

## Deployment Steps (General)

### Step 1: Prepare Your Code

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"
```

### Step 2: Push to GitHub

```bash
# Create new repository on GitHub
# Then push your code

git remote add origin https://github.com/yourusername/telegram-video-bot.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Your Chosen Platform

Follow the specific platform instructions above.

## Important Notes

### Limitations

⚠️ **Important Warnings:**

1. **Platform Changes**: Instagram, YouTube, and Facebook frequently update their websites. This may cause the downloaders to stop working.

2. **Private Content**: Cannot download private or age-restricted videos

3. **Rate Limiting**: Platforms may block requests if you download too many videos

4. **File Size**: Telegram bots can only send files up to 50MB

5. **Terms of Service**: Downloading videos may violate platform ToS. Use responsibly and only download content you have permission to download.

6. **No Audio (Sometimes)**: Some YouTube videos may download without audio due to separate audio/video streams

### Legal Disclaimer

This bot is for **educational purposes only**. Users are responsible for:
- Respecting copyright laws
- Following platform Terms of Service
- Obtaining permission before downloading others' content
- Not using downloaded content for commercial purposes without permission

## Troubleshooting

### Bot Not Responding

1. Check if bot token is correct
2. Verify environment variable is set
3. Check bot logs for errors

### Download Fails

1. Verify the URL is correct and publicly accessible
2. Check if video is private or age-restricted
3. Some videos may require login - bot cannot handle authenticated content

### Video Quality Issues

The bot downloads the first available video format. For better quality, platforms like YouTube may require more complex stream selection.

## File Structure

```
telegram_bot/
├── bot.py              # Main bot logic with Telegram API
├── downloaders.py      # Video download functions
├── requirements.txt    # Empty (no dependencies!)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## How It Works

1. **Bot Polling**: The bot uses Telegram's `getUpdates` method with long polling to receive messages
2. **URL Detection**: Checks incoming messages for Instagram, YouTube, or Facebook URLs
3. **Video Extraction**: Scrapes the webpage HTML to find video URLs
4. **Download**: Downloads the video file using `urllib`
5. **Upload**: Sends the video back to the user via Telegram API

## Contributing

Feel free to improve the downloaders or add support for more platforms!

## License

MIT License - Use freely for educational purposes

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages in bot logs
3. Verify the URL is publicly accessible

---

**Made with ❤️ using only Python standard library**
