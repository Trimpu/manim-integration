"""
Quick Demo - Math Video Generator
This script demonstrates how to generate a math video with minimal setup.
"""

import os
from math_video_generator import MathVideoGenerator

def quick_demo():
    """Generate a quick demo video."""
    print("Math Video Generator - Quick Demo")
    print("=" * 40)
    
    try:
        # Initialize the generator
        generator = MathVideoGenerator()
        print("✅ Generator initialized successfully")
        
        # Generate a simple math video
        topic = "Linear Functions and Slope"
        print(f"\n🎬 Generating video for: {topic}")
        
        video_path = generator.create_video(
            math_topic=topic,
            difficulty="beginner",
            duration=20,
            quality="medium_quality"
        )
        
        if video_path:
            print(f"\n🎉 Success! Video created at: {video_path}")
            print("\nYou can now:")
            print("1. Open the video file to watch the animation")
            print("2. Check the generated Manim code in the math_videos/ folder")
            print("3. Run the full application for more options")
        else:
            print("\n❌ Video generation failed. Check the error messages above.")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file with GITHUB_TOKEN=your_token")
        print("2. Set up your GitHub token with access to GitHub Models")
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")

if __name__ == "__main__":
    quick_demo()
