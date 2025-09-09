"""
Frontend Launcher for Math Video Generator
Choose your preferred frontend interface.
"""

import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def check_setup():
    """Check if the application is set up correctly."""
    try:
        from math_video_generator import MathVideoGenerator
        generator = MathVideoGenerator()
        return True, "✅ Setup complete!"
    except Exception as e:
        return False, f"❌ Setup error: {e}"

def launch_streamlit():
    """Launch the Streamlit web interface."""
    print("🚀 Starting Streamlit Web Interface...")
    print("📱 Interface will open at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            "D:/VSCODE/aitesting/.venv/Scripts/streamlit.exe",
            "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], cwd=Path.cwd())
    except KeyboardInterrupt:
        print("\n👋 Streamlit server stopped.")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

def launch_flask():
    """Launch the Flask web interface."""
    print("🚀 Starting Flask Web Interface...")
    print("📱 Interface will open at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    # Open browser after a short delay
    import threading
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        subprocess.run([
            "D:/VSCODE/aitesting/.venv/Scripts/python.exe",
            "flask_app.py"
        ], cwd=Path.cwd())
    except KeyboardInterrupt:
        print("\n👋 Flask server stopped.")
    except Exception as e:
        print(f"❌ Error starting Flask: {e}")

def main():
    """Main launcher function."""
    print("🎬 Math Video Generator - Frontend Launcher")
    print("=" * 50)
    
    # Check setup
    setup_ok, setup_message = check_setup()
    print(setup_message)
    
    if not setup_ok:
        print("\n⚠️  Please set up your GitHub token in the .env file first.")
        print("📋 Instructions:")
        print("1. Create .env file with: GITHUB_TOKEN=your_token_here")
        print("2. Get token from: https://github.com/settings/tokens")
        return
    
    print("\n🌐 Choose your frontend interface:")
    print("1. 📱 Streamlit Dashboard (Recommended)")
    print("2. 🌐 Flask Web App")
    print("3. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                launch_streamlit()
                break
            elif choice == "2":
                launch_flask()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
