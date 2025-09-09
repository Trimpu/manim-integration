import os
import re
import tempfile
import subprocess
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MathVideoGenerator:
    def __init__(self):
        """Initialize the Math Video Generator with GitHub AI integration."""
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4o"  # Using GPT-4o which is available in GitHub Models
        
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # Create output directory
        self.output_dir = Path("math_videos")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_manim_code(self, math_topic, difficulty="intermediate", duration=30):
        """
        Generate Manim code for a given math topic using GitHub AI.
        
        Args:
            math_topic (str): The mathematical concept to visualize
            difficulty (str): Difficulty level (beginner, intermediate, advanced)
            duration (int): Approximate duration of the video in seconds
        
        Returns:
            str: Generated Manim code
        """
        system_prompt = f"""You are an expert in mathematical visualization and Manim (Mathematical Animation Engine).
        
        Your task is to generate complete, executable Manim code that creates educational math videos.
        
        Guidelines:
        1. Create a class that inherits from Scene
        2. Use proper Manim imports and syntax
        3. Include clear mathematical explanations as text animations
        4. Use appropriate colors, scaling, and positioning
        5. Add smooth transitions and animations
        6. Target duration: approximately {duration} seconds
        7. Difficulty level: {difficulty}
        8. Make the visualization engaging and educational
        9. Include step-by-step explanations
        10. Use proper mathematical notation with MathTex when needed
        
        Return ONLY the Python code without any markdown formatting or explanations."""
        
        user_prompt = f"""Create a Manim animation that explains and visualizes: {math_topic}
        
        The animation should:
        - Start with an introduction to the concept
        - Show step-by-step mathematical derivations or examples
        - Use visual elements like graphs, equations, geometric shapes as appropriate
        - End with a summary or key takeaway
        - Be suitable for {difficulty} level students"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating Manim code: {e}")
            return None
    
    def clean_generated_code(self, code):
        """Clean and validate the generated Manim code."""
        # Remove markdown code blocks if present
        code = re.sub(r'```python\n|```\n|```', '', code)
        
        # Ensure proper imports
        if "from manim import *" not in code:
            code = "from manim import *\n\n" + code
        
        return code
    
    def create_video(self, math_topic, difficulty="intermediate", duration=30, quality="medium_quality"):
        """
        Create a math visualization video for the given topic.
        
        Args:
            math_topic (str): The mathematical concept to visualize
            difficulty (str): Difficulty level
            duration (int): Target duration in seconds
            quality (str): Video quality (low_quality, medium_quality, high_quality)
        
        Returns:
            str: Path to the generated video file
        """
        print(f"Generating Manim code for: {math_topic}")
        
        # Generate Manim code using AI
        manim_code = self.generate_manim_code(math_topic, difficulty, duration)
        
        if not manim_code:
            print("Failed to generate Manim code")
            return None
        
        # Clean the generated code
        manim_code = self.clean_generated_code(manim_code)
        
        # Create a temporary Python file with shortened name
        safe_topic_name = re.sub(r'[^\w\s-]', '', math_topic).strip()
        safe_topic_name = re.sub(r'[-\s]+', '_', safe_topic_name)
        
        # Limit the filename length to avoid Windows path limits
        if len(safe_topic_name) > 50:
            safe_topic_name = safe_topic_name[:50]
        
        temp_file = self.output_dir / f"{safe_topic_name}_scene.py"
        
        try:
            # Write the generated code to file
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(manim_code)
            
            print(f"Manim code saved to: {temp_file}")
            print("Generated code preview:")
            print("-" * 50)
            print(manim_code[:500] + "..." if len(manim_code) > 500 else manim_code)
            print("-" * 50)
            
            # Extract scene class name from the code
            scene_match = re.search(r'class\s+(\w+)\s*\(Scene\)', manim_code)
            if not scene_match:
                print("No Scene class found in generated code")
                return None
            
            scene_name = scene_match.group(1)
            
            # Run Manim to generate the video
            print(f"Rendering video with Manim...")
            
            # Map quality settings to Manim quality flags
            quality_map = {
                "low_quality": "l",
                "medium_quality": "m", 
                "high_quality": "h"
            }
            
            cmd = [
                "D:/VSCODE/aitesting/.venv/Scripts/python.exe", "-m", "manim", "render",
                str(temp_file), scene_name,
                "--quality", quality_map.get(quality, "m"),
                "--output_file", f"{safe_topic_name}_video"
            ]
            
            # Run from the project root directory, not the output directory
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path.cwd()))
            
            if result.returncode == 0:
                print("Video generated successfully!")
                
                # Find the generated video file
                # Manim creates videos in media/videos/[scene_file_name]/[quality]/
                scene_file_stem = temp_file.stem
                quality_folder = {"l": "480p15", "m": "720p30", "h": "1080p60"}[quality_map.get(quality, "m")]
                media_dir = Path("media") / "videos" / scene_file_stem / quality_folder
                
                if media_dir.exists():
                    video_files = list(media_dir.glob("*.mp4"))
                    if video_files:
                        video_path = video_files[0]
                        print(f"Video saved to: {video_path}")
                        return str(video_path)
                
                # Alternative: look in the main output directory
                video_files = list(self.output_dir.glob("*.mp4"))
                if video_files:
                    video_path = video_files[-1]  # Get the most recent
                    print(f"Video saved to: {video_path}")
                    return str(video_path)
                
                print("Video file not found in expected location")
                return None
            else:
                print(f"Manim rendering failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return None
        
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
    
    def create_multiple_videos(self, topics_list, difficulty="intermediate"):
        """Create multiple videos from a list of topics."""
        results = []
        
        for topic in topics_list:
            print(f"\n{'='*60}")
            print(f"Processing: {topic}")
            print(f"{'='*60}")
            
            video_path = self.create_video(topic, difficulty)
            results.append({
                'topic': topic,
                'video_path': video_path,
                'success': video_path is not None
            })
        
        return results

def main():
    """Main function to demonstrate the Math Video Generator."""
    try:
        # Initialize the generator
        generator = MathVideoGenerator()
        
        # Example topics
        topics = [
            "Pythagorean Theorem",
            "Quadratic Functions and Parabolas",
            "Derivatives and Rates of Change",
            "The Unit Circle and Trigonometry"
        ]
        
        print("Math Video Generator with GitHub AI and Manim")
        print("=" * 50)
        
        # Interactive mode
        while True:
            print("\nOptions:")
            print("1. Generate single video")
            print("2. Generate multiple videos from predefined topics")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                topic = input("Enter math topic to visualize: ").strip()
                if topic:
                    difficulty = input("Enter difficulty (beginner/intermediate/advanced) [intermediate]: ").strip() or "intermediate"
                    video_path = generator.create_video(topic, difficulty)
                    if video_path:
                        print(f"\n✅ Video created successfully: {video_path}")
                    else:
                        print("\n❌ Failed to create video")
            
            elif choice == "2":
                difficulty = input("Enter difficulty for all videos (beginner/intermediate/advanced) [intermediate]: ").strip() or "intermediate"
                results = generator.create_multiple_videos(topics, difficulty)
                
                print(f"\n{'='*60}")
                print("SUMMARY")
                print(f"{'='*60}")
                
                for result in results:
                    status = "✅ Success" if result['success'] else "❌ Failed"
                    print(f"{status}: {result['topic']}")
                    if result['video_path']:
                        print(f"   Path: {result['video_path']}")
            
            elif choice == "3":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease ensure you have set the GITHUB_TOKEN environment variable.")
        print("You can create a .env file with: GITHUB_TOKEN=your_token_here")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
