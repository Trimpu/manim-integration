"""
Streamlit Web Frontend for Math Video Generator
A modern web interface for creating math visualization videos.
"""

import streamlit as st
import os
import time
from pathlib import Path
import subprocess
from math_video_generator import MathVideoGenerator

# Page configuration
st.set_page_config(
    page_title="Math Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_setup():
    """Check if the application is properly set up."""
    try:
        # Check if .env file exists
        if not Path(".env").exists():
            return False, "❌ .env file not found. Please create it with your GITHUB_TOKEN."
        
        # Check if GitHub token is set
        from dotenv import load_dotenv
        load_dotenv()
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return False, "❌ GITHUB_TOKEN not found in .env file."
        
        # Try to initialize the generator
        MathVideoGenerator()
        return True, "✅ Setup complete! Ready to generate videos."
        
    except Exception as e:
        return False, f"❌ Setup error: {str(e)}"

def generate_video_with_progress(topic, difficulty, duration, quality):
    """Generate video with progress tracking."""
    try:
        # Initialize generator
        generator = MathVideoGenerator()
        
        # Create progress placeholders
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Generate code
        status_text.text("🤖 Generating Manim code with AI...")
        progress_bar.progress(20)
        
        manim_code = generator.generate_manim_code(topic, difficulty, duration)
        if not manim_code:
            return None, "Failed to generate Manim code"
        
        progress_bar.progress(40)
        status_text.text("💾 Saving generated code...")
        
        # Clean and save code
        manim_code = generator.clean_generated_code(manim_code)
        
        # Create filename
        import re
        safe_topic_name = re.sub(r'[^\w\s-]', '', topic).strip()
        safe_topic_name = re.sub(r'[-\s]+', '_', safe_topic_name)
        if len(safe_topic_name) > 50:
            safe_topic_name = safe_topic_name[:50]
        
        temp_file = Path("math_videos") / f"{safe_topic_name}_scene.py"
        temp_file.parent.mkdir(exist_ok=True)
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(manim_code)
        
        progress_bar.progress(60)
        status_text.text("🎬 Rendering video with Manim...")
        
        # Extract scene class name
        scene_match = re.search(r'class\s+(\w+)\s*\(Scene\)', manim_code)
        if not scene_match:
            return None, "No Scene class found in generated code"
        
        scene_name = scene_match.group(1)
        
        # Render video
        quality_map = {"low_quality": "l", "medium_quality": "m", "high_quality": "h"}
        
        cmd = [
            "D:/VSCODE/aitesting/.venv/Scripts/python.exe", "-m", "manim", "render",
            str(temp_file), scene_name,
            "--quality", quality_map.get(quality, "m"),
            "--output_file", f"{safe_topic_name}_video"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path.cwd()))
        
        progress_bar.progress(90)
        status_text.text("🔍 Locating generated video...")
        
        if result.returncode == 0:
            # Find the video file
            scene_file_stem = temp_file.stem
            quality_folder = {"l": "480p15", "m": "720p30", "h": "1080p60"}[quality_map.get(quality, "m")]
            media_dir = Path("media") / "videos" / scene_file_stem / quality_folder
            
            if media_dir.exists():
                video_files = list(media_dir.glob("*.mp4"))
                if video_files:
                    progress_bar.progress(100)
                    status_text.text("✅ Video generated successfully!")
                    return str(video_files[0]), manim_code
            
            return None, "Video file not found after rendering"
        else:
            return None, f"Manim rendering failed: {result.stderr}"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Math Video Generator</h1>', unsafe_allow_html=True)
    st.markdown("### Create Educational Math Videos with AI + Manim")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Setup check
        setup_ok, setup_message = check_setup()
        if setup_ok:
            st.markdown(f'<div class="success-box">{setup_message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">{setup_message}</div>', unsafe_allow_html=True)
            st.markdown("""
            **Setup Instructions:**
            1. Create `.env` file in project directory
            2. Add: `GITHUB_TOKEN=your_token_here`
            3. Get token from: https://github.com/settings/tokens
            """)
            st.stop()
        
        st.markdown("---")
        
        # Video settings
        st.subheader("🎥 Video Settings")
        difficulty = st.selectbox(
            "Difficulty Level",
            ["beginner", "intermediate", "advanced"],
            index=1
        )
        
        duration = st.slider("Duration (seconds)", 15, 120, 45)
        
        quality = st.selectbox(
            "Video Quality",
            ["low_quality", "medium_quality", "high_quality"],
            index=1
        )
        
        st.markdown("---")
        
        # Examples
        st.subheader("💡 Example Topics")
        examples = [
            "Pythagorean theorem proof",
            "Quadratic function graphing",
            "Derivatives and tangent lines",
            "Integration as area under curve",
            "Trigonometric unit circle",
            "Matrix multiplication visualization"
        ]
        
        for example in examples:
            if st.button(f"📝 {example}", key=f"ex_{example}"):
                st.session_state.topic = example
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Enter Your Math Topic")
        
        # Text input for topic
        topic = st.text_area(
            "Describe the mathematical concept you want to visualize:",
            value=st.session_state.get('topic', ''),
            height=120,
            placeholder="Example: Explain calculus derivatives with visual examples showing tangent lines and rates of change",
            help="Be specific about what you want to visualize. Include any particular aspects or examples you want covered."
        )
        
        # Generate button
        generate_btn = st.button("🚀 Generate Video", type="primary", use_container_width=True)
        
        if generate_btn and topic.strip():
            with st.container():
                st.markdown("---")
                st.subheader("🎬 Generation Progress")
                
                video_path, result = generate_video_with_progress(topic, difficulty, duration, quality)
                
                if video_path:
                    st.markdown(f'<div class="success-box">✅ <strong>Video Generated Successfully!</strong><br>📁 Location: {video_path}</div>', unsafe_allow_html=True)
                    
                    # Video preview (if possible)
                    if Path(video_path).exists():
                        try:
                            st.video(video_path)
                        except:
                            st.info("Video file created but preview not available. Check the file location above.")
                    
                    # Download button
                    if Path(video_path).exists():
                        with open(video_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Video",
                                data=file.read(),
                                file_name=Path(video_path).name,
                                mime="video/mp4"
                            )
                    
                    # Show generated code
                    with st.expander("🔍 View Generated Manim Code"):
                        st.code(result, language="python")
                
                else:
                    st.markdown(f'<div class="error-box">❌ <strong>Generation Failed</strong><br>{result}</div>', unsafe_allow_html=True)
        
        elif generate_btn and not topic.strip():
            st.warning("⚠️ Please enter a math topic to visualize.")
    
    with col2:
        st.subheader("📊 Recent Videos")
        
        # List recent videos
        media_path = Path("media/videos")
        if media_path.exists():
            video_folders = [d for d in media_path.iterdir() if d.is_dir()]
            
            if video_folders:
                for folder in sorted(video_folders, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    # Find video files in the folder
                    for quality_folder in folder.iterdir():
                        if quality_folder.is_dir():
                            videos = list(quality_folder.glob("*.mp4"))
                            if videos:
                                video = videos[0]
                                # Clean up the folder name for display
                                display_name = folder.name.replace("_", " ").title()
                                if len(display_name) > 30:
                                    display_name = display_name[:30] + "..."
                                
                                st.write(f"🎬 {display_name}")
                                if st.button(f"📁 Open", key=f"open_{folder.name}"):
                                    import subprocess
                                    subprocess.run(['explorer', str(quality_folder)], check=False)
                                st.markdown("---")
                                break
            else:
                st.info("No videos generated yet.")
        else:
            st.info("No videos generated yet.")

if __name__ == "__main__":
    main()
