#!/usr/bin/env python3
"""
Telegram Video Downloader Bot (with HTTP server for Render Web Service)
Downloads videos from Instagram, YouTube, and Facebook using only Python standard library
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import sys
import time
import ssl
import subprocess
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from downloaders import download_instagram, download_youtube, download_facebook, extract_audio


# Simple HTTP server for health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Bot is running!')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass


def start_http_server():
    """Start HTTP server in background thread"""
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"HTTP server listening on port {port}")
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0

        # Create SSL context to handle HTTPS
        self.ssl_context = ssl.create_default_context()

        # Store pending downloads {chat_id: {'url': url, 'platform': platform}}
        self.pending_downloads = {}

    def make_request(self, method, data=None, files=None):
        """Make HTTP request to Telegram API"""
        url = f"{self.api_url}/{method}"

        try:
            if files:
                # Handle file upload with multipart/form-data
                boundary = '----WebKitFormBoundary' + ''.join([str(int(time.time() * 1000))])
                body = []

                # Add regular fields
                if data:
                    for key, value in data.items():
                        body.append(f'--{boundary}'.encode())
                        body.append(f'Content-Disposition: form-data; name="{key}"'.encode())
                        body.append(b'')
                        body.append(str(value).encode())

                # Add file
                for field_name, file_data in files.items():
                    filename, content = file_data
                    body.append(f'--{boundary}'.encode())
                    body.append(f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"'.encode())
                    body.append(b'Content-Type: video/mp4')
                    body.append(b'')
                    body.append(content)

                body.append(f'--{boundary}--'.encode())
                body.append(b'')

                body_bytes = b'\r\n'.join(body)

                headers = {
                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                    'Content-Length': str(len(body_bytes))
                }

                req = urllib.request.Request(url, data=body_bytes, headers=headers)

            elif data:
                # Regular POST request with JSON
                headers = {'Content-Type': 'application/json'}
                json_data = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=json_data, headers=headers)
            else:
                # GET request
                req = urllib.request.Request(url)

            with urllib.request.urlopen(req, context=self.ssl_context, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
            return None
        except Exception as e:
            print(f"Error making request: {e}")
            return None

    def get_updates(self, offset=None, timeout=30):
        """Get updates from Telegram using long polling"""
        data = {'timeout': timeout}
        if offset:
            data['offset'] = offset

        return self.make_request('getUpdates', data=data)

    def send_message(self, chat_id, text, reply_markup=None):
        """Send text message to user"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        if reply_markup:
            data['reply_markup'] = reply_markup
        return self.make_request('sendMessage', data=data)

    def send_video(self, chat_id, video_data, filename, caption=None):
        """Send video file to user"""
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption

        files = {'video': (filename, video_data)}
        return self.make_request('sendVideo', data=data, files=files)

    def send_audio(self, chat_id, audio_data, filename, caption=None):
        """Send audio file to user"""
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption

        files = {'audio': (filename, audio_data)}
        return self.make_request('sendAudio', data=data, files=files)

    def send_voice(self, chat_id, voice_data, caption=None):
        """Send voice message to user"""
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption

        files = {'voice': ('voice.ogg', voice_data)}
        return self.make_request('sendVoice', data=data, files=files)

    def answer_callback_query(self, callback_query_id, text=None):
        """Answer callback query from inline keyboard"""
        data = {'callback_query_id': callback_query_id}
        if text:
            data['text'] = text
        return self.make_request('answerCallbackQuery', data=data)

    def send_chat_action(self, chat_id, action='upload_video'):
        """Send chat action (typing, uploading, etc.)"""
        data = {
            'chat_id': chat_id,
            'action': action
        }
        return self.make_request('sendChatAction', data=data)

    def process_message(self, message):
        """Process incoming message"""
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id or not text:
            return

        # Handle /start command
        if text.startswith('/start'):
            welcome_msg = """
<b>🎥 Video Downloader Bot</b>

Send me a video URL from:
• Instagram (Reels/Posts)
• YouTube (Videos/Shorts)
• Facebook (Videos)

Choose to download as:
• 📹 Video - Full video with sound
• 🎵 Audio - Audio only (MP3)

<b>Example:</b>
https://www.instagram.com/reel/xxxxx/
https://youtu.be/xxxxx
https://www.facebook.com/xxxxx
"""
            self.send_message(chat_id, welcome_msg)
            return

        # Check if message contains a URL
        if not ('instagram.com' in text or 'youtube.com' in text or 'youtu.be' in text or 'facebook.com' in text or 'fb.watch' in text):
            self.send_message(chat_id, "❌ Please send a valid Instagram, YouTube, or Facebook video URL.")
            return

        # Determine platform
        platform = ""
        if 'instagram.com' in text:
            platform = "Instagram"
        elif 'youtube.com' in text or 'youtu.be' in text:
            platform = "YouTube"
        elif 'facebook.com' in text or 'fb.watch' in text:
            platform = "Facebook"

        # Store the URL for later
        self.pending_downloads[chat_id] = {
            'url': text,
            'platform': platform
        }

        # Create inline keyboard with Video and Audio options
        keyboard = {
            'inline_keyboard': [
                [
                    {'text': '📹 Video', 'callback_data': 'format_video'},
                    {'text': '🎵 Audio', 'callback_data': 'format_audio'}
                ]
            ]
        }

        self.send_message(
            chat_id,
            f"📎 <b>{platform}</b> link detected!\n\nChoose download format:",
            reply_markup=keyboard
        )

    def process_callback_query(self, callback_query):
        """Process callback query from inline keyboard"""
        callback_id = callback_query.get('id')
        chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
        data = callback_query.get('data', '')

        if not chat_id or not data:
            return

        # Answer the callback query
        self.answer_callback_query(callback_id)

        # Check if we have a pending download for this chat
        if chat_id not in self.pending_downloads:
            self.send_message(chat_id, "❌ Session expired. Please send the URL again.")
            return

        download_info = self.pending_downloads[chat_id]
        url = download_info['url']
        platform = download_info['platform']

        # Determine format
        format_type = 'video' if data == 'format_video' else 'audio'

        # Send processing message
        if format_type == 'video':
            self.send_message(chat_id, f"📥 Downloading {platform} video...")
        else:
            self.send_message(chat_id, f"📥 Downloading {platform} audio...")

        # Download video
        video_data = None
        filename = "video.mp4"

        try:
            if platform == "Instagram":
                self.send_chat_action(chat_id, 'upload_video' if format_type == 'video' else 'upload_audio')
                video_data = download_instagram(url)
                filename = "instagram_video.mp4"

            elif platform == "YouTube":
                self.send_chat_action(chat_id, 'upload_video' if format_type == 'video' else 'upload_audio')
                video_data = download_youtube(url)
                filename = "youtube_video.mp4"

            elif platform == "Facebook":
                self.send_chat_action(chat_id, 'upload_video' if format_type == 'video' else 'upload_audio')
                video_data = download_facebook(url)
                filename = "facebook_video.mp4"

            if video_data and len(video_data) > 0:
                # Check file size (Telegram limit is 50MB for bots)
                size_mb = len(video_data) / (1024 * 1024)

                if size_mb > 50:
                    self.send_message(chat_id, f"❌ File is too large ({size_mb:.1f}MB). Telegram bot limit is 50MB.")
                    # Clean up
                    del self.pending_downloads[chat_id]
                    return

                # If audio format is requested, extract audio
                if format_type == 'audio':
                    self.send_message(chat_id, "🎵 Extracting audio...")
                    audio_data = extract_audio(video_data, filename)

                    if audio_data:
                        size_mb = len(audio_data) / (1024 * 1024)
                        audio_filename = filename.replace('.mp4', '.mp3')
                        self.send_message(chat_id, f"📤 Uploading audio ({size_mb:.1f}MB)...")
                        result = self.send_audio(chat_id, audio_data, audio_filename, f"✅ Downloaded from {platform}")

                        if result and result.get('ok'):
                            print(f"Successfully sent audio to chat {chat_id}")
                        else:
                            self.send_message(chat_id, "❌ Failed to send audio. Please try again.")
                    else:
                        self.send_message(chat_id, "❌ Failed to extract audio. Sending as video instead...")
                        # Fallback to video
                        result = self.send_video(chat_id, video_data, filename, f"✅ Downloaded from {platform}")
                else:
                    # Send as video
                    self.send_message(chat_id, f"📤 Uploading video ({size_mb:.1f}MB)...")
                    result = self.send_video(chat_id, video_data, filename, f"✅ Downloaded from {platform}")

                    if result and result.get('ok'):
                        print(f"Successfully sent video to chat {chat_id}")
                    else:
                        self.send_message(chat_id, "❌ Failed to send video. Please try again.")

                # Clean up pending download
                del self.pending_downloads[chat_id]
            else:
                self.send_message(chat_id, f"❌ Failed to download from {platform}. The URL might be invalid or the video is private.")
                # Clean up
                del self.pending_downloads[chat_id]

        except Exception as e:
            print(f"Error processing download: {e}")
            self.send_message(chat_id, f"❌ Error: {str(e)}")
            # Clean up
            if chat_id in self.pending_downloads:
                del self.pending_downloads[chat_id]

    def start_polling(self):
        """Start the bot with long polling"""
        print("Bot started. Waiting for messages...")

        while True:
            try:
                updates = self.get_updates(offset=self.last_update_id + 1, timeout=30)

                if updates and updates.get('ok'):
                    for update in updates.get('result', []):
                        self.last_update_id = update.get('update_id', 0)

                        # Process message
                        if 'message' in update:
                            self.process_message(update['message'])

                        # Process callback query (from inline keyboard)
                        elif 'callback_query' in update:
                            self.process_callback_query(update['callback_query'])

                time.sleep(0.5)

            except KeyboardInterrupt:
                print("\nBot stopped.")
                sys.exit(0)
            except Exception as e:
                print(f"Error in polling loop: {e}")
                time.sleep(5)


def main():
    # Get bot token from environment variable
    token = os.environ.get('TELEGRAM_BOT_TOKEN')

    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Usage: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        sys.exit(1)

    # Start HTTP server for health checks (needed for Render Web Service)
    start_http_server()

    # Create and start bot
    bot = TelegramBot(token)
    bot.start_polling()


if __name__ == '__main__':
    main()
