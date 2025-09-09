"""
Direct Prompt Input - No Terminal Input Required
Just modify the MATH_PROMPT variable below and run the script.
"""

from math_video_generator import MathVideoGenerator

# 🎯 PASTE YOUR FULL PROMPT HERE:
MATH_PROMPT = """A right triangle, whose base and height are 15 cm. and 20 cm. respectively is
made to revolve about its hypotenuse. Find the volume and surface area of the double cone so
formed."""

# Configuration
DIFFICULTY = "intermediate"  # beginner, intermediate, advanced
DURATION = 60  # seconds
QUALITY = "medium_quality"  # low_quality, medium_quality, high_quality

def generate_video_from_prompt():
    """Generate video from the predefined prompt."""
    
    # Clean the prompt (remove extra whitespace and line breaks)
    clean_prompt = ' '.join(MATH_PROMPT.split())
    
    print("Direct Prompt Video Generator")
    print("=" * 40)
    print(f"📝 Prompt: {clean_prompt}")
    print(f"📊 Difficulty: {DIFFICULTY}")
    print(f"⏱️ Duration: {DURATION} seconds")
    print(f"🎥 Quality: {QUALITY}")
    print(f"📏 Character count: {len(clean_prompt)}")
    
    try:
        generator = MathVideoGenerator()
        
        print(f"\n🎬 Generating video...")
        print("This may take a few minutes...")
        
        video_path = generator.create_video(
            math_topic=clean_prompt,
            difficulty=DIFFICULTY,
            duration=DURATION,
            quality=QUALITY
        )
        
        if video_path:
            print(f"\n🎉 SUCCESS! Video created at:")
            print(f"📁 {video_path}")
            
            # Try to open the folder
            import subprocess
            import os
            try:
                folder_path = os.path.dirname(video_path)
                subprocess.run(['explorer', folder_path], check=True)
                print(f"\n📂 Opened folder: {folder_path}")
            except:
                print("\n💡 Manually navigate to the video file location above.")
        else:
            print("\n❌ Video generation failed.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    generate_video_from_prompt()
