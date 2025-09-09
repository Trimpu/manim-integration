"""
PDF Math Video Generator - Advanced Frontend
Interactive PDF viewer with text selection and instant video generation
"""

import streamlit as st
import pdfplumber
import PyPDF2
import tempfile
import os
import base64
from pathlib import Path
import time
from math_video_generator import MathVideoGenerator

# Page configuration
st.set_page_config(
    page_title="PDF Math Video Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .pdf-container {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    
    .selected-text {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .video-container {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
    
    .processing-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'pdf_text' not in st.session_state:
        st.session_state.pdf_text = ""
    if 'selected_text' not in st.session_state:
        st.session_state.selected_text = ""
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'pdf_pages' not in st.session_state:
        st.session_state.pdf_pages = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        # Extract text using pdfplumber (better for complex layouts)
        pages_text = []
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
                else:
                    pages_text.append("")
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return pages_text
    
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return []

def create_pdf_viewer(pdf_file):
    """Create a simple PDF viewer with text extraction."""
    try:
        # Display PDF in an iframe
        base64_pdf = base64.b64encode(pdf_file.getvalue()).decode('utf-8')
        pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" height="600px" type="application/pdf">
        </iframe>
        '''
        return pdf_display
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")
        return None

def display_video_player(video_path):
    """Display video player in Streamlit."""
    try:
        if os.path.exists(video_path):
            # Read video file
            with open(video_path, 'rb') as video_file:
                video_bytes = video_file.read()
            
            # Display video player
            st.video(video_bytes)
            return True
        else:
            st.error(f"Video file not found: {video_path}")
            return False
    except Exception as e:
        st.error(f"Error displaying video: {str(e)}")
        return False

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 PDF Math Video Generator</h1>', unsafe_allow_html=True)
    st.markdown("**Upload a math PDF, select text, and get instant video explanations!**")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Video settings
        st.subheader("Video Settings")
        difficulty = st.selectbox(
            "Difficulty Level",
            ["beginner", "intermediate", "advanced"],
            index=1
        )
        
        duration = st.slider(
            "Video Duration (seconds)",
            min_value=20,
            max_value=120,
            value=45,
            step=5
        )
        
        quality = st.selectbox(
            "Video Quality",
            ["low_quality", "medium_quality", "high_quality"],
            index=1
        )
        
        st.divider()
        
        # Generated videos history
        st.subheader("📹 Generated Videos")
        if st.session_state.generated_videos:
            for i, video_info in enumerate(st.session_state.generated_videos):
                with st.expander(f"Video {i+1}: {video_info['topic'][:30]}..."):
                    st.write(f"**Topic:** {video_info['topic']}")
                    st.write(f"**Status:** {video_info['status']}")
                    if video_info['status'] == 'completed' and os.path.exists(video_info['path']):
                        if st.button(f"Show Video {i+1}", key=f"show_video_{i}"):
                            st.session_state.current_video = video_info['path']
        else:
            st.info("No videos generated yet")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 PDF Viewer")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload a Math PDF",
            type=['pdf'],
            help="Upload a PDF containing mathematical content"
        )
        
        if uploaded_file is not None:
            # Display PDF
            st.subheader("PDF Content")
            pdf_display = create_pdf_viewer(uploaded_file)
            if pdf_display:
                st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Extract text from PDF
            if st.button("🔍 Extract Text from PDF", key="extract_text"):
                with st.spinner("Extracting text from PDF..."):
                    pages_text = extract_text_from_pdf(uploaded_file)
                    if pages_text:
                        st.session_state.pdf_pages = pages_text
                        st.session_state.pdf_text = "\n\n".join(pages_text)
                        st.success(f"✅ Extracted text from {len(pages_text)} pages!")
            
            # Page navigation if text is extracted
            if st.session_state.pdf_pages:
                st.subheader("📖 Page Navigation")
                page_num = st.selectbox(
                    "Select Page",
                    range(len(st.session_state.pdf_pages)),
                    format_func=lambda x: f"Page {x+1}"
                )
                st.session_state.current_page = page_num
                
                # Display current page text
                st.subheader(f"Page {page_num + 1} Text")
                page_text = st.session_state.pdf_pages[page_num]
                
                # Text area for selection
                selected_text = st.text_area(
                    "Select and copy text from here:",
                    value=page_text,
                    height=300,
                    key=f"page_text_{page_num}",
                    help="Copy the math content you want to generate a video for"
                )
        
        else:
            st.markdown('''
            <div class="pdf-container">
                <h3>📁 Upload a PDF file to get started</h3>
                <p>Supported formats: PDF</p>
                <p>Upload math textbooks, research papers, or homework problems</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.header("🎬 Video Generator")
        
        # Manual text input option
        st.subheader("✏️ Enter Math Content")
        manual_text = st.text_area(
            "Or manually enter math content:",
            height=150,
            placeholder="Enter mathematical concepts, problems, or equations you want to visualize...",
            help="You can either extract text from PDF or manually enter content here"
        )
        
        # Combine selected/manual text
        final_text = manual_text if manual_text.strip() else (selected_text if 'selected_text' in locals() else "")
        
        if final_text.strip():
            st.markdown(f'''
            <div class="selected-text">
                <h4>📝 Selected Content:</h4>
                <p>{final_text[:200]}{"..." if len(final_text) > 200 else ""}</p>
                <small>Character count: {len(final_text)}</small>
            </div>
            ''', unsafe_allow_html=True)
            
            # Generate video button
            if st.button("🎥 Generate Video", type="primary", key="generate_video"):
                try:
                    # Initialize video generator
                    generator = MathVideoGenerator()
                    
                    # Add to processing queue
                    video_info = {
                        'topic': final_text[:50],
                        'full_text': final_text,
                        'status': 'processing',
                        'path': '',
                        'timestamp': time.time()
                    }
                    st.session_state.generated_videos.append(video_info)
                    
                    # Processing message
                    processing_placeholder = st.empty()
                    processing_placeholder.markdown('''
                    <div class="processing-message">
                        <h4>🔄 Processing...</h4>
                        <p>Generating AI-powered mathematical visualization...</p>
                        <p>This may take 2-5 minutes depending on complexity.</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Generate video
                    status_text.text("🤖 AI generating Manim code...")
                    progress_bar.progress(25)
                    
                    video_path = generator.create_video(
                        math_topic=final_text,
                        difficulty=difficulty,
                        duration=duration,
                        quality=quality
                    )
                    
                    progress_bar.progress(100)
                    processing_placeholder.empty()
                    
                    if video_path and os.path.exists(video_path):
                        # Update video info
                        st.session_state.generated_videos[-1]['status'] = 'completed'
                        st.session_state.generated_videos[-1]['path'] = video_path
                        
                        # Success message
                        st.markdown('''
                        <div class="success-message">
                            <h4>✅ Video Generated Successfully!</h4>
                            <p>Your mathematical visualization is ready!</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Display video
                        st.subheader("🎬 Generated Video")
                        display_video_player(video_path)
                        
                        # Download button
                        with open(video_path, 'rb') as video_file:
                            st.download_button(
                                label="📥 Download Video",
                                data=video_file.read(),
                                file_name=f"math_video_{int(time.time())}.mp4",
                                mime="video/mp4"
                            )
                    
                    else:
                        st.session_state.generated_videos[-1]['status'] = 'failed'
                        st.error("❌ Failed to generate video. Please try again.")
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                
                except Exception as e:
                    st.error(f"❌ Error generating video: {str(e)}")
                    if st.session_state.generated_videos:
                        st.session_state.generated_videos[-1]['status'] = 'failed'
        
        else:
            st.info("👆 Upload a PDF and extract text, or manually enter math content to generate videos")
        
        # Display current video if selected
        if hasattr(st.session_state, 'current_video'):
            st.subheader("🎥 Current Video")
            display_video_player(st.session_state.current_video)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🚀 Powered by GitHub AI Models + Manim | Built with Streamlit</p>
        <p>📚 Upload PDF → 🔍 Select Text → 🎬 Generate Video → 📹 Watch & Learn!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
