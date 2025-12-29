"""
Video downloaders for Instagram, YouTube, and Facebook using yt-dlp
Supports 1000+ websites with high reliability
"""

import subprocess
import tempfile
import os
import json


def download_video_ytdlp(url):
    """
    Download video using yt-dlp with multiple fallback methods
    Returns video data as bytes
    """
    # Try multiple extraction methods in order of success rate
    methods = [
        {
            'name': 'iOS Client',
            'args': [
                '--extractor-args', 'youtube:player_client=ios,web',
                '--extractor-args', 'youtube:skip=hls,dash',
            ]
        },
        {
            'name': 'Android Client',
            'args': [
                '--extractor-args', 'youtube:player_client=android,web',
            ]
        },
        {
            'name': 'Web Embed',
            'args': [
                '--extractor-args', 'youtube:player_client=web_embedded',
            ]
        },
        {
            'name': 'Mobile Web',
            'args': [
                '--extractor-args', 'youtube:player_client=mweb,web',
            ]
        }
    ]

    last_error = None

    for method in methods:
        try:
            print(f"Trying {method['name']} method for: {url}")

            # Create temporary directory for downloads
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, 'video.%(ext)s')

                # Base yt-dlp command
                cmd = [
                    'yt-dlp',
                    '--no-warnings',
                    '--no-playlist',
                    '--format', 'best[ext=mp4][height<=720]/best[ext=mp4]/best',  # Limit quality to avoid bot detection
                    '--output', output_path,
                    '--max-filesize', '50M',  # Telegram limit
                    '--no-check-certificate',
                    # Better user agent
                    '--user-agent', 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
                    # Age gate bypass
                    '--age-limit', '100',
                ]

                # Add method-specific arguments
                cmd.extend(method['args'])
                cmd.append(url)

                # Run yt-dlp
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minutes timeout
                )

                if result.returncode == 0:
                    # Success! Find and read the downloaded file
                    files = os.listdir(temp_dir)
                    if files:
                        video_file = os.path.join(temp_dir, files[0])
                        with open(video_file, 'rb') as f:
                            video_data = f.read()
                        print(f"✅ {method['name']} succeeded! Downloaded {len(video_data)} bytes")
                        return video_data

                # This method failed, try next one
                error_msg = result.stderr or result.stdout
                last_error = error_msg
                print(f"❌ {method['name']} failed, trying next method...")

        except subprocess.TimeoutExpired:
            last_error = "Download timed out"
            print(f"❌ {method['name']} timed out, trying next method...")
            continue
        except Exception as e:
            last_error = str(e)
            print(f"❌ {method['name']} error: {e}, trying next method...")
            continue

    # All methods failed
    print(f"❌ All download methods failed")

    # Check if it's a bot detection error
    if last_error and ('Sign in to confirm' in last_error or 'bot' in last_error.lower()):
        raise Exception("YouTube bot detection - This video requires advanced authentication. Try a different video or use the bot later when YouTube restrictions are lighter.")
    else:
        raise Exception(f"Download failed after trying all methods: {last_error[:200] if last_error else 'Unknown error'}")


def download_instagram(url):
    """Download video from Instagram using yt-dlp"""
    try:
        return download_video_ytdlp(url)
    except Exception as e:
        raise Exception(f"Instagram download failed: {str(e)}")


def download_youtube(url):
    """Download video from YouTube using yt-dlp"""
    try:
        return download_video_ytdlp(url)
    except Exception as e:
        raise Exception(f"YouTube download failed: {str(e)}")


def download_facebook(url):
    """Download video from Facebook using yt-dlp"""
    try:
        return download_video_ytdlp(url)
    except Exception as e:
        raise Exception(f"Facebook download failed: {str(e)}")


