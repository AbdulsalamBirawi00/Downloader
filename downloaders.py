"""
Video downloaders for Instagram, YouTube, and Facebook
Using only Python standard library
"""

import urllib.request
import urllib.parse
import re
import json
import ssl
import subprocess
import tempfile
import os


def create_request(url, headers=None):
    """Create HTTP request with headers"""
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    if headers:
        default_headers.update(headers)

    req = urllib.request.Request(url, headers=default_headers)
    return req


def download_file(url, headers=None):
    """Download file from URL"""
    try:
        req = create_request(url, headers)
        ssl_context = ssl.create_default_context()

        with urllib.request.urlopen(req, context=ssl_context, timeout=60) as response:
            # Handle gzip compression
            import gzip
            import io

            content = response.read()

            # Check if content is gzipped
            if response.headers.get('Content-Encoding') == 'gzip':
                content = gzip.decompress(content)

            return content

    except Exception as e:
        print(f"Error downloading file: {e}")
        return None


def download_instagram(url):
    """
    Download video from Instagram
    Works with reels and posts
    """
    try:
        # Clean URL
        url = url.split('?')[0]

        # Add embed to URL for easier parsing
        if '/reel/' in url or '/p/' in url or '/tv/' in url:
            # Try to get the shortcode
            parts = url.rstrip('/').split('/')
            shortcode = parts[-1]

            # Method 1: Try to fetch page and extract video URL
            html = download_file(url)

            if not html:
                raise Exception("Failed to fetch Instagram page")

            html_str = html.decode('utf-8', errors='ignore')

            # Look for video URL in various places
            video_url = None

            # Pattern 1: Look for video_url in JSON data
            patterns = [
                r'"video_url":"([^"]+)"',
                r'"playback_url":"([^"]+)"',
                r'{"src":"([^"]+)","type":"video/mp4"}',
                r'contentUrl":"([^"]+\.mp4[^"]*)"',
            ]

            for pattern in patterns:
                match = re.search(pattern, html_str)
                if match:
                    video_url = match.group(1)
                    # Decode unicode escapes
                    video_url = video_url.encode().decode('unicode_escape')
                    # Fix escaped slashes
                    video_url = video_url.replace('\\/', '/')
                    break

            if not video_url:
                # Try to find in og:video tag
                og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html_str)
                if og_video:
                    video_url = og_video.group(1)

            if video_url:
                print(f"Found Instagram video URL: {video_url[:100]}...")

                # Download the video
                video_data = download_file(video_url)

                if video_data:
                    return video_data
                else:
                    raise Exception("Failed to download Instagram video")
            else:
                raise Exception("Could not find video URL in Instagram page. The post might be private or not contain a video.")

    except Exception as e:
        print(f"Instagram download error: {e}")
        raise Exception(f"Instagram download failed: {str(e)}")


def download_youtube(url):
    """
    Download video from YouTube
    Basic implementation - may not work for all videos
    """
    try:
        # Extract video ID
        video_id = None

        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
        elif 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[-1].split('&')[0]
        elif 'youtube.com/shorts/' in url:
            video_id = url.split('shorts/')[-1].split('?')[0]

        if not video_id:
            raise Exception("Could not extract YouTube video ID")

        print(f"YouTube video ID: {video_id}")

        # Fetch video page
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        html = download_file(watch_url)

        if not html:
            raise Exception("Failed to fetch YouTube page")

        html_str = html.decode('utf-8', errors='ignore')

        # Try to find player response JSON
        patterns = [
            r'var ytInitialPlayerResponse = ({.+?});',
            r'ytInitialPlayerResponse\s*=\s*({.+?});',
        ]

        player_response = None
        for pattern in patterns:
            match = re.search(pattern, html_str)
            if match:
                try:
                    player_response = json.loads(match.group(1))
                    break
                except:
                    continue

        if not player_response:
            raise Exception("Could not find YouTube player response. Video might be age-restricted or private.")

        # Extract streaming data
        streaming_data = player_response.get('streamingData', {})

        # Get formats (video+audio) or adaptiveFormats (separate video/audio)
        formats = streaming_data.get('formats', [])

        if not formats:
            # Try adaptive formats (these usually have better quality but separate audio/video)
            formats = streaming_data.get('adaptiveFormats', [])

        if not formats:
            raise Exception("No video formats found")

        # Find best video format with both video and audio
        best_format = None
        for fmt in formats:
            # Prefer formats that have both video and audio
            if fmt.get('url') and fmt.get('mimeType', '').startswith('video/'):
                # Check if it has audio
                if 'audio' in fmt.get('mimeType', '') or not fmt.get('audioChannels') is None or 'acodec' not in fmt:
                    best_format = fmt
                    break

        # If no combined format, just get first video format
        if not best_format:
            for fmt in formats:
                if fmt.get('url') and 'video' in fmt.get('mimeType', ''):
                    best_format = fmt
                    break

        if not best_format or not best_format.get('url'):
            raise Exception("No downloadable video format found")

        video_url = best_format['url']
        print(f"Found YouTube video URL: {video_url[:100]}...")

        # Download the video
        video_data = download_file(video_url)

        if video_data:
            return video_data
        else:
            raise Exception("Failed to download YouTube video")

    except Exception as e:
        print(f"YouTube download error: {e}")
        raise Exception(f"YouTube download failed: {str(e)}")


def download_facebook(url):
    """
    Download video from Facebook
    Basic implementation
    """
    try:
        # Handle fb.watch URLs
        if 'fb.watch' in url:
            # Fetch the redirect
            html = download_file(url)
            if html:
                html_str = html.decode('utf-8', errors='ignore')
                # Try to find redirect URL
                redirect_match = re.search(r'<meta property="og:url" content="([^"]+)"', html_str)
                if redirect_match:
                    url = redirect_match.group(1)

        # Fetch Facebook page
        html = download_file(url)

        if not html:
            raise Exception("Failed to fetch Facebook page")

        html_str = html.decode('utf-8', errors='ignore')

        # Look for video URLs in various formats
        video_url = None

        # Pattern 1: HD video URL
        patterns = [
            r'"playable_url":"([^"]+)"',
            r'"playable_url_quality_hd":"([^"]+)"',
            r'"browser_native_hd_url":"([^"]+)"',
            r'"browser_native_sd_url":"([^"]+)"',
            r'"playable_url_hd":"([^"]+)"',
            r'hd_src:"([^"]+)"',
            r'sd_src:"([^"]+)"',
            r'"videoUrl":"([^"]+)"',
        ]

        for pattern in patterns:
            match = re.search(pattern, html_str)
            if match:
                video_url = match.group(1)
                # Decode unicode escapes
                video_url = video_url.encode().decode('unicode_escape')
                # Fix escaped slashes
                video_url = video_url.replace('\\/', '/')
                # Unescape HTML entities
                video_url = video_url.replace('&amp;', '&')
                break

        if not video_url:
            # Try og:video
            og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html_str)
            if og_video:
                video_url = og_video.group(1)
                video_url = video_url.replace('&amp;', '&')

        if video_url:
            print(f"Found Facebook video URL: {video_url[:100]}...")

            # Download the video
            video_data = download_file(video_url)

            if video_data:
                return video_data
            else:
                raise Exception("Failed to download Facebook video")
        else:
            raise Exception("Could not find video URL in Facebook page. The video might be private or require login.")

    except Exception as e:
        print(f"Facebook download error: {e}")
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
            # -i: input file
            # -vn: no video
            # -acodec libmp3lame: use MP3 codec
            # -q:a 2: quality (2 is high quality)
            # -y: overwrite output file
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
