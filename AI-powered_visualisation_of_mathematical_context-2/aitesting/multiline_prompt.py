"""
Multi-line Prompt Handler for Math Video Generator
This script handles long, multi-line prompts properly.
"""

from math_video_generator import MathVideoGenerator

def get_multiline_input(prompt):
    """Get input that can span multiple lines."""
    print(prompt)
    print("(Press Enter twice when finished, or type 'END' on a new line)")
    print("-" * 50)
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END' or (line.strip() == '' and lines):
            break
        lines.append(line)
    
    return ' '.join(lines).strip()

def main():
    """Main function with better input handling."""
    try:
        generator = MathVideoGenerator()
        
        print("Math Video Generator - Multi-line Prompt Handler")
        print("=" * 55)
        
        # Get the full prompt with proper handling
        print("\n🎯 Enter your complete math problem/topic:")
        topic = get_multiline_input("Your math topic")
        
        if not topic:
            print("No topic provided.")
            return
        
        print(f"\n📝 Full topic received:")
        print(f"'{topic}'")
        print(f"Character count: {len(topic)}")
        
        # Confirm before proceeding
        confirm = input(f"\nProceed with this topic? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
        
        # Get other parameters
        difficulty = input("Enter difficulty (beginner/intermediate/advanced) [intermediate]: ").strip() or "intermediate"
        
        try:
            duration = int(input("Enter target duration in seconds [45]: ").strip() or "45")
        except ValueError:
            duration = 45
        
        quality = input("Enter quality (low_quality/medium_quality/high_quality) [medium_quality]: ").strip() or "medium_quality"
        
        print(f"\n🎬 Generating video...")
        print(f"📊 Topic: {topic}")
        print(f"📊 Difficulty: {difficulty}")
        print(f"⏱️ Duration: {duration} seconds")
        print(f"🎥 Quality: {quality}")
        print("\nThis may take a few minutes...")
        
        # Generate the video
        video_path = generator.create_video(
            math_topic=topic,
            difficulty=difficulty,
            duration=duration,
            quality=quality
        )
        
        if video_path:
            print(f"\n🎉 SUCCESS! Video created at:")
            print(f"📁 {video_path}")
            
            # Open the folder
            import subprocess
            try:
                folder_path = str(video_path).replace(video_path.split('\\')[-1], '')
                subprocess.run(['explorer', folder_path], check=True)
                print(f"\n📂 Opened folder: {folder_path}")
            except:
                print("\n💡 Manually navigate to the video file location above.")
        else:
            print("\n❌ Video generation failed. Check the error messages above.")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please ensure your GitHub token is set up in the .env file.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
