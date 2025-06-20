#!/usr/bin/env python3
"""
Simple test script to verify Flask app can start without errors
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import generateScreenplay
        print("✓ generateScreenplay imported successfully")
    except ImportError as e:
        print(f"✗ generateScreenplay import failed: {e}")
        return False
    
    try:
        import processScreenplay
        print("✓ processScreenplay imported successfully")
    except ImportError as e:
        print(f"✗ processScreenplay import failed: {e}")
        return False
    
    try:
        import generateScenesImagesFlux
        print("✓ generateScenesImagesFlux imported successfully")
    except ImportError as e:
        print(f"✗ generateScenesImagesFlux import failed: {e}")
        return False
    
    try:
        import generateVideoFal
        print("✓ generateVideoFal imported successfully")
    except ImportError as e:
        print(f"✗ generateVideoFal import failed: {e}")
        return False
    
    try:
        import generateAudioElevenLabs
        print("✓ generateAudioElevenLabs imported successfully")
    except ImportError as e:
        print(f"✗ generateAudioElevenLabs import failed: {e}")
        return False
    
    try:
        import videoAudioOverlay
        print("✓ videoAudioOverlay imported successfully")
    except ImportError as e:
        print(f"✗ videoAudioOverlay import failed: {e}")
        return False
    
    try:
        import utils
        print("✓ utils imported successfully")
    except ImportError as e:
        print(f"✗ utils import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration file and environment variables"""
    try:
        from config import (
            TOGETHER_API_KEY, 
            OPENAI_API_KEY, 
            ELEVENLABS_API_KEY, 
            FAL_API_KEY, 
            FLASK_SECRET_KEY
        )
        print("✓ Configuration imported successfully")
        
        # Check if .env file exists
        if os.path.exists('.env'):
            print("✓ .env file found")
        else:
            print("⚠ Warning: .env file not found. Run 'python setup_env.py' to create it.")
        
        # Check if API keys are set (optional warning)
        if not any([TOGETHER_API_KEY, OPENAI_API_KEY, ELEVENLABS_API_KEY, FAL_API_KEY]):
            print("⚠ Warning: No API keys configured")
            print("   Run 'python setup_env.py' to create .env file")
            print("   Then edit .env file with your API keys")
        else:
            print("✓ API keys configured")
            
    except ImportError as e:
        print(f"✗ Configuration import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test that Flask app can be created"""
    try:
        from app import app
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def test_directories():
    """Test that required directories exist or can be created"""
    required_dirs = [
        "templates",
        "static", 
        "outputs",
        "outputs/screenplays",
        "outputs/images",
        "outputs/videos",
        "outputs/audios",
        "outputs/combined"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory exists: {directory}")
        else:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✓ Directory created: {directory}")
            except Exception as e:
                print(f"✗ Failed to create directory {directory}: {e}")
                return False
    
    return True

def main():
    """Run all tests"""
    print("Testing Flask application setup...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_config),
        ("App Creation Tests", test_app_creation),
        ("Directory Tests", test_directories)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✓ {test_name} passed")
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Flask app should work correctly.")
        print("\nTo run the app:")
        print("python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues before running the app.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 