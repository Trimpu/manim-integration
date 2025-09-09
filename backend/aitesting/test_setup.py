"""
Test script to verify GitHub AI connection and generate a simple Manim example.
Run this first to ensure everything is configured correctly.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

def test_github_ai_connection():
    """Test the GitHub AI connection using the configuration from aitest.md."""
    
    print("Testing GitHub AI Connection...")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Configuration from aitest.md
    token = os.environ.get("GITHUB_TOKEN")
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4o"  # Using GPT-4o which is available
    
    if not token:
        print("❌ ERROR: GITHUB_TOKEN not found in environment variables")
        print("\nPlease:")
        print("1. Create a .env file in this directory")
        print("2. Add your GitHub token: GITHUB_TOKEN=your_token_here")
        print("3. Get a token from: https://github.com/settings/tokens")
        return False
    
    try:
        # Initialize OpenAI client with GitHub endpoint
        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )
        
        print(f"✅ Token found: {token[:8]}...")
        print(f"✅ Endpoint: {endpoint}")
        print(f"✅ Model: {model}")
        
        # Test basic chat completion
        print("\nTesting basic AI response...")
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "What is 2 + 2?",
                }
            ],
            model=model
        )
        
        result = response.choices[0].message.content
        print(f"✅ AI Response: {result}")
        
        # Test Manim code generation
        print("\nTesting Manim code generation...")
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Generate a simple Manim scene that shows the text 'Hello, Math!' 
                    Use proper Manim syntax. Return only Python code without markdown formatting.""",
                },
                {
                    "role": "user",
                    "content": "Create a basic Manim scene",
                }
            ],
            model=model
        )
        
        manim_code = response.choices[0].message.content.strip()
        print("✅ Generated Manim code:")
        print("-" * 30)
        print(manim_code[:200] + "..." if len(manim_code) > 200 else manim_code)
        print("-" * 30)
        
        # Save test code
        with open("test_scene.py", "w", encoding="utf-8") as f:
            f.write(manim_code)
        
        print("✅ Test code saved to: test_scene.py")
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Ensure FFmpeg is installed for video rendering")
        print("2. Run: D:/VSCODE/aitesting/.venv/Scripts/python.exe math_video_generator.py")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nPossible issues:")
        print("- Invalid GitHub token")
        print("- Network connectivity problems")
        print("- GitHub Models API unavailable")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking Dependencies...")
    print("=" * 30)
    
    try:
        import openai
        print(f"✅ OpenAI SDK: {openai.__version__}")
    except ImportError:
        print("❌ OpenAI SDK not installed")
        return False
    
    try:
        import manim
        print(f"✅ Manim: {manim.__version__}")
    except ImportError:
        print("❌ Manim not installed")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv: Available")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    return True

if __name__ == "__main__":
    print("Math Video Generator - Setup Test")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Missing dependencies. Please install them first.")
        exit(1)
    
    # Test GitHub AI connection
    if test_github_ai_connection():
        print("\n🚀 Setup complete! You're ready to generate math videos.")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
