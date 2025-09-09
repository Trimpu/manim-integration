"""
Enhanced Interactive PDF Video Generator
Real-time text selection with JavaScript-Streamlit communication
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
    page_title="Enhanced Interactive PDF Video Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 0
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'pdf_metadata' not in st.session_state:
        st.session_state.pdf_metadata = {}
    if 'page_images' not in st.session_state:
        st.session_state.page_images = []
    if 'page_text_blocks' not in st.session_state:
        st.session_state.page_text_blocks = []
    if 'trigger_generation' not in st.session_state:
        st.session_state.trigger_generation = False

def extract_text_blocks_with_positions(page):
    """Extract text blocks with their exact positions for overlay."""
    blocks = []
    
    # Get text blocks with position information
    text_dict = page.get_text("dict")
    
    for block in text_dict["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                line_text = ""
                line_bbox = None
                
                for span in line["spans"]:
                    if span["text"].strip():
                        line_text += span["text"]
                        if line_bbox is None:
                            line_bbox = list(span["bbox"])
                        else:
                            # Extend bbox to include this span
                            line_bbox[2] = max(line_bbox[2], span["bbox"][2])
                            line_bbox[3] = max(line_bbox[3], span["bbox"][3])
                
                if line_text.strip() and line_bbox:
                    blocks.append({
                        "text": line_text,
                        "bbox": line_bbox,
                        "font": span.get("font", "Arial"),
                        "size": span.get("size", 12)
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
        
        for page_num in range(min(doc.page_count, 15)):  # Limit to 15 pages for performance
            page = doc[page_num]
            
            # Convert page to image with higher resolution
            mat = fitz.Matrix(1.5, 1.5)  # 1.5x zoom for good quality
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

def create_enhanced_pdf_viewer(page_image, text_blocks, page_num):
    """Create an enhanced PDF viewer with real text selection."""
    
    # Convert PIL image to base64 for HTML display
    img_buffer = io.BytesIO()
    page_image.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    # Get image dimensions
    img_width, img_height = page_image.size
    
    # Create JavaScript-enabled HTML component
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
                background: #f8f9fa;
            }}
            
            .pdf-container {{
                position: relative;
                display: inline-block;
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                overflow: hidden;
                max-width: 100%;
            }}
            
            .pdf-image {{
                display: block;
                width: 100%;
                max-width: 800px;
                height: auto;
            }}
            
            .text-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 2;
            }}
            
            .text-line {{
                position: absolute;
                cursor: text;
                user-select: text;
                color: transparent;
                line-height: 1.1;
                white-space: nowrap;
                overflow: hidden;
                padding: 1px;
                border-radius: 2px;
                transition: background-color 0.2s;
            }}
            
            .text-line:hover {{
                background-color: rgba(0, 123, 255, 0.1);
            }}
            
            .text-line::selection {{
                background-color: rgba(255, 193, 7, 0.6);
                color: black;
            }}
            
            .selection-popup {{
                position: fixed;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 20px;
                border-radius: 25px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                z-index: 1000;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                animation: popup-appear 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                border: 2px solid rgba(255,255,255,0.3);
                backdrop-filter: blur(10px);
            }}
            
            .selection-popup:hover {{
                transform: scale(1.05);
                box-shadow: 0 12px 30px rgba(0,0,0,0.4);
            }}
            
            .selection-popup:active {{
                transform: scale(0.95);
            }}
            
            @keyframes popup-appear {{
                from {{
                    opacity: 0;
                    transform: scale(0.5) translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }}
            }}
            
            .selected-text-preview {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                border: 2px solid #28a745;
                border-radius: 10px;
                padding: 15px;
                max-width: 300px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 999;
                font-size: 12px;
                animation: slide-in 0.3s ease-out;
            }}
            
            @keyframes slide-in {{
                from {{
                    opacity: 0;
                    transform: translateX(100%);
                }}
                to {{
                    opacity: 1;
                    transform: translateX(0);
                }}
            }}
            
            .preview-header {{
                font-weight: bold;
                color: #28a745;
                margin-bottom: 8px;
                font-size: 13px;
            }}
            
            .preview-text {{
                color: #333;
                line-height: 1.3;
                max-height: 80px;
                overflow-y: auto;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div class="pdf-container" id="pdf-container">
            <img src="data:image/png;base64,{img_str}" 
                 class="pdf-image" 
                 id="pdf-image"
                 draggable="false">
            <div class="text-overlay" id="text-overlay">
    """
    
    # Add text blocks as selectable overlays
    for i, block in enumerate(text_blocks):
        if not block["text"].strip():
            continue
            
        x0, y0, x1, y1 = block["bbox"]
        
        # Calculate relative positions as percentages
        left_percent = (x0 / img_width) * 100
        top_percent = (y0 / img_height) * 100
        width_percent = ((x1 - x0) / img_width) * 100
        height_percent = ((y1 - y0) / img_height) * 100
        
        # Estimate font size based on block height
        font_size = max(8, (y1 - y0) * 0.8)
        
        html_content += f"""
            <div class="text-line" 
                 style="left: {left_percent}%; top: {top_percent}%; 
                        width: {width_percent}%; height: {height_percent}%;
                        font-size: {font_size}px;"
                 data-text="{block['text']}" 
                 data-block-id="{i}">
                {block['text']}
            </div>
        """
    
    html_content += f"""
            </div>
        </div>

        <script>
            let currentSelection = '';
            let selectionPopup = null;
            let textPreview = null;
            let isGenerating = false;

            function removePopup() {{
                if (selectionPopup) {{
                    selectionPopup.remove();
                    selectionPopup = null;
                }}
            }}

            function removePreview() {{
                if (textPreview) {{
                    textPreview.remove();
                    textPreview = null;
                }}
            }}

            function showTextPreview(text) {{
                removePreview();
                
                textPreview = document.createElement('div');
                textPreview.className = 'selected-text-preview';
                textPreview.innerHTML = `
                    <div class="preview-header">✨ Selected Text</div>
                    <div class="preview-text">${{text.substring(0, 200)}}${{text.length > 200 ? '...' : ''}}</div>
                `;
                
                document.body.appendChild(textPreview);
                
                // Auto-remove after 5 seconds
                setTimeout(() => {{
                    removePreview();
                }}, 5000);
            }}

            function handleTextSelection() {{
                const selection = window.getSelection();
                const selectedText = selection.toString().trim();
                
                removePopup();
                
                if (selectedText.length > 5) {{
                    currentSelection = selectedText;
                    showSelectionPopup(selection);
                    showTextPreview(selectedText);
                }} else {{
                    removePreview();
                }}
            }}

            function showSelectionPopup(selection) {{
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();
                
                selectionPopup = document.createElement('div');
                selectionPopup.className = 'selection-popup';
                selectionPopup.innerHTML = '🎬 Generate Video';
                
                // Position popup above selection
                const popupX = rect.left + (rect.width / 2) - 75;
                const popupY = rect.top - 50;
                
                selectionPopup.style.left = Math.max(10, popupX) + 'px';
                selectionPopup.style.top = Math.max(10, popupY) + 'px';
                
                selectionPopup.onclick = function(e) {{
                    e.preventDefault();
                    if (!isGenerating && currentSelection.length > 5) {{
                        generateVideo();
                    }}
                }};
                
                document.body.appendChild(selectionPopup);
            }}

            function generateVideo() {{
                if (isGenerating) return;
                
                isGenerating = true;
                selectionPopup.innerHTML = '⏳ Generating...';
                selectionPopup.style.cursor = 'not-allowed';
                
                // Send message to Streamlit parent
                const message = {{
                    type: 'generate_video',
                    text: currentSelection,
                    page: {page_num},
                    timestamp: Date.now()
                }};
                
                // Post message to parent window (Streamlit)
                if (window.parent) {{
                    window.parent.postMessage(message, '*');
                }} else {{
                    console.log('Message to send:', message);
                }}
                
                // Clean up UI
                setTimeout(() => {{
                    removePopup();
                    removePreview();
                    window.getSelection().removeAllRanges();
                    isGenerating = false;
                }}, 1000);
            }}

            // Event listeners
            document.addEventListener('mouseup', handleTextSelection);
            document.addEventListener('touchend', handleTextSelection);
            
            // Clear selection when clicking outside
            document.addEventListener('click', function(e) {{
                if (!e.target.closest('.text-overlay') && !e.target.closest('.selection-popup')) {{
                    removePopup();
                    removePreview();
                }}
            }});
            
            // Keyboard shortcuts
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    removePopup();
                    removePreview();
                    window.getSelection().removeAllRanges();
                }}
                
                if ((e.ctrlKey || e.metaKey) && e.key === 'g' && currentSelection.length > 5) {{
                    e.preventDefault();
                    generateVideo();
                }}
            }});
            
            // Listen for messages from parent
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'clear_selection') {{
                    removePopup();
                    removePreview();
                    window.getSelection().removeAllRanges();
                    currentSelection = '';
                    isGenerating = false;
                }}
            }});
            
            console.log('Interactive PDF viewer loaded with {{len(text_blocks)}} text blocks');
        </script>
    </body>
    </html>
    """
    
    return html_content

def process_video_from_selection(selected_text, page_num):
    """Process video generation from user selection."""
    
    if not selected_text or len(selected_text.strip()) < 5:
        st.warning("⚠️ Selected text is too short. Please select more content.")
        return False
    
    # Create dynamic progress display
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    border: 2px solid #2196f3; border-radius: 15px; padding: 2rem; 
                    text-align: center; animation: pulse 2s infinite;">
            <h3>🎬 Generating Video from Selected Text</h3>
            <div style="background: white; border-radius: 8px; padding: 1rem; margin: 1rem 0; 
                        font-family: monospace; font-size: 0.9rem; max-height: 120px; overflow-y: auto;">
                "{selected_text[:300]}{'...' if len(selected_text) > 300 else ''}"
            </div>
            <p>🤖 AI is processing your mathematical content...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize generator
            generator = MathVideoGenerator()
            
            # Step-by-step progress
            status_text.text("🧠 Analyzing mathematical content with AI...")
            progress_bar.progress(20)
            time.sleep(0.8)
            
            status_text.text("📝 Generating Manim animation code...")
            progress_bar.progress(40)
            time.sleep(0.8)
            
            status_text.text("🎬 Rendering high-quality video...")
            progress_bar.progress(60)
            time.sleep(0.5)
            
            # Generate video
            video_path = generator.create_video(
                math_topic=selected_text,
                difficulty="intermediate",
                duration=60,
                quality="medium_quality"
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Video generation complete!")
            time.sleep(1)
            
            # Clear progress
            progress_container.empty()
            
            if video_path and os.path.exists(video_path):
                # Store video info
                video_info = {
                    'page': page_num,
                    'topic': selected_text[:100],
                    'path': video_path,
                    'timestamp': time.time(),
                    'full_text': selected_text,
                    'method': 'selection'
                }
                st.session_state.generated_videos.append(video_info)
                
                # Success display
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                            border: 2px solid #28a745; border-radius: 15px; padding: 2rem; 
                            margin: 2rem 0; animation: slideIn 0.5s ease-out;">
                    <h3>🎉 Video Generated Successfully!</h3>
                    <p><strong>📄 Source:</strong> Page {page_num} (Text Selection)</p>
                    <p><strong>📊 Stats:</strong> {len(selected_text)} characters, {len(selected_text.split())} words</p>
                    <p><strong>⏰ Generated:</strong> {time.strftime('%H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display video immediately
                st.subheader("🎬 Your Generated Video")
                
                try:
                    with open(video_path, 'rb') as video_file:
                        video_bytes = video_file.read()
                    
                    st.video(video_bytes)
                    
                    # Download options
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download MP4",
                            data=video_bytes,
                            file_name=f"selected_text_video_p{page_num}_{int(time.time())}.mp4",
                            mime="video/mp4",
                            key=f"download_selection_{page_num}_{int(time.time())}"
                        )
                    
                    with col2:
                        if st.button("🔄 Generate Another", key=f"regenerate_{int(time.time())}"):
                            st.rerun()
                    
                    with col3:
                        if st.button("📋 Copy Video Path", key=f"copy_path_{int(time.time())}"):
                            st.success(f"Path: {video_path}")
                    
                    return True
                
                except Exception as e:
                    st.error(f"Error displaying video: {str(e)}")
                    return False
            
            else:
                st.error("❌ Failed to generate video. Please try again.")
                return False
        
        except Exception as e:
            st.error(f"❌ Error generating video: {str(e)}")
            progress_container.empty()
            return False

def main():
    """Enhanced main application."""
    initialize_session_state()
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        .main-header {
            font-family: 'Inter', sans-serif;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
            font-weight: 300;
        }
        
        .feature-highlight {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 0 10px 10px 0;
            margin: 1rem 0;
        }
        
        .stats-container {
            background: white;
            border-radius: 15px;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📚 Enhanced Interactive PDF Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Select text directly from PDF pages • Generate videos instantly</p>', unsafe_allow_html=True)
    
    # Message handler for JavaScript communication
    if 'message_handler' not in st.session_state:
        st.session_state.message_handler = True
        
        # JavaScript message listener
        components.html("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'generate_video') {
                // Store the selection data in session storage
                sessionStorage.setItem('selectedText', event.data.text);
                sessionStorage.setItem('selectedPage', event.data.page);
                sessionStorage.setItem('triggerGeneration', 'true');
                
                // Trigger Streamlit rerun by changing a query parameter
                const url = new URL(window.location);
                url.searchParams.set('trigger', Date.now());
                window.history.replaceState({}, '', url);
                
                // Force refresh
                window.location.reload();
            }
        });
        
        // Check for stored selection on page load
        if (sessionStorage.getItem('triggerGeneration') === 'true') {
            const selectedText = sessionStorage.getItem('selectedText');
            const selectedPage = sessionStorage.getItem('selectedPage');
            
            if (selectedText && selectedPage) {
                // Clear the trigger
                sessionStorage.removeItem('triggerGeneration');
                
                // Send to Streamlit (this is a simplified approach)
                console.log('Triggering video generation for:', selectedText);
            }
        }
        </script>
        """, height=0)
    
    # Check URL parameters for trigger
    query_params = st.query_params
    if 'trigger' in query_params:
        # This indicates a page reload after text selection
        st.query_params.clear()
    
    # File upload
    uploaded_file = st.file_uploader(
        "📁 Upload Mathematical PDF Document",
        type=['pdf'],
        help="Upload textbooks, research papers, or problem sets"
    )
    
    if uploaded_file is not None:
        # Process PDF if not already done
        if (st.session_state.pdf_document is None or 
            st.session_state.pdf_document != uploaded_file.name):
            
            with st.spinner("🔍 Processing PDF for interactive text selection..."):
                pages_data, metadata, page_images, page_text_blocks = convert_pdf_to_interactive_pages(uploaded_file)
                
                if pages_data:
                    st.session_state.pdf_pages = pages_data
                    st.session_state.pdf_metadata = metadata
                    st.session_state.page_images = page_images
                    st.session_state.page_text_blocks = page_text_blocks
                    st.session_state.pdf_document = uploaded_file.name
                    st.success(f"✅ PDF processed! Ready for interactive text selection on {len(pages_data)} pages.")
                else:
                    st.error("❌ Failed to process PDF")
                    return
        
        # Display metadata
        if st.session_state.pdf_metadata:
            metadata = st.session_state.pdf_metadata
            
            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📄 Pages", metadata.get('page_count', 0))
            with col2:
                st.metric("📁 Size", f"{metadata.get('file_size', 0) / 1024:.1f} KB")
            with col3:
                st.metric("🎥 Videos", len(st.session_state.generated_videos))
            with col4:
                available_videos = len([v for v in st.session_state.generated_videos if os.path.exists(v.get('path', ''))])
                st.metric("✅ Available", available_videos)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
        <div class="feature-highlight">
            <h4>🎯 How to Use Interactive Selection:</h4>
            <ul>
                <li><strong>📖 Navigate:</strong> Use the page controls below to browse your PDF</li>
                <li><strong>🖱️ Select Text:</strong> Click and drag directly on the PDF to select mathematical content</li>
                <li><strong>💫 Generate:</strong> Click the floating "🎬 Generate Video" popup that appears</li>
                <li><strong>⚡ Shortcuts:</strong> Press Ctrl+G after selecting text, or Escape to clear selection</li>
                <li><strong>📥 Download:</strong> Videos appear immediately with download options</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Page navigation
        if st.session_state.pdf_pages:
            # Page controls
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("⬅️ Previous Page", disabled=st.session_state.current_page <= 0):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col2:
                page_options = [f"Page {i+1} ({page['word_count']} words)" 
                              for i, page in enumerate(st.session_state.pdf_pages)]
                
                selected_page = st.selectbox(
                    "📖 Select Page:",
                    range(len(st.session_state.pdf_pages)),
                    index=st.session_state.current_page,
                    format_func=lambda x: page_options[x],
                    key="enhanced_page_selector"
                )
                
                if selected_page != st.session_state.current_page:
                    st.session_state.current_page = selected_page
                    st.rerun()
            
            with col3:
                if st.button("➡️ Next Page", disabled=st.session_state.current_page >= len(st.session_state.pdf_pages) - 1):
                    st.session_state.current_page += 1
                    st.rerun()
            
            # Display current page
            if st.session_state.current_page < len(st.session_state.pdf_pages):
                page_info = st.session_state.pdf_pages[st.session_state.current_page]
                page_image = st.session_state.page_images[st.session_state.current_page]
                text_blocks = st.session_state.page_text_blocks[st.session_state.current_page]
                
                st.subheader(f"📄 Page {page_info['page_num']} - Interactive Text Selection")
                
                # Create and display interactive viewer
                interactive_html = create_enhanced_pdf_viewer(
                    page_image, 
                    text_blocks, 
                    page_info['page_num']
                )
                
                # Display interactive viewer
                components.html(interactive_html, height=700, scrolling=True)
        
        # Manual text input for testing
        st.divider()
        
        with st.expander("🧪 Manual Text Input (for testing)", expanded=False):
            test_text = st.text_area(
                "Enter mathematical content manually:",
                placeholder="Type or paste mathematical content here for testing...",
                height=100,
                key="manual_test_input"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎬 Generate Video from Manual Input", type="primary", key="manual_generate") and test_text:
                    success = process_video_from_selection(test_text, st.session_state.current_page + 1)
                    if success:
                        st.balloons()
            
            with col2:
                if st.button("🔄 Clear Input", key="clear_manual"):
                    st.rerun()
        
        # Video gallery
        if st.session_state.generated_videos:
            st.divider()
            st.header("🎬 Generated Videos Gallery")
            
            # Sort videos by timestamp (newest first)
            sorted_videos = sorted(st.session_state.generated_videos, key=lambda x: x['timestamp'], reverse=True)
            
            for i, video_info in enumerate(sorted_videos):
                with st.expander(
                    f"🎥 Video {i+1} from Page {video_info['page']}: {video_info['topic'][:60]}...", 
                    expanded=(i == 0)  # Expand the newest video
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**📄 Source:** Page {video_info['page']} ({video_info.get('method', 'unknown')})")
                        st.markdown(f"**📝 Content:** {video_info.get('full_text', video_info['topic'])[:300]}{'...' if len(video_info.get('full_text', '')) > 300 else ''}")
                        st.markdown(f"**⏰ Generated:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(video_info['timestamp']))}")
                        
                        # Display video
                        if os.path.exists(video_info['path']):
                            try:
                                with open(video_info['path'], 'rb') as video_file:
                                    video_bytes = video_file.read()
                                st.video(video_bytes)
                            except Exception as e:
                                st.error(f"Error loading video: {str(e)}")
                        else:
                            st.warning("Video file not found")
                    
                    with col2:
                        st.markdown("**📊 Video Info**")
                        st.write(f"Size: {os.path.getsize(video_info['path']) / (1024*1024):.1f} MB" if os.path.exists(video_info['path']) else "N/A")
                        
                        # Download button
                        if os.path.exists(video_info['path']):
                            with open(video_info['path'], 'rb') as video_file:
                                st.download_button(
                                    label="📥 Download",
                                    data=video_file.read(),
                                    file_name=f"enhanced_video_p{video_info['page']}_{i+1}.mp4",
                                    mime="video/mp4",
                                    key=f"enhanced_download_{i}",
                                    use_container_width=True
                                )
    
    else:
        # Upload prompt
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    border-radius: 20px; margin: 2rem 0; border: 2px dashed #667eea;">
            <h2>📁 Upload Your PDF to Experience the Future</h2>
            <p style="font-size: 1.3rem; color: #666; margin: 1.5rem 0;">
                Revolutionary PDF interaction with direct text selection and instant video generation
            </p>
            <div style="margin: 2.5rem 0;">
                <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                    <div style="background: white; padding: 1rem; border-radius: 10px; min-width: 200px;">
                        <h4>🖱️ Direct Selection</h4>
                        <p>Select text directly from PDF pages</p>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 10px; min-width: 200px;">
                        <h4>💫 Floating Actions</h4>
                        <p>Contextual popup menus</p>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 10px; min-width: 200px;">
                        <h4>⚡ Instant Videos</h4>
                        <p>Real-time generation</p>
                    </div>
                </div>
            </div>
            <p style="color: #888; font-style: italic;">Upload a mathematical PDF and watch the magic happen!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0; font-family: 'Inter', sans-serif;">
        <p style="font-size: 1.1rem; font-weight: 600;">🚀 Enhanced Interactive PDF Video Generator</p>
        <p>Next-Generation PDF Experience | Direct Text Selection • Floating UI • Instant Generation</p>
        <p style="font-size: 0.9rem; color: #888;">Powered by GitHub AI • Manim • Advanced JavaScript</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
