#!/usr/bin/env python3
"""
Test script to verify bot setup before deployment
"""

import sys
import os
import urllib.request
import json


def test_python_version():
    """Check Python version"""
    print("Testing Python version...")
    version = sys.version_info

    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.7 or higher")
        return False


def test_bot_token():
    """Check if bot token is set and valid"""
    print("\nTesting bot token...")

    token = os.environ.get('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        print("\nSet it with:")
        print("  export TELEGRAM_BOT_TOKEN='your_token_here'")
        return False

    # Test if token is valid by calling getMe
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            if data.get('ok'):
                bot_info = data.get('result', {})
                bot_name = bot_info.get('first_name', 'Unknown')
                bot_username = bot_info.get('username', 'Unknown')
                print(f"✅ Bot token is valid")
                print(f"   Bot name: {bot_name}")
                print(f"   Bot username: @{bot_username}")
                return True
            else:
                print("❌ Invalid bot token")
                return False

    except Exception as e:
        print(f"❌ Error validating token: {e}")
        return False


def test_imports():
    """Check if all required modules can be imported"""
    print("\nTesting required modules...")

    required_modules = [
        'urllib.request',
        'urllib.parse',
        'json',
        'ssl',
        're',
        'os',
        'sys',
        'time'
    ]

    all_ok = True
    for module_name in required_modules:
        try:
            # Test import
            parts = module_name.split('.')
            if len(parts) == 2:
                exec(f"from {parts[0]} import {parts[1]}")
            else:
                exec(f"import {module_name}")
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name} - {e}")
            all_ok = False

    return all_ok


def test_files():
    """Check if all required files exist"""
    print("\nTesting required files...")

    required_files = [
        'bot.py',
        'downloaders.py',
    ]

    all_ok = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - NOT FOUND")
            all_ok = False

    return all_ok


def test_internet():
    """Check internet connectivity"""
    print("\nTesting internet connection...")

    try:
        req = urllib.request.Request('https://www.google.com')
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print("✅ Internet connection - OK")
                return True
            else:
                print("❌ Internet connection - Failed")
                return False
    except Exception as e:
        print(f"❌ Internet connection - {e}")
        return False


def test_ffmpeg():
    """Check if ffmpeg is installed (optional)"""
    print("\nTesting ffmpeg (optional - for audio extraction)...")

    try:
        import subprocess
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            # Get ffmpeg version
            output = result.stdout.decode('utf-8', errors='ignore')
            version_line = output.split('\n')[0]
            print(f"✅ ffmpeg installed - {version_line}")
            return True
        else:
            print("⚠️  ffmpeg not found - Audio extraction will not work")
            print("   Install: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)")
            return True  # Don't fail the test, it's optional
    except FileNotFoundError:
        print("⚠️  ffmpeg not found - Audio extraction will not work")
        print("   Bot will still work for video downloads")
        print("   Install: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)")
        return True  # Don't fail the test, it's optional
    except Exception as e:
        print(f"⚠️  Could not check ffmpeg - {e}")
        return True  # Don't fail the test, it's optional


def main():
    print("=" * 50)
    print("Telegram Video Downloader Bot - Setup Test")
    print("=" * 50)

    results = []

    results.append(("Python Version", test_python_version()))
    results.append(("Required Modules", test_imports()))
    results.append(("Required Files", test_files()))
    results.append(("Internet Connection", test_internet()))
    results.append(("Bot Token", test_bot_token()))
    results.append(("ffmpeg (Optional)", test_ffmpeg()))

    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 50)

    if all_passed:
        print("\n🎉 All tests passed! Your bot is ready to run.")
        print("\nRun the bot with:")
        print("  python3 bot.py")
        print("\nOr use the start script:")
        print("  ./start.sh (Linux/Mac)")
        print("  start.bat (Windows)")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
