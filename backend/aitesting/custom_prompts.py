"""
Custom Prompt Input - Math Video Generator
This script shows exactly where to input your custom math topics.
"""

from math_video_generator import MathVideoGenerator

def generate_custom_video():
    """Generate a video with your custom prompt."""
    
    # Initialize generator
    try:
        generator = MathVideoGenerator()
    except ValueError as e:
        print(f"Setup Error: {e}")
        print("Please set up your GitHub token in the .env file first.")
        return
    
    # ============================================
    # 🎯 INPUT YOUR CUSTOM PROMPTS HERE
    # ============================================
    
    # Example custom prompts you can modify:
    custom_topics = [
        "Explain the concept of derivatives using real-world examples",
        "Visualize how compound interest grows over time",
        "Show the relationship between sine and cosine waves",
        "Demonstrate the proof of the quadratic formula step by step",
        "Explain logarithms using exponential growth examples",
        "Visualize the concept of limits in calculus",
        "Show how matrix multiplication works geometrically"
    ]
    
    print("Custom Math Video Generator")
    print("=" * 40)
    print("\nPredefined custom prompts:")
    for i, topic in enumerate(custom_topics, 1):
        print(f"{i}. {topic}")
    
    print(f"{len(custom_topics) + 1}. Enter your own custom prompt")
    
    try:
        choice = int(input(f"\nChoose a prompt (1-{len(custom_topics) + 1}): "))
        
        if 1 <= choice <= len(custom_topics):
            # Use predefined prompt
            selected_topic = custom_topics[choice - 1]
            print(f"\nSelected: {selected_topic}")
            
        elif choice == len(custom_topics) + 1:
            # ============================================
            # 🎯 MAIN INPUT POINT FOR YOUR CUSTOM PROMPT
            # ============================================
            selected_topic = input("\n🎯 Enter your custom math topic/prompt: ").strip()
            
        else:
            print("Invalid choice")
            return
        
        if not selected_topic:
            print("No topic provided")
            return
        
        # Get difficulty level
        difficulty = input("Enter difficulty (beginner/intermediate/advanced) [intermediate]: ").strip() or "intermediate"
        
        # Get video duration
        try:
            duration = int(input("Enter target duration in seconds [30]: ").strip() or "30")
        except ValueError:
            duration = 30
        
        # Get quality
        quality = input("Enter quality (low_quality/medium_quality/high_quality) [medium_quality]: ").strip() or "medium_quality"
        
        print(f"\n🎬 Generating video for: {selected_topic}")
        print(f"📊 Difficulty: {difficulty}")
        print(f"⏱️ Duration: {duration} seconds")
        print(f"🎥 Quality: {quality}")
        print("\nThis may take a few minutes...")
        
        # Generate the video
        video_path = generator.create_video(
            math_topic=selected_topic,
            difficulty=difficulty,
            duration=duration,
            quality=quality
        )
        
        if video_path:
            print(f"\n🎉 SUCCESS! Video created at: {video_path}")
            print("\nYou can now:")
            print("1. Watch the video file")
            print("2. Check the generated Manim code in the math_videos/ folder")
        else:
            print("\n❌ Video generation failed. Check the error messages above.")
    
    except ValueError:
        print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")

def quick_custom_prompt():
    """Quick function to generate video from a single prompt."""
    
    # ============================================
    # 🎯 DIRECT PROMPT INPUT - MODIFY THIS
    # ============================================
    
    # Change this to your desired math topic:
    YOUR_CUSTOM_PROMPT = "Explain the Fibonacci sequence and golden ratio connection"
    
    try:
        generator = MathVideoGenerator()
        
        print(f"Generating video for: {YOUR_CUSTOM_PROMPT}")
        
        video_path = generator.create_video(
            math_topic=YOUR_CUSTOM_PROMPT,
            difficulty="intermediate",
            duration=45,
            quality="medium_quality"
        )
        
        if video_path:
            print(f"✅ Video created: {video_path}")
        else:
            print("❌ Video generation failed")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Choose your input method:")
    print("1. Interactive prompt selection")
    print("2. Quick custom prompt (modify the code)")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        generate_custom_video()
    elif choice == "2":
        quick_custom_prompt()
    else:
        print("Invalid choice")
