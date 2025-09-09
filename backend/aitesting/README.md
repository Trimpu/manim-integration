# 🎬 AI-Powered Mathematical Visualization Generator

Transform mathematical concepts into engaging animated videos using AI-generated Manim code!

## 🌟 Overview

This project combines **GitHub AI Models**, **Manim (Mathematical Animation Engine)**, and **Streamlit** to create an intelligent system that converts mathematical text into beautiful, educational video animations.

### ✨ Key Features

- 🤖 **AI-Powered Code Generation**: Uses GitHub AI Models (GPT-4o) to generate Manim animation code
- 📊 **Mathematical Visualization**: Creates stunning animations for algebra, calculus, geometry, and more
- � **PDF Integration**: Upload PDFs and select text directly for video generation
- � **Multiple Quality Options**: Low, medium, and high-quality video rendering
- 🎯 **Difficulty Levels**: Beginner, intermediate, and advanced explanations
- 🌐 **Web Interface**: Easy-to-use Streamlit frontend with multiple app modes
- 📱 **Interactive PDF Viewer**: Direct text selection with floating action popups

## 🚀 Demo Applications

### 1. **Integrated PDF App** (`integrated_pdf_app.py`)
- Upload mathematical PDFs
- View pages as high-quality images
- Select text from sidebar editor
- Generate videos with live progress tracking
- Download and organize in video gallery

### 2. **Direct Selection App** (`direct_selection_app.py`)
- Interactive PDF viewer with text overlay
- Direct text selection from PDF pages
- Floating action popup for instant video generation
- Seamless inline workflow

### 3. **Basic Video Generator** (`streamlit_app.py`)
- Simple text input interface
- Quick video generation from mathematical topics
- Perfect for testing and basic use cases

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- FFmpeg (for video rendering)
- GitHub Personal Access Token with AI Models access

### 1. Clone the Repository
```bash
git clone https://github.com/Trimpu/AI-powered_visualisation_of_mathematical_context-2.git
cd AI-powered_visualisation_of_mathematical_context-2
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
1. Copy `.env.template` to `.env`
2. Add your GitHub Personal Access Token:
```env
GITHUB_TOKEN=your_github_personal_access_token_here
```

### 5. Install FFmpeg
- **Windows**: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 🎯 Quick Start

### Option 1: Integrated PDF Experience
```bash
streamlit run integrated_pdf_app.py
```

### Option 2: Direct Selection Interface
```bash
streamlit run direct_selection_app.py
```

### Option 3: Basic Text Input
```bash
streamlit run streamlit_app.py
```

## Example Topics

The application can generate videos for various mathematical concepts:

- **Algebra**: Quadratic Functions, Linear Equations, Polynomial Operations
- **Geometry**: Pythagorean Theorem, Circle Properties, Triangle Theorems
- **Calculus**: Derivatives, Integrals, Limits, Chain Rule
- **Trigonometry**: Unit Circle, Sine/Cosine Waves, Trigonometric Identities
- **Statistics**: Normal Distribution, Central Limit Theorem, Probability
- **Linear Algebra**: Matrix Operations, Eigenvalues, Vector Spaces

## Generated Output

Videos are saved in the `math_videos/` directory with the following structure:
```
math_videos/
├── media/
│   └── videos/
│       └── [topic_name]/
│           └── medium_quality/
│               └── [video_file].mp4
└── [topic_name]_scene.py
```

## Quality Settings

Available quality options:
- `low_quality` - 480p, faster rendering
- `medium_quality` - 720p, balanced (default)
- `high_quality` - 1080p, slower rendering

## Configuration

The application uses GitHub AI with the following settings:
- **Endpoint**: `https://models.github.ai/inference`
- **Model**: `openai/gpt-4o`
- **Temperature**: 0.7 (for creative but focused code generation)

## Troubleshooting

### Common Issues

1. **"GITHUB_TOKEN not found"**
   - Ensure you've created a `.env` file with your GitHub token
   - Verify the token has access to GitHub Models

2. **FFmpeg not found**
   - Install FFmpeg and ensure it's in your system PATH
   - Restart your terminal after installation

3. **Manim rendering fails**
   - Check the generated Python code for syntax errors
   - Ensure all Manim imports are correct
   - Try with `low_quality` setting first

4. **AI generates invalid code**
   - The application attempts to clean generated code automatically
   - Check the saved `.py` file in `math_videos/` for manual debugging

### Getting Help

If you encounter issues:
1. Check the generated Manim code in the `math_videos/` directory
2. Test with the simple example first
3. Verify your GitHub token permissions
4. Ensure FFmpeg is properly installed

## Technical Details

### Architecture

1. **AI Integration**: Uses OpenAI SDK to communicate with GitHub AI models
2. **Code Generation**: Sends structured prompts to generate educational Manim code
3. **Code Cleaning**: Automatically formats and validates generated code
4. **Video Rendering**: Uses Manim CLI to render animations to MP4 files

### Prompt Engineering

The application uses carefully crafted prompts that:
- Specify exact Manim syntax requirements
- Request educational step-by-step explanations
- Include difficulty level considerations
- Ensure proper mathematical notation usage

## Examples of Generated Content

The AI can generate code for visualizations like:
- Animated equation solving
- Geometric proofs with moving shapes
- Function graphing with transformations
- 3D mathematical objects and rotations
- Step-by-step mathematical derivations

## Future Enhancements

Potential improvements:
- Custom animation styles and themes
- Interactive parameter adjustment
- Voice narration integration
- Export to different formats
- Batch processing with configuration files
- Integration with educational platforms
