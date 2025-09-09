import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleMathExplainer:
    def __init__(self):
        """Initialize the Simple Math Explainer with GitHub AI integration."""
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4o"
        
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
    
    def generate_explanation(self, math_topic, difficulty="intermediate"):
        """
        Generate a detailed mathematical explanation for a given topic.
        
        Args:
            math_topic (str): The mathematical concept to explain
            difficulty (str): Difficulty level (beginner, intermediate, advanced)
        
        Returns:
            dict: Contains explanation text, steps, and examples
        """
        difficulty_prompts = {
            "beginner": "Explain this in simple terms suitable for middle school students with lots of examples.",
            "intermediate": "Provide a clear explanation suitable for high school students with step-by-step solutions.",
            "advanced": "Give a detailed mathematical explanation suitable for college-level students with rigorous steps."
        }
        
        prompt = f"""You are an expert mathematics tutor. Please provide a comprehensive explanation for the following mathematical problem or concept:

{math_topic}

Requirements:
- {difficulty_prompts.get(difficulty, difficulty_prompts['intermediate'])}
- Break down the solution into clear, numbered steps
- Provide the final answer clearly
- Use simple language and avoid overly complex notation
- Include any relevant formulas or theorems
- If it's a word problem, identify what's given and what needs to be found

Format your response as a JSON object with these fields:
- "title": A concise title for the problem
- "given": What information is provided (for word problems)
- "find": What needs to be determined
- "formula": Any relevant formulas or theorems
- "steps": An array of step-by-step solution steps
- "answer": The final answer
- "explanation": A brief summary explaining the approach
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful mathematics tutor. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            explanation_text = response.choices[0].message.content.strip()
            
            # Try to parse as JSON, fallback to plain text if it fails
            try:
                explanation_data = json.loads(explanation_text)
                return explanation_data
            except json.JSONDecodeError:
                # Fallback to simple structure
                return {
                    "title": "Mathematical Solution",
                    "given": "Problem provided by user",
                    "find": "Solution to the mathematical problem",
                    "formula": "Various mathematical principles apply",
                    "steps": explanation_text.split('\n'),
                    "answer": "See detailed explanation above",
                    "explanation": explanation_text
                }
                
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return {
                "title": "Error",
                "given": "Mathematical problem",
                "find": "Solution",
                "formula": "N/A",
                "steps": [f"Sorry, I encountered an error while generating the explanation: {str(e)}"],
                "answer": "Unable to generate solution",
                "explanation": "Please try again or check your mathematical problem formatting."
            }
