import os
import json
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleMathVideoGenerator:
    def __init__(self):
        """Initialize the Math Video Generator with GitHub AI integration."""
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4o"
        
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # Create output directory
        self.output_dir = Path("math_videos")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_explanation(self, math_topic, difficulty="intermediate"):
        """
        Generate a detailed mathematical explanation using GitHub AI.
        
        Args:
            math_topic (str): The mathematical concept to explain
            difficulty (str): Difficulty level (beginner, intermediate, advanced)
        
        Returns:
            str: Generated explanation
        """
        system_prompt = f"""You are an expert mathematics tutor. 
        
        Provide a clear, step-by-step explanation for the given mathematical problem or concept.
        
        Guidelines:
        1. Start with understanding what's given and what needs to be found
        2. Break down the solution into clear, logical steps
        3. Show all calculations and reasoning
        4. Explain the mathematical concepts involved
        5. Provide the final answer clearly
        
        Difficulty level: {difficulty}
        Make the explanation appropriate for this level.
        """
        
        user_prompt = f"""Please provide a detailed mathematical explanation for:

{math_topic}

Include:
- Problem understanding
- Step-by-step solution
- Mathematical formulas used
- Final answer
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return None
    
    def create_video(self, math_topic, difficulty="intermediate", duration=30, quality="medium_quality"):
        """
        Create a mathematical explanation (simplified version without actual video).
        
        Args:
            math_topic (str): The mathematical concept to explain
            difficulty (str): Difficulty level
            duration (int): Target duration (not used in simplified version)
            quality (str): Video quality (not used in simplified version)
        
        Returns:
            str: Path to the generated explanation file
        """
        print(f"Generating mathematical explanation for: {math_topic}")
        
        # Generate explanation using AI
        explanation = self.generate_explanation(math_topic, difficulty)
        
        if not explanation:
            print("Failed to generate explanation")
            return None
        
        # Create a safe filename
        safe_topic_name = "".join(c for c in math_topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic_name = safe_topic_name.replace(' ', '_')[:50]
        
        # Create explanation file
        explanation_file = self.output_dir / f"{safe_topic_name}_explanation.json"
        
        try:
            # Save explanation as JSON with metadata
            explanation_data = {
                "topic": math_topic,
                "difficulty": difficulty,
                "explanation": explanation,
                "generated_at": time.time(),
                "type": "mathematical_explanation"
            }
            
            with open(explanation_file, 'w', encoding='utf-8') as f:
                json.dump(explanation_data, f, indent=2, ensure_ascii=False)
            
            print(f"Explanation saved to: {explanation_file}")
            return str(explanation_file)
            
        except Exception as e:
            print(f"Error saving explanation: {e}")
            return None

# For backwards compatibility
MathVideoGenerator = SimpleMathVideoGenerator
