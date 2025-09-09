"""
Advanced PDF Math Video Generator with Interactive Text Selection
Enhanced version with better PDF viewing and text selection capabilities
"""

import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
import base64
from pathlib import Path
import time
import json
from math_video_generator import MathVideoGenerator

# Page configuration
st.set_page_config(
    page_title="Advanced PDF Math Video Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .pdf-viewer-container {
        border: 3px solid #e0e0e0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        background: white;
    }
    
    .text-selection-area {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .selected-text-display {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #2196f3;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(33,150,243,0.2);
    }
    
    .video-generation-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #ffb74d;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255,183,77,0.2);
    }
    
    .success-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        color: #2e7d32;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #66bb6a;
        box-shadow: 0 4px 12px rgba(102,187,106,0.2);
    }
    
    .processing-card {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        color: #f57c00;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #ffb74d;
        box-shadow: 0 4px 12px rgba(255,183,77,0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #ce93d8;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3f51b5;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'pdf_document' not in st.session_state:
        st.session_state.pdf_document = None
    if 'pdf_pages_text' not in st.session_state:
        st.session_state.pdf_pages_text = []
    if 'selected_text' not in st.session_state:
        st.session_state.selected_text = ""
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'pdf_metadata' not in st.session_state:
        st.session_state.pdf_metadata = {}

def extract_pdf_content(pdf_file):
    """Extract comprehensive content from PDF using PyMuPDF."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        # Open PDF with PyMuPDF
        doc = fitz.open(tmp_path)
        
        # Extract metadata
        metadata = {
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'subject': doc.metadata.get('subject', 'Unknown'),
            'page_count': doc.page_count,
            'file_size': len(pdf_file.getvalue())
        }
        
        # Extract text from all pages
        pages_content = []
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Extract text
            text = page.get_text()
            
            # Extract text blocks with coordinates (for better selection)
            blocks = page.get_text("blocks")
            
            # Get page dimensions
            rect = page.rect
            
            page_info = {
                'page_num': page_num + 1,
                'text': text,
                'blocks': blocks,
                'width': rect.width,
                'height': rect.height,
                'word_count': len(text.split()) if text else 0
            }
            pages_content.append(page_info)
        
        doc.close()
        os.unlink(tmp_path)
        
        return pages_content, metadata
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return [], {}

def create_enhanced_pdf_viewer(pdf_file):
    """Create enhanced PDF viewer with better controls."""
    try:
        # Convert PDF to base64 for display
        base64_pdf = base64.b64encode(pdf_file.getvalue()).decode('utf-8')
        
        # Enhanced PDF viewer with controls
        pdf_viewer_html = f'''
        <div class="pdf-viewer-container">
            <div style="background: #f8f9fa; padding: 10px; border-bottom: 1px solid #dee2e6;">
                <h5 style="margin: 0; color: #495057;">📄 PDF Viewer</h5>
                <small style="color: #6c757d;">Click and drag to select text, then copy to generate videos</small>
            </div>
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" height="700px" type="application/pdf"
                    style="border: none;">
                <p>Your browser does not support PDFs. Please download the PDF to view it.</p>
            </iframe>
        </div>
        '''
        return pdf_viewer_html
    
    except Exception as e:
        st.error(f"Error creating PDF viewer: {str(e)}")
        return None

def display_page_content(page_info, page_num):
    """Display individual page content with selection capabilities."""
    st.subheader(f"📄 Page {page_info['page_num']} Content")
    
    # Page statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <strong>{page_info['word_count']}</strong><br>
            <small>Words</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <strong>{len(page_info['text'].split("."))} </strong><br>
            <small>Sentences</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <strong>{len(page_info['text'])}</strong><br>
            <small>Characters</small>
        </div>
        ''', unsafe_allow_html=True)
    
    # Text content area
    st.markdown('''
    <div class="text-selection-area">
        <h5>📝 Page Text (Select and Copy)</h5>
        <p style="color: #6c757d; font-size: 0.9em;">
            Select mathematical content from the text below, then paste it in the video generator.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Editable text area for easy selection
    selected_text = st.text_area(
        "Page Text:",
        value=page_info['text'],
        height=400,
        key=f"page_content_{page_num}",
        help="Select and copy the mathematical content you want to create a video for"
    )
    
    return selected_text

def generate_video_interface():
    """Create the video generation interface."""
    st.header("🎬 AI Video Generator")
    
    # Input methods
    input_method = st.radio(
        "Choose input method:",
        ["📝 Manual Input", "📋 From PDF Selection"],
        horizontal=True
    )
    
    if input_method == "📝 Manual Input":
        user_input = st.text_area(
            "Enter mathematical content:",
            height=150,
            placeholder="Enter mathematical concepts, equations, or problems...",
            help="Describe what you want to visualize or paste selected PDF text here"
        )
    else:
        user_input = st.text_area(
            "Paste selected PDF text here:",
            height=150,
            placeholder="Copy text from the PDF viewer and paste it here...",
            help="Select text from the PDF pages and paste it here"
        )
    
    if user_input and user_input.strip():
        # Display selected content
        st.markdown(f'''
        <div class="selected-text-display">
            <h5>📝 Content to Visualize:</h5>
            <p style="font-style: italic;">"{user_input[:300]}{'...' if len(user_input) > 300 else ''}"</p>
            <small><strong>Length:</strong> {len(user_input)} characters</small>
        </div>
        ''', unsafe_allow_html=True)
        
        # Video settings
        st.subheader("⚙️ Video Settings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            difficulty = st.selectbox(
                "🎯 Difficulty Level",
                ["beginner", "intermediate", "advanced"],
                index=1,
                help="Choose the educational level for the explanation"
            )
        
        with col2:
            duration = st.slider(
                "⏱️ Duration (seconds)",
                min_value=20,
                max_value=180,
                value=60,
                step=10,
                help="Target video length"
            )
        
        with col3:
            quality = st.selectbox(
                "🎥 Video Quality",
                ["low_quality", "medium_quality", "high_quality"],
                index=1,
                help="Higher quality takes longer to render"
            )
        
        # Generate button
        if st.button("🚀 Generate Mathematical Video", type="primary", use_container_width=True):
            return user_input, difficulty, duration, quality
    
    return None, None, None, None

def display_video_gallery():
    """Display gallery of generated videos."""
    if st.session_state.generated_videos:
        st.header("🎬 Video Gallery")
        
        for i, video_info in enumerate(st.session_state.generated_videos):
            with st.expander(f"🎥 Video {i+1}: {video_info['topic'][:40]}...", expanded=(i==len(st.session_state.generated_videos)-1)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**📝 Topic:** {video_info['topic']}")
                    st.write(f"**📊 Status:** {video_info['status']}")
                    st.write(f"**⏰ Generated:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(video_info['timestamp']))}")
                
                with col2:
                    if video_info['status'] == 'completed' and os.path.exists(video_info['path']):
                        # Download button
                        with open(video_info['path'], 'rb') as video_file:
                            st.download_button(
                                label="📥 Download",
                                data=video_file.read(),
                                file_name=f"math_video_{i+1}.mp4",
                                mime="video/mp4",
                                key=f"download_{i}"
                            )
                
                # Display video if completed
                if video_info['status'] == 'completed' and os.path.exists(video_info['path']):
                    try:
                        with open(video_info['path'], 'rb') as video_file:
                            video_bytes = video_file.read()
                        st.video(video_bytes)
                    except Exception as e:
                        st.error(f"Error displaying video: {str(e)}")

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Advanced PDF Math Video Generator</h1>', unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="feature-highlight">
            <h4>📚 PDF Integration</h4>
            <p>Upload and view PDFs with text extraction</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="feature-highlight">
            <h4>🤖 AI Generation</h4>
            <p>GitHub AI models create educational videos</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="feature-highlight">
            <h4>🎬 Instant Videos</h4>
            <p>Professional Manim animations in minutes</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Main layout
    tab1, tab2, tab3 = st.tabs(["📄 PDF Viewer", "🎬 Video Generator", "🎥 Video Gallery"])
    
    with tab1:
        st.header("📚 PDF Document Processor")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload PDF Document",
            type=['pdf'],
            help="Upload mathematical textbooks, papers, or problem sets"
        )
        
        if uploaded_file is not None:
            # Display PDF viewer
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.subheader("📄 PDF Viewer")
                pdf_viewer = create_enhanced_pdf_viewer(uploaded_file)
                if pdf_viewer:
                    st.markdown(pdf_viewer, unsafe_allow_html=True)
            
            with col2:
                st.subheader("📊 Document Analysis")
                
                # Extract content if not already done
                if st.button("🔍 Analyze PDF Content", type="secondary"):
                    with st.spinner("Analyzing PDF content..."):
                        pages_content, metadata = extract_pdf_content(uploaded_file)
                        st.session_state.pdf_pages_text = pages_content
                        st.session_state.pdf_metadata = metadata
                        st.success("✅ PDF analysis complete!")
                
                # Display metadata if available
                if st.session_state.pdf_metadata:
                    metadata = st.session_state.pdf_metadata
                    
                    st.markdown(f'''
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                        <h5>📋 Document Info</h5>
                        <p><strong>Title:</strong> {metadata.get('title', 'Unknown')[:50]}</p>
                        <p><strong>Pages:</strong> {metadata.get('page_count', 0)}</p>
                        <p><strong>Size:</strong> {metadata.get('file_size', 0) / 1024:.1f} KB</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Page navigation
                if st.session_state.pdf_pages_text:
                    st.subheader("📖 Page Navigation")
                    
                    page_options = [f"Page {i+1} ({page['word_count']} words)" 
                                  for i, page in enumerate(st.session_state.pdf_pages_text)]
                    
                    selected_page_idx = st.selectbox(
                        "Select Page:",
                        range(len(st.session_state.pdf_pages_text)),
                        format_func=lambda x: page_options[x]
                    )
                    
                    # Display selected page content
                    if selected_page_idx < len(st.session_state.pdf_pages_text):
                        page_info = st.session_state.pdf_pages_text[selected_page_idx]
                        display_page_content(page_info, selected_page_idx)
    
    with tab2:
        # Video generation interface
        user_input, difficulty, duration, quality = generate_video_interface()
        
        if user_input:
            # Process video generation
            st.markdown('''
            <div class="video-generation-card">
                <h4>🎬 Generating Your Video...</h4>
                <p>Creating AI-powered mathematical visualization</p>
            </div>
            ''', unsafe_allow_html=True)
            
            try:
                # Initialize generator
                generator = MathVideoGenerator()
                
                # Add to video history
                video_info = {
                    'topic': user_input[:100],
                    'full_text': user_input,
                    'status': 'processing',
                    'path': '',
                    'timestamp': time.time(),
                    'settings': {
                        'difficulty': difficulty,
                        'duration': duration,
                        'quality': quality
                    }
                }
                st.session_state.generated_videos.append(video_info)
                
                # Progress tracking
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🤖 AI analyzing mathematical content...")
                    progress_bar.progress(20)
                    time.sleep(1)
                    
                    status_text.text("📝 Generating Manim animation code...")
                    progress_bar.progress(40)
                    
                    # Generate video
                    video_path = generator.create_video(
                        math_topic=user_input,
                        difficulty=difficulty,
                        duration=duration,
                        quality=quality
                    )
                    
                    progress_bar.progress(80)
                    status_text.text("🎬 Rendering final video...")
                    time.sleep(1)
                    progress_bar.progress(100)
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                
                if video_path and os.path.exists(video_path):
                    # Update video info
                    st.session_state.generated_videos[-1]['status'] = 'completed'
                    st.session_state.generated_videos[-1]['path'] = video_path
                    
                    # Success message
                    st.markdown('''
                    <div class="success-card">
                        <h4>🎉 Video Generated Successfully!</h4>
                        <p>Your mathematical visualization is ready to watch!</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Display video immediately
                    st.subheader("🎬 Your Generated Video")
                    try:
                        with open(video_path, 'rb') as video_file:
                            video_bytes = video_file.read()
                        st.video(video_bytes)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Video",
                            data=video_bytes,
                            file_name=f"math_video_{int(time.time())}.mp4",
                            mime="video/mp4",
                            type="secondary",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error displaying video: {str(e)}")
                
                else:
                    st.session_state.generated_videos[-1]['status'] = 'failed'
                    st.error("❌ Failed to generate video. Please try again with different content.")
            
            except Exception as e:
                st.error(f"❌ Error generating video: {str(e)}")
                if st.session_state.generated_videos:
                    st.session_state.generated_videos[-1]['status'] = 'failed'
    
    with tab3:
        display_video_gallery()
    
    # Sidebar with app info
    with st.sidebar:
        st.header("🎛️ Application Info")
        
        # Statistics
        total_videos = len(st.session_state.generated_videos)
        completed_videos = len([v for v in st.session_state.generated_videos if v['status'] == 'completed'])
        
        st.metric("Total Videos", total_videos)
        st.metric("Completed", completed_videos)
        st.metric("Success Rate", f"{(completed_videos/total_videos*100):.1f}%" if total_videos > 0 else "0%")
        
        st.divider()
        
        # Instructions
        st.markdown("""
        ### 📖 How to Use:
        
        1. **📄 Upload PDF**: Choose a math document
        2. **🔍 Analyze Content**: Extract text from pages
        3. **📝 Select Text**: Copy mathematical content
        4. **🎬 Generate Video**: Create AI visualization
        5. **📥 Download**: Save your video
        
        ### 🎯 Tips:
        - Select specific problems or concepts
        - Use clear mathematical language
        - Try different difficulty levels
        - Longer content = longer processing time
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <h4>🚀 Powered by Advanced AI Technology</h4>
        <p>GitHub AI Models (GPT-4o) + Manim Mathematical Animations + Streamlit</p>
        <p><strong>Workflow:</strong> 📚 PDF Upload → 🔍 Text Selection → 🤖 AI Generation → 🎬 Video Creation → 📥 Download</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
