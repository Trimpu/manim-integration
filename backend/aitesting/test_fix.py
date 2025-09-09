"""
Quick test of the fixed math video generator
"""

from math_video_generator import MathVideoGenerator

def test_fixed_generator():
    try:
        generator = MathVideoGenerator()
        
        # Test with a simple topic
        video_path = generator.create_video(
            math_topic="Simple linear equations y = mx + b",
            difficulty="beginner",
            duration=20,
            quality="medium_quality"
        )
        
        if video_path:
            print(f"✅ SUCCESS! Video created at: {video_path}")
        else:
            print("❌ Failed to create video")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fixed_generator()
