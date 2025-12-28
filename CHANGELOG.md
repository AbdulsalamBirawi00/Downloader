# Changelog

## Version 2.0 - Audio Extraction Feature

### New Features

**🎵 Audio Download Option**
- Users can now choose to download videos as audio (MP3) files
- Inline keyboard appears when sending a video URL with two options:
  - 📹 Video - Full video with sound
  - 🎵 Audio - Audio only (MP3 format)

**Audio Extraction**
- Uses ffmpeg to extract audio from videos
- High-quality MP3 output (quality level 2)
- Automatic fallback to video if ffmpeg is not installed or extraction fails

### Technical Changes

**bot.py:**
- Added inline keyboard support for format selection
- New methods: `send_audio()`, `send_voice()`, `answer_callback_query()`
- Added `process_callback_query()` to handle button clicks
- Added `pending_downloads` dictionary to store user selections
- Updated `send_message()` to support reply_markup parameter
- Modified polling loop to handle callback queries

**downloaders.py:**
- Added `extract_audio()` function for audio extraction
- Uses subprocess to call ffmpeg
- Creates temporary files for conversion
- Handles cleanup automatically
- Returns audio data as bytes or None on failure

**Documentation:**
- Updated README.md with audio feature information
- Added ffmpeg installation instructions
- Updated QUICKSTART.md and DEPLOY.md
- Modified render.yaml to install ffmpeg during build
- Updated test_setup.py to check for ffmpeg availability

### Dependencies

**Optional:**
- ffmpeg (system package) - Required for audio extraction only
- Bot works without ffmpeg but will only send videos

### Deployment Notes

**For Render.com:**
- Build command updated to: `apt-get update && apt-get install -y ffmpeg`
- This installs ffmpeg automatically during deployment

**For other platforms:**
- Ensure ffmpeg is installed on the server
- Linux: `apt install ffmpeg` or `yum install ffmpeg`
- Docker: Add `RUN apt-get update && apt-get install -y ffmpeg` to Dockerfile

### User Experience

1. User sends video URL
2. Bot shows inline keyboard with Video/Audio options
3. User clicks preferred format
4. Bot downloads and processes the video
5. If Audio selected:
   - Checks for ffmpeg
   - Extracts audio to MP3
   - Sends as audio file
   - Falls back to video if extraction fails
6. User receives the file

### File Size Limits

- Videos: 50MB (Telegram bot limit)
- Audio: Typically 5-10x smaller than video
- Audio extraction helps download larger content within Telegram limits

---

## Version 1.0 - Initial Release

### Features
- Download videos from Instagram, YouTube, and Facebook
- Pure Python implementation using only standard library
- Long polling for receiving messages
- Support for multiple platforms
- Free deployment options
- Comprehensive documentation
