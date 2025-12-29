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
    Download video using yt-dlp
    Returns video data as bytes
    """
    try:
        # Create temporary directory for downloads
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'video.%(ext)s')

            # yt-dlp command
            cmd = [
                'yt-dlp',
                '--no-warnings',
                '--no-playlist',
                '--format', 'best[ext=mp4]/best',  # Prefer MP4 format
                '--output', output_path,
                '--max-filesize', '50M',  # Telegram limit
                '--no-check-certificate',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                url
            ]

            print(f"Downloading with yt-dlp: {url}")

            # Run yt-dlp
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                print(f"yt-dlp error: {error_msg}")
                raise Exception(f"Download failed: {error_msg[:200]}")

            # Find the downloaded file
            files = os.listdir(temp_dir)
            if not files:
                raise Exception("No file was downloaded")

            video_file = os.path.join(temp_dir, files[0])

            # Read the video file
            with open(video_file, 'rb') as f:
                video_data = f.read()

            print(f"Successfully downloaded {len(video_data)} bytes")
            return video_data

    except subprocess.TimeoutExpired:
        raise Exception("Download timed out (exceeded 2 minutes)")
    except Exception as e:
        print(f"Download error: {e}")
        raise


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
    Download audio directly using yt-dlp (faster than downloading video then extracting)
    Returns audio data as bytes
    """
    try:
        # Create temporary directory for downloads
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'audio.%(ext)s')

            # yt-dlp command for audio
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
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                url
            ]

            print(f"Downloading audio with yt-dlp: {url}")

            # Run yt-dlp
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                print(f"yt-dlp audio error: {error_msg}")
                # Try fallback: download video then extract
                print("Trying fallback: download video then extract audio...")
                video_data = download_video_ytdlp(url)
                return extract_audio(video_data, 'video.mp4')

            # Find the downloaded file
            files = os.listdir(temp_dir)
            if not files:
                raise Exception("No audio file was downloaded")

            audio_file = os.path.join(temp_dir, files[0])

            # Read the audio file
            with open(audio_file, 'rb') as f:
                audio_data = f.read()

            print(f"Successfully downloaded audio {len(audio_data)} bytes")
            return audio_data

    except subprocess.TimeoutExpired:
        raise Exception("Audio download timed out (exceeded 2 minutes)")
    except Exception as e:
        print(f"Audio download error: {e}")
        raise