def extract_audio(video_data, filename):
    """
    Extract audio from video using ffmpeg
    Returns audio data as bytes or None if extraction fails
    """
    try:
        # Check if ffmpeg is available
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                print("ffmpeg not found. Install ffmpeg to extract audio.")
                return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("ffmpeg not found. Install ffmpeg to extract audio.")
            return None

        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_data)
            temp_video_path = temp_video.name

        # Output audio file
        temp_audio_path = temp_video_path.replace('.mp4', '.mp3')

        try:
            # Extract audio using ffmpeg
            cmd = [
                'ffmpeg',
                '-i', temp_video_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-q:a', '2',  # High quality
                '-y',  # Overwrite
                temp_audio_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=60  # 60 seconds timeout
            )

            if result.returncode == 0 and os.path.exists(temp_audio_path):
                # Read the audio file
                with open(temp_audio_path, 'rb') as audio_file:
                    audio_data = audio_file.read()

                # Clean up
                os.remove(temp_video_path)
                os.remove(temp_audio_path)

                print(f"Successfully extracted audio ({len(audio_data)} bytes)")
                return audio_data
            else:
                print(f"ffmpeg error: {result.stderr.decode('utf-8', errors='ignore')}")
                # Clean up
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
                return None

        except subprocess.TimeoutExpired:
            print("Audio extraction timed out")
            # Clean up
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            return None

    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None


def download_audio_directly(url):
    """
    Download audio directly using yt-dlp with multiple fallback methods
    Returns audio data as bytes
    """
    # Try multiple extraction methods
    methods = [
        {
            'name': 'iOS Client Audio',
            'args': [
                '--extractor-args', 'youtube:player_client=ios,web',
            ]
        },
        {
            'name': 'Android Client Audio',
            'args': [
                '--extractor-args', 'youtube:player_client=android,web',
            ]
        }
    ]

    last_error = None

    for method in methods:
        try:
            print(f"Trying {method['name']} method for: {url}")

            # Create temporary directory for downloads
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, 'audio.%(ext)s')

                # Base yt-dlp command for audio
                cmd = [
                    'yt-dlp',
                    '--no-warnings',
                    '--no-playlist',
                    '--extract-audio',
                    '--audio-format', 'mp3',
                    '--audio-quality', '0',  # Best quality
                    '--output', output_path,
                    '--max-filesize', '50M',  # Telegram limit
                    '--no-check-certificate',
                    # Better user agent
                    '--user-agent', 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
                    # Age gate bypass
                    '--age-limit', '100',
                ]

                # Add method-specific arguments
                cmd.extend(method['args'])
                cmd.append(url)

                # Run yt-dlp
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minutes timeout
                )

                if result.returncode == 0:
                    # Success! Find and read the downloaded file
                    files = os.listdir(temp_dir)
                    if files:
                        audio_file = os.path.join(temp_dir, files[0])
                        with open(audio_file, 'rb') as f:
                            audio_data = f.read()
                        print(f"✅ {method['name']} succeeded! Downloaded {len(audio_data)} bytes")
                        return audio_data

                # This method failed, try next one
                error_msg = result.stderr or result.stdout
                last_error = error_msg
                print(f"❌ {method['name']} failed, trying next method...")

        except subprocess.TimeoutExpired:
            last_error = "Download timed out"
            print(f"❌ {method['name']} timed out, trying next method...")
            continue
        except Exception as e:
            last_error = str(e)
            print(f"❌ {method['name']} error: {e}, trying next method...")
            continue

    # All audio methods failed, try fallback: download video then extract
    print("All audio methods failed. Trying fallback: download video then extract audio...")
    try:
        video_data = download_video_ytdlp(url)
        return extract_audio(video_data, 'video.mp4')
    except Exception as e:
        # Complete failure
        if last_error and ('Sign in to confirm' in last_error or 'bot' in last_error.lower()):
            raise Exception("YouTube bot detection - This video requires advanced authentication. Try a different video or use the bot later.")
        else:
            raise Exception(f"Audio download failed: {str(e)[:200]}")
