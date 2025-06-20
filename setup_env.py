#!/usr/bin/env python3
"""
Setup script to help users create their .env file
"""

import os
import secrets
import string

def generate_secret_key():
    """Generate a random secret key for Flask"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def create_env_file():
    """Create a .env file with template values"""
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Generate a random secret key
    secret_key = generate_secret_key()
    
    env_content = f"""# API Keys Configuration
# Fill in your actual API keys below

# Together AI API key for text-to-screenplay generation
# Get your key from: https://together.ai/
TOGETHER_API_KEY=your-together-ai-key-here

# OpenAI API key for image generation
# Get your key from: https://platform.openai.com/
OPENAI_API_KEY=your-openai-key-here

# ElevenLabs API key for text-to-speech
# Get your key from: https://elevenlabs.io/
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Fal AI API key for image-to-video generation
# Get your key from: https://fal.ai/
FAL_API_KEY=your-fal-ai-key-here

# Flask secret key (auto-generated, change this in production)
FLASK_SECRET_KEY={secret_key}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("\n📝 Next steps:")
        print("1. Edit the .env file and replace the placeholder values with your actual API keys")
        print("2. Run: python test_flask.py")
        print("3. Run: python app.py")
        print("\n🔒 Security note: The .env file is automatically added to .gitignore")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def update_gitignore():
    """Add .env to .gitignore if it exists"""
    gitignore_path = '.gitignore'
    
    # Check if .gitignore exists
    if not os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'w') as f:
                f.write("# Environment variables\n.env\n")
            print("✅ Created .gitignore file")
        except Exception as e:
            print(f"⚠️  Could not create .gitignore: {e}")
        return
    
    # Check if .env is already in .gitignore
    try:
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        if '.env' not in content:
            with open(gitignore_path, 'a') as f:
                f.write("\n# Environment variables\n.env\n")
            print("✅ Added .env to .gitignore")
        else:
            print("✅ .env is already in .gitignore")
            
    except Exception as e:
        print(f"⚠️  Could not update .gitignore: {e}")

def main():
    """Main setup function"""
    print("🔧 Setting up environment variables for Tell Me Your Story Flask App")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Update .gitignore
    update_gitignore()
    
    print("\n🎉 Setup complete!")
    print("\n📚 For more information, see FLASK_README.md")

if __name__ == "__main__":
    main() 