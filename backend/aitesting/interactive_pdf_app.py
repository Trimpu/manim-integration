"""
Interactive PDF Video Generator
PDF viewer with direct text selection and floating action popups
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
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Interactive PDF Video Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with interactive text selection
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
    
    .pdf-viewer-container {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        position: relative;
        max-height: 800px;
        overflow-y: auto;
    }
    
    .pdf-page-container {
        position: relative;
        margin: 20px 0;
        display: inline-block;
        width: 100%;
    }
    
    .pdf-page-image {
        width: 100%;
        border: 1px solid #ddd;
        border-radius: 5px;
        display: block;
    }
    
    .text-layer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: auto;
        z-index: 2;
    }
    
    .text-block {
        position: absolute;
        cursor: text;
        user-select: text;
        color: transparent;
        background: rgba(0, 0, 255, 0.1);
        border-radius: 2px;
        font-family: Arial, sans-serif;
        line-height: 1.2;
        white-space: pre;
    }
    
    .text-block:hover {
        background: rgba(0, 0, 255, 0.2);
    }
    
    .text-block::selection {
        background: rgba(255, 255, 0, 0.6);
        color: black;
    }
    
    .selection-popup {
        position: fixed;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 1000;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
        animation: popup-appear 0.2s ease-out;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .selection-popup:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(0,0,0,0.4);
    }
    
    @keyframes popup-appear {
        from {
            opacity: 0;
            transform: scale(0.8) translateY(10px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    .video-result-container {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border: 2px solid #ff9800;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(255,152,0,0.2);
        animation: result-appear 0.5s ease-out;
    }
    
    @keyframes result-appear {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .generation-progress {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
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
    
    .selected-text-display {
        background: #f8f9fa;
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        max-height: 150px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    
    .generation-settings {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
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
    if 'page_text_blocks' not in st.session_state:
        st.session_state.page_text_blocks = []
    if 'generation_in_progress' not in st.session_state:
        st.session_state.generation_in_progress = False

def extract_text_blocks_with_positions(page):
    """Extract text blocks with their exact positions for overlay."""
    blocks = []
    
    # Get text blocks with position information
    text_dict = page.get_text("dict")
    
    for block in text_dict["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        bbox = span["bbox"]  # [x0, y0, x1, y1]
                        blocks.append({
                            "text": span["text"],
                            "bbox": bbox,
                            "font": span["font"],
                            "size": span["size"],
                            "flags": span["flags"]
                        })
    
    return blocks

def convert_pdf_to_interactive_pages(pdf_file):
    """Convert PDF pages to images with text overlay information."""
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
        
        # Convert pages to images and extract text with positions
        pages_data = []
        page_images = []
        page_text_blocks = []
        
        for page_num in range(min(doc.page_count, 20)):  # Limit to 20 pages for performance
            page = doc[page_num]
            
            # Convert page to image with higher resolution
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image
            img = Image.open(io.BytesIO(img_data))
            page_images.append(img)
            
            # Extract text blocks with positions
            text_blocks = extract_text_blocks_with_positions(page)
            page_text_blocks.append(text_blocks)
            
            # Extract plain text
            text = page.get_text()
            
            page_info = {
                'page_num': page_num + 1,
                'text': text,
                'word_count': len(text.split()) if text else 0,
                'char_count': len(text) if text else 0,
                'image_size': img.size  # (width, height)
            }
            pages_data.append(page_info)
        
        doc.close()
        os.unlink(tmp_path)
        
        return pages_data, metadata, page_images, page_text_blocks
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return [], {}, [], []

def create_interactive_pdf_viewer(page_image, text_blocks, page_num):
    """Create an interactive PDF viewer with selectable text overlay."""
    
    # Convert PIL image to base64 for HTML display
    img_buffer = io.BytesIO()
    page_image.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    # Get image dimensions
    img_width, img_height = page_image.size
    
    # Create text overlay HTML
    text_overlay_html = ""
    for i, block in enumerate(text_blocks):
        x0, y0, x1, y1 = block["bbox"]
        
        # Scale coordinates to match the display size
        # Assuming the image is displayed at a reasonable width
        scale_factor = 0.5  # Adjust based on actual display
        
        left = x0 * scale_factor
        top = y0 * scale_factor
        width = (x1 - x0) * scale_factor
        height = (y1 - y0) * scale_factor
        font_size = max(8, block["size"] * scale_factor * 0.7)
        
        text_overlay_html += f"""
        <div class="text-block" 
             style="left: {left}px; top: {top}px; width: {width}px; height: {height}px; font-size: {font_size}px;"
             data-text="{block['text']}"
             data-block-id="{i}">
            {block['text']}
        </div>
        """
    
    # Interactive PDF viewer HTML with JavaScript
    interactive_html = f"""
    <div class="pdf-viewer-container">
        <div class="pdf-page-container" id="page-{page_num}">
            <img src="data:image/png;base64,{img_str}" 
                 class="pdf-page-image" 
                 id="pdf-image-{page_num}"
                 style="width: 100%; max-width: 800px;">
            <div class="text-layer" id="text-layer-{page_num}">
                {text_overlay_html}
            </div>
        </div>
    </div>
    
    <script>
    (function() {{
        let selectedText = '';
        let selectionPopup = null;
        
        // Remove any existing popup
        function removePopup() {{
            if (selectionPopup) {{
                selectionPopup.remove();
                selectionPopup = null;
            }}
        }}
        
        // Handle text selection
        function handleSelection() {{
            const selection = window.getSelection();
            const selectedStr = selection.toString().trim();
            
            if (selectedStr.length > 0) {{
                selectedText = selectedStr;
                showSelectionPopup(selection);
            }} else {{
                removePopup();
            }}
        }}
        
        // Show floating action popup
        function showSelectionPopup(selection) {{
            removePopup();
            
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            
            selectionPopup = document.createElement('div');
            selectionPopup.className = 'selection-popup';
            selectionPopup.innerHTML = '🎬 Generate Video';
            selectionPopup.style.left = (rect.left + rect.width / 2 - 75) + 'px';
            selectionPopup.style.top = (rect.top - 45) + 'px';
            
            selectionPopup.onclick = function() {{
                generateVideoFromSelection(selectedText);
                removePopup();
                selection.removeAllRanges();
            }};
            
            document.body.appendChild(selectionPopup);
        }}
        
        // Send selected text to Streamlit for video generation
        function generateVideoFromSelection(text) {{
            // Store selected text in Streamlit session state
            window.parent.postMessage({{
                type: 'text_selected',
                text: text,
                page: {page_num}
            }}, '*');
        }}
        
        // Add event listeners
        const textLayer = document.getElementById('text-layer-{page_num}');
        if (textLayer) {{
            textLayer.addEventListener('mouseup', handleSelection);
            textLayer.addEventListener('touchend', handleSelection);
        }}
        
        // Remove popup when clicking elsewhere
        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.text-layer') && !e.target.closest('.selection-popup')) {{
                removePopup();
            }}
        }});
        
        // Handle messages from parent
        window.addEventListener('message', function(event) {{
            if (event.data.type === 'clear_selection') {{
                removePopup();
                window.getSelection().removeAllRanges();
            }}
        }});
    }})();
    </script>
    """
    
    return interactive_html

def process_video_generation_interactive(text, page_num):
    """Process video generation with enhanced UI feedback."""
    
    # Create progress container
    progress_placeholder = st.empty()
    
    with progress_placeholder.container():
        st.markdown(f"""
        <div class="generation-progress">
            <h3>🎬 Generating Mathematical Video</h3>
            <p><strong>Selected Text:</strong> "{text[:100]}{'...' if len(text) > 100 else ''}"</p>
            <p>🤖 Processing with AI and Manim...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize generator
            generator = MathVideoGenerator()
            
            # Progress updates
            status_text.text("🧠 AI analyzing mathematical content...")
            progress_bar.progress(25)
            time.sleep(1)
            
            status_text.text("📝 Generating Manim animation code...")
            progress_bar.progress(50)
            time.sleep(1)
            
            status_text.text("🎬 Rendering video (2-5 minutes)...")
            progress_bar.progress(75)
            
            # Generate video with default settings
            video_path = generator.create_video(
                math_topic=text,
                difficulty="intermediate",
                duration=60,
                quality="medium_quality"
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Video generation complete!")
            time.sleep(1)
            
            # Clear progress indicators
            progress_placeholder.empty()
            
            if video_path and os.path.exists(video_path):
                # Store video info
                video_info = {
                    'page': page_num,
                    'topic': text[:100],
                    'path': video_path,
                    'timestamp': time.time(),
                    'full_text': text
                }
                st.session_state.generated_videos.append(video_info)
                
                # Display success with video
                st.markdown(f"""
                <div class="video-result-container">
                    <h3>🎉 Video Generated Successfully!</h3>
                    <p><strong>📄 From Page:</strong> {page_num}</p>
                    <p><strong>📝 Source Text:</strong> "{text[:150]}{'...' if len(text) > 150 else ''}"</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display video
                try:
                    with open(video_path, 'rb') as video_file:
                        video_bytes = video_file.read()
                    
                    st.video(video_bytes)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Video",
                        data=video_bytes,
                        file_name=f"selected_text_video_page_{page_num}_{int(time.time())}.mp4",
                        mime="video/mp4",
                        key=f"download_interactive_{page_num}_{int(time.time())}"
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
            progress_placeholder.empty()
            return False

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 Interactive PDF Video Generator</h1>', unsafe_allow_html=True)
    st.markdown("**Upload PDF → Select text directly → Generate videos instantly!**")
    
    # JavaScript message handler for text selection
    components.html("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'text_selected') {
            // Send the selected text to Streamlit
            window.parent.postMessage({
                type: 'streamlit_message',
                text: event.data.text,
                page: event.data.page
            }, '*');
        }
    });
    </script>
    """, height=0)
    
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
            
            with st.spinner("🔍 Processing PDF for interactive viewing..."):
                pages_data, metadata, page_images, page_text_blocks = convert_pdf_to_interactive_pages(uploaded_file)
                
                if pages_data:
                    st.session_state.pdf_pages = pages_data
                    st.session_state.pdf_metadata = metadata
                    st.session_state.page_images = page_images
                    st.session_state.page_text_blocks = page_text_blocks
                    st.session_state.pdf_document = uploaded_file.name
                    st.success(f"✅ PDF processed! Found {len(pages_data)} interactive pages.")
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
                st.metric("✅ Available", completed_videos)
        
        # Instructions
        st.markdown("""
        <div style="background: #e8f5e8; border: 2px solid #28a745; border-radius: 10px; padding: 1rem; margin: 1rem 0;">
            <h4>📖 How to Use Interactive Selection:</h4>
            <p>• <strong>Navigate:</strong> Use the controls below to browse pages</p>
            <p>• <strong>Select Text:</strong> Click and drag directly on the PDF to select mathematical content</p>
            <p>• <strong>Generate Video:</strong> A "🎬 Generate Video" popup will appear - click it to create your animation</p>
            <p>• <strong>Watch & Download:</strong> Videos appear immediately below with download options</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            
            # Display current page with interactive text selection
            if st.session_state.current_page < len(st.session_state.pdf_pages):
                page_info = st.session_state.pdf_pages[st.session_state.current_page]
                page_image = st.session_state.page_images[st.session_state.current_page]
                text_blocks = st.session_state.page_text_blocks[st.session_state.current_page]
                
                st.subheader(f"📄 Page {page_info['page_num']} - Interactive View")
                
                # Create interactive PDF viewer
                interactive_html = create_interactive_pdf_viewer(
                    page_image, 
                    text_blocks, 
                    page_info['page_num']
                )
                
                # Display interactive viewer
                components.html(interactive_html, height=600, scrolling=True)
        
        # Check for text selection (this would need to be enhanced with actual JS communication)
        # For demo purposes, add a manual text input for testing
        st.divider()
        st.subheader("🧪 Manual Text Selection (for testing)")
        test_text = st.text_area(
            "Or manually enter text to test video generation:",
            placeholder="Enter mathematical content here...",
            height=100
        )
        
        if st.button("🎬 Generate Video from Manual Input", type="primary") and test_text:
            success = process_video_generation_interactive(test_text, st.session_state.current_page + 1)
            if success:
                st.balloons()
        
        # Video gallery
        if st.session_state.generated_videos:
            st.divider()
            st.header("🎬 Generated Videos Gallery")
            
            for i, video_info in enumerate(st.session_state.generated_videos):
                with st.expander(f"🎥 Video {i+1} from Page {video_info['page']}: {video_info['topic'][:50]}...", expanded=i == len(st.session_state.generated_videos) - 1):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**📄 Source Page:** {video_info['page']}")
                        st.write(f"**📝 Selected Text:** {video_info['full_text'][:200]}{'...' if len(video_info['full_text']) > 200 else ''}")
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
                                    file_name=f"interactive_video_{video_info['page']}_{i+1}.mp4",
                                    mime="video/mp4",
                                    key=f"gallery_download_{i}"
                                )
    
    else:
        # Upload prompt
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;">
            <h3>📁 Upload a PDF to Get Started</h3>
            <p style="font-size: 1.2rem; color: #666; margin: 1rem 0;">
                Experience the next generation of PDF interaction!
            </p>
            <div style="margin: 2rem 0; font-size: 1.1rem;">
                <p><strong>✨ New Interactive Features:</strong></p>
                <p>🖱️ Direct text selection on PDF pages</p>
                <p>💫 Floating action popups</p>
                <p>🎬 Instant video generation</p>
                <p>📥 Seamless workflow</p>
            </div>
            <p style="color: #888;">Select text directly from the PDF and generate mathematical videos instantly!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <p>🚀 <strong>Interactive PDF Video Generator</strong></p>
        <p>Next-Gen PDF Experience | Direct Selection • Floating Actions • Instant Videos</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
