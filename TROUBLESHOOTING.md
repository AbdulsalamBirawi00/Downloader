# Troubleshooting Guide

## Deployment Issues

### Render.com: "Read-only file system" error

**Error message:**
```
E: List directory /var/lib/apt/lists/partial is missing. - Acquire (30: Read-only file system)
==> Build failed 😞
```

**Cause:** Render.com's Python environment doesn't allow `apt-get` commands.

**Solution:** Use Docker environment instead of Python.

**Steps to fix:**
1. Make sure you have the `Dockerfile` in your repository
2. In Render.com dashboard:
   - Go to your service settings
   - Change **Environment** from "Python" to **"Docker"**
   - Set **Dockerfile Path** to `./Dockerfile`
   - Save changes
3. Trigger a manual redeploy

**Or create a new service:**
1. Delete the old service
2. Create new Web Service
3. Select **Docker** as environment
4. Set Dockerfile path to `./Dockerfile`
5. Add your `TELEGRAM_BOT_TOKEN` environment variable
6. Deploy!

---

### Missing Dockerfile

**Error:** "Dockerfile not found"

**Solution:**
Make sure `Dockerfile` is committed to your GitHub repository:

```bash
git add Dockerfile .dockerignore
git commit -m "Add Dockerfile for deployment"
git push
```

Then trigger a redeploy on Render.

---

### ffmpeg not found during runtime

**Symptoms:**
- Bot sends video when audio is requested
- Logs show "ffmpeg not found"

**Solution:**
Make sure you're using the Dockerfile deployment method, which automatically installs ffmpeg.

**Verify in Dockerfile:**
```dockerfile
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## Runtime Issues

### Bot not responding to messages

**Check 1: Is the bot running?**
- Check Render.com logs for errors
- Look for "Bot started. Waiting for messages..." message

**Check 2: Is the token correct?**
- Verify `TELEGRAM_BOT_TOKEN` environment variable is set
- Make sure there are no extra spaces in the token

**Check 3: Did you message the right bot?**
- Make sure you're messaging the bot username you created
- Send `/start` to initialize the conversation

**Check 4: Check logs**
```bash
# On Render.com, go to Logs tab
# Look for error messages or exceptions
```

---

### Bot sends video instead of audio

**Cause:** ffmpeg is not installed or not working.

**Solution for Render.com:**
1. Make sure you deployed with **Docker** environment
2. Check Dockerfile includes ffmpeg installation
3. Redeploy the service

**Solution for local testing:**
```bash
# Install ffmpeg
brew install ffmpeg           # macOS
sudo apt install ffmpeg       # Linux
choco install ffmpeg          # Windows

# Verify
ffmpeg -version
```

---

### Download fails with "Failed to download video"

**Common causes:**

1. **Private video** - Bot can't access private or age-restricted content
2. **Invalid URL** - Make sure the URL is correct
3. **Platform blocking** - Instagram/YouTube/Facebook may block automated downloads
4. **Video removed** - The video might have been deleted

**Solutions:**
- Make sure the video is public
- Try the URL in a browser first
- Wait a few minutes and try again (rate limiting)

---

### File too large error

**Error:** "Video is too large (XX.XMB). Telegram bot limit is 50MB."

**Solutions:**
1. **Try audio format** - Audio files are much smaller
2. **Use shorter videos** - Find a shorter clip
3. **No current workaround** - Telegram's bot API has a hard 50MB limit

---

### Session expired error

**Error:** "Session expired. Please send the URL again."

**Cause:** You waited too long to click Video/Audio button, or the bot restarted.

**Solution:** Simply send the URL again.

---

## GitHub Issues

### Push rejected

**Error:** "Updates were rejected because the remote contains work that you do not have locally"

**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

---

### Authentication failed

**Solution:**
```bash
# Use Personal Access Token instead of password
# Generate at: https://github.com/settings/tokens
# Use token as password when prompted
```

---

## Platform-Specific Issues

### Render.com

**Free tier sleeps after 15 minutes of inactivity**
- This is normal behavior
- Bot wakes up automatically when a message arrives
- First response after sleep may be slower

**Solution:** Upgrade to paid tier for always-on service

---

### Railway.app

**Free tier credit exhausted**
- Free tier gives $5/month credit
- Monitor your usage in dashboard

**Solution:**
- Add payment method for additional credit
- Or switch to Render.com

---

### Replit

**Bot stops when you close the tab**
- Free tier requires tab to be open
- Or use Replit's "Always On" feature (paid)

**Solution:**
- Keep the tab open
- Or use Render.com/Railway for true 24/7 hosting

---

## How to Get Help

### Enable Debug Logging

The bot already prints helpful debug messages. Check the logs:

**Render.com:**
1. Go to your service dashboard
2. Click **"Logs"** tab
3. Look for error messages in red

**Local testing:**
- All debug messages appear in terminal
- Look for lines starting with "Error:" or Python tracebacks

### Common Log Messages

**"Successfully sent video to chat XXXXX"** - ✅ Working correctly

**"Failed to fetch [platform] page"** - ❌ Can't download from that URL

**"ffmpeg not found"** - ⚠️ Audio extraction won't work

**"HTTP Error: 403"** - ❌ Blocked by platform

**"Bot started. Waiting for messages..."** - ✅ Bot is running

---

## Still Need Help?

1. **Check this guide first** - Most issues are covered here
2. **Check deployment logs** - Error messages are very helpful
3. **Verify environment variables** - Make sure `TELEGRAM_BOT_TOKEN` is set
4. **Test locally first** - Run `python3 test_setup.py`
5. **Review documentation** - README.md, DEPLOY.md, QUICKSTART.md

---

## Quick Fixes Checklist

- [ ] Using Docker environment on Render (not Python)
- [ ] Dockerfile exists in repository
- [ ] TELEGRAM_BOT_TOKEN environment variable is set
- [ ] Token has no extra spaces or quotes
- [ ] Bot is running (check logs)
- [ ] Messaging the correct bot username
- [ ] Video URL is public and valid
- [ ] ffmpeg is installed (for audio extraction)
- [ ] File size is under 50MB
- [ ] Latest code is pushed to GitHub

---

**Most deployment issues are fixed by using Docker instead of Python environment!**
