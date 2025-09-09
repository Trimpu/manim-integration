"""
Simple example demonstrating AI-generated Manim code for math visualization.
This script shows a basic workflow without the full application complexity.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_simple_manim_example():
    """Generate a simple Manim example using GitHub AI."""
    
    # Setup GitHub AI client (from aitest.md)
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Please set GITHUB_TOKEN in your .env file")
        return
    
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4o"
    
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    
    # Generate Manim code for a simple math concept
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a Manim expert. Generate complete, executable Manim code.
                
                Requirements:
                - Create a class inheriting from Scene
                - Use proper Manim syntax
                - Include mathematical visualizations
                - Add text explanations
                - Make it educational and engaging
                
                Return ONLY Python code without markdown formatting.""",
            },
            {
                "role": "user",
                "content": "Create a Manim animation that visualizes the Pythagorean theorem with a right triangle, showing a² + b² = c²",
            }
        ],
        model=model
    )
    
    # Save the generated code
    manim_code = response.choices[0].message.content.strip()
    
    # Clean up any markdown formatting
    if "```python" in manim_code:
        manim_code = manim_code.split("```python")[1].split("```")[0].strip()
    elif "```" in manim_code:
        manim_code = manim_code.split("```")[1].strip()
    
    # Ensure proper imports
    if "from manim import *" not in manim_code:
        manim_code = "from manim import *\n\n" + manim_code
    
    # Save to file
    with open("pythagorean_example.py", "w", encoding="utf-8") as f:
        f.write(manim_code)
    
    print("Generated Manim code:")
    print("=" * 50)
    print(manim_code)
    print("=" * 50)
    print("\nCode saved to: pythagorean_example.py")
    print("\nTo render the video, run:")
    print("D:/VSCODE/aitesting/.venv/Scripts/python.exe -m manim pythagorean_example.py --medium_quality")

if __name__ == "__main__":
    generate_simple_manim_example()
