"""
Integrated PDF Video Generator
PDF viewer with inline text selection and instant video generation
"""

import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
import base64
from pathlib import Path
import time
import json
from PIL import Image
import io
from math_video_generator import MathVideoGenerator

# Page configuration
st.set_page_config(
    page_title="Integrated PDF Video Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .pdf-display-container {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-height: 800px;
        overflow-y: auto;
    }
    
    .page-image {
        width: 100%;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin: 10px 0;
        cursor: text;
    }
    
    .text-selection-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .selected-text-display {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .quick-action-buttons {
        display: flex;
        gap: 10px;
        margin: 1rem 0;
    }
    
    .video-preview-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border: 2px solid #ff9800;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255,152,0,0.2);
    }
    
    .processing-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        color: white;
        font-size: 1.5rem;
    }
    
    .page-controls {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .stats-row {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 0.5rem;
        background: #e9ecef;
        border-radius: 5px;
        min-width: 80px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'pdf_document' not in st.session_state:
        st.session_state.pdf_document = None
    if 'pdf_pages' not in st.session_state:
        st.session_state.pdf_pages = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'selected_text' not in st.session_state:
        st.session_state.selected_text = ""
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'pdf_metadata' not in st.session_state:
        st.session_state.pdf_metadata = {}
    if 'page_images' not in st.session_state:
        st.session_state.page_images = []

def convert_pdf_to_images(pdf_file):
    """Convert PDF pages to images for better display."""
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
            'page_count': doc.page_count,
            'file_size': len(pdf_file.getvalue())
        }
        
        # Convert pages to images and extract text
        pages_data = []
        page_images = []
        
        for page_num in range(min(doc.page_count, 50)):  # Limit to 50 pages for performance
            page = doc[page_num]
            
            # Convert page to image
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image
            img = Image.open(io.BytesIO(img_data))
            page_images.append(img)
            
            # Extract text with blocks
            text = page.get_text()
            blocks = page.get_text("blocks")
            
            page_info = {
                'page_num': page_num + 1,
                'text': text,
                'blocks': blocks,
                'word_count': len(text.split()) if text else 0,
                'char_count': len(text) if text else 0
            }
            pages_data.append(page_info)
        
        doc.close()
        os.unlink(tmp_path)
        
        return pages_data, metadata, page_images
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return [], {}, []

def display_pdf_page_with_text(page_image, page_text, page_num):
    """Display PDF page as image with text overlay for selection."""
    
    # Create columns for image and text
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📄 Page {page_num}")
        
        # Display page image
        st.image(page_image, use_column_width=True, caption=f"Page {page_num}")
        
    with col2:
        st.subheader("📝 Text Content")
        
        # Display extractable text
        if page_text.strip():
            # Text selection area
            selected_text = st.text_area(
                "Select text to convert to video:",
                value=page_text,
                height=400,
                key=f"text_area_{page_num}",
                help="Select and modify the text you want to convert to a video"
            )
            
            # Quick stats
            word_count = len(selected_text.split()) if selected_text else 0
            char_count = len(selected_text) if selected_text else 0
            
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-item">
                    <strong>{word_count}</strong><br>
                    <small>Words</small>
                </div>
                <div class="stat-item">
                    <strong>{char_count}</strong><br>
                    <small>Characters</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            return selected_text
        else:
            st.warning("No text found on this page")
            return ""

def create_inline_video_generator(selected_text, page_num):
    """Create inline video generation interface."""
    if selected_text and selected_text.strip():
        st.markdown(f"""
        <div class="text-selection-box">
            <h4>🎬 Generate Video from Selected Text</h4>
            <div class="selected-text-display">{selected_text[:300]}{'...' if len(selected_text) > 300 else ''}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Video settings in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            difficulty = st.selectbox(
                "🎯 Difficulty",
                ["beginner", "intermediate", "advanced"],
                index=1,
                key=f"diff_{page_num}"
            )
        
        with col2:
            duration = st.selectbox(
                "⏱️ Duration",
                [30, 45, 60, 90, 120],
                index=2,
                key=f"dur_{page_num}"
            )
        
        with col3:
            quality = st.selectbox(
                "🎥 Quality",
                ["low_quality", "medium_quality", "high_quality"],
                index=1,
                key=f"qual_{page_num}"
            )
        
        with col4:
            st.write("")  # Spacing
            generate_button = st.button(
                "🚀 Generate Video",
                type="primary",
                key=f"gen_{page_num}",
                use_container_width=True
            )
        
        if generate_button:
            return selected_text, difficulty, duration, quality
    
    return None, None, None, None

def process_video_generation(text, difficulty, duration, quality, page_num):
    """Process video generation with real-time feedback."""
    
    # Create processing container
    progress_container = st.container()
    
    with progress_container:
        st.markdown(f"""
        <div class="video-preview-card">
            <h4>🎬 Generating Your Mathematical Video...</h4>
            <p>Converting your selected content into an educational animation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize generator
            generator = MathVideoGenerator()
            
            # Progress updates
            status_text.text("🤖 Analyzing mathematical content...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("📝 Generating Manim animation code...")
            progress_bar.progress(40)
            time.sleep(0.5)
            
            status_text.text("🎬 Rendering video (this may take 2-5 minutes)...")
            progress_bar.progress(60)
            
            # Generate video
            video_path = generator.create_video(
                math_topic=text,
                difficulty=difficulty,
                duration=duration,
                quality=quality
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Video generation complete!")
            
            # Clear progress indicators
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            if video_path and os.path.exists(video_path):
                # Store video info
                video_info = {
                    'page': page_num,
                    'topic': text[:100],
                    'path': video_path,
                    'timestamp': time.time(),
                    'settings': {
                        'difficulty': difficulty,
                        'duration': duration,
                        'quality': quality
                    }
                }
                st.session_state.generated_videos.append(video_info)
                
                # Success message
                st.success("🎉 Video generated successfully!")
                
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
                        file_name=f"math_video_page_{page_num}_{int(time.time())}.mp4",
                        mime="video/mp4",
                        key=f"download_{page_num}_{int(time.time())}"
                    )
                    
                    return True
                
                except Exception as e:
                    st.error(f"Error displaying video: {str(e)}")
                    return False
            
            else:
                st.error("❌ Failed to generate video. Please try again.")
                return False
        
        except Exception as e:
            st.error(f"❌ Error generating video: {str(e)}")
            progress_bar.empty()
            status_text.empty()
            return False

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 Integrated PDF Video Generator</h1>', unsafe_allow_html=True)
    st.markdown("**Upload a PDF → Select text directly → Generate videos instantly!**")
    
    # File upload
    uploaded_file = st.file_uploader(
        "📁 Upload Math PDF Document",
        type=['pdf'],
        help="Upload mathematical textbooks, papers, or problem sets"
    )
    
    if uploaded_file is not None:
        # Process PDF if not already done
        if (st.session_state.pdf_document is None or 
            st.session_state.pdf_document != uploaded_file.name):
            
            with st.spinner("🔍 Processing PDF document..."):
                pages_data, metadata, page_images = convert_pdf_to_images(uploaded_file)
                
                if pages_data:
                    st.session_state.pdf_pages = pages_data
                    st.session_state.pdf_metadata = metadata
                    st.session_state.page_images = page_images
                    st.session_state.pdf_document = uploaded_file.name
                    st.success(f"✅ PDF processed! Found {len(pages_data)} pages with text.")
                else:
                    st.error("❌ Failed to process PDF")
                    return
        
        # Display PDF metadata
        if st.session_state.pdf_metadata:
            metadata = st.session_state.pdf_metadata
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📄 Pages", metadata.get('page_count', 0))
            with col2:
                st.metric("📁 Size", f"{metadata.get('file_size', 0) / 1024:.1f} KB")
            with col3:
                st.metric("🎥 Videos Generated", len(st.session_state.generated_videos))
            with col4:
                completed_videos = len([v for v in st.session_state.generated_videos if os.path.exists(v.get('path', ''))])
                st.metric("✅ Completed", completed_videos)
        
        # Page navigation
        if st.session_state.pdf_pages:
            st.markdown("""
            <div class="page-controls">
                <h4>📖 Navigate Through Pages</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Page selector
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("⬅️ Previous", disabled=st.session_state.current_page <= 0):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col2:
                page_options = [f"Page {i+1} ({page['word_count']} words)" 
                              for i, page in enumerate(st.session_state.pdf_pages)]
                
                selected_page = st.selectbox(
                    "Select Page:",
                    range(len(st.session_state.pdf_pages)),
                    index=st.session_state.current_page,
                    format_func=lambda x: page_options[x],
                    key="page_selector"
                )
                
                if selected_page != st.session_state.current_page:
                    st.session_state.current_page = selected_page
                    st.rerun()
            
            with col3:
                if st.button("➡️ Next", disabled=st.session_state.current_page >= len(st.session_state.pdf_pages) - 1):
                    st.session_state.current_page += 1
                    st.rerun()
            
            # Display current page
            if st.session_state.current_page < len(st.session_state.pdf_pages):
                page_info = st.session_state.pdf_pages[st.session_state.current_page]
                page_image = st.session_state.page_images[st.session_state.current_page]
                
                # Display page with text selection
                selected_text = display_pdf_page_with_text(
                    page_image, 
                    page_info['text'], 
                    page_info['page_num']
                )
                
                # Inline video generation
                if selected_text:
                    text, difficulty, duration, quality = create_inline_video_generator(
                        selected_text, 
                        page_info['page_num']
                    )
                    
                    if text:
                        # Generate video
                        success = process_video_generation(
                            text, difficulty, duration, quality, page_info['page_num']
                        )
                        
                        if success:
                            st.balloons()
        
        # Video gallery at the bottom
        if st.session_state.generated_videos:
            st.divider()
            st.header("🎬 Generated Videos Gallery")
            
            for i, video_info in enumerate(st.session_state.generated_videos):
                with st.expander(f"🎥 Video {i+1} from Page {video_info['page']}: {video_info['topic'][:50]}...", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**📄 Source Page:** {video_info['page']}")
                        st.write(f"**📝 Topic:** {video_info['topic']}")
                        st.write(f"**⏰ Created:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(video_info['timestamp']))}")
                        
                        # Display video if exists
                        if os.path.exists(video_info['path']):
                            try:
                                with open(video_info['path'], 'rb') as video_file:
                                    video_bytes = video_file.read()
                                st.video(video_bytes)
                            except Exception as e:
                                st.error(f"Error loading video: {str(e)}")
                    
                    with col2:
                        # Download button
                        if os.path.exists(video_info['path']):
                            with open(video_info['path'], 'rb') as video_file:
                                st.download_button(
                                    label="📥 Download",
                                    data=video_file.read(),
                                    file_name=f"math_video_page_{video_info['page']}_{i+1}.mp4",
                                    mime="video/mp4",
                                    key=f"gallery_download_{i}"
                                )
    
    else:
        # Upload prompt
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;">
            <h3>📁 Upload a PDF to Get Started</h3>
            <p style="font-size: 1.1rem; color: #666;">
                Choose a mathematical PDF document from your computer.<br>
                You'll be able to view it, select text, and generate videos instantly!
            </p>
            <div style="margin: 2rem 0;">
                <p><strong>✨ Features:</strong></p>
                <p>📄 Visual PDF viewer • 📝 Direct text selection • 🎬 Instant video generation • 📥 Easy downloads</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <p>🚀 <strong>Integrated PDF Video Generator</strong></p>
        <p>Powered by GitHub AI + Manim + Streamlit | Upload → Select → Generate → Download</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
