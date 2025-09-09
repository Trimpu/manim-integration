"""
Direct Selection PDF Video Generator
Streamlit-optimized version with real text selection handling
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
    page_title="Direct Selection PDF Video Generator",
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
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'pdf_metadata' not in st.session_state:
        st.session_state.pdf_metadata = {}
    if 'page_images' not in st.session_state:
        st.session_state.page_images = []
    if 'page_text_blocks' not in st.session_state:
        st.session_state.page_text_blocks = []
    if 'selected_text_for_generation' not in st.session_state:
        st.session_state.selected_text_for_generation = ""
    if 'trigger_video_generation' not in st.session_state:
        st.session_state.trigger_video_generation = False

def extract_text_with_coordinates(page):
    """Extract text with precise coordinates for overlay positioning."""
    text_instances = []
    blocks = page.get_text("dict")
    
    for block in blocks["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        text_instances.append({
                            "text": span["text"],
                            "bbox": span["bbox"],  # [x0, y0, x1, y1]
                            "font": span.get("font", "Arial"),
                            "size": span.get("size", 12),
                            "flags": span.get("flags", 0)
                        })
    
    return text_instances

def convert_pdf_with_text_overlay(pdf_file):
    """Convert PDF to images with text overlay data."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        doc = fitz.open(tmp_path)
        
        metadata = {
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'page_count': doc.page_count,
            'file_size': len(pdf_file.getvalue())
        }
        
        pages_data = []
        page_images = []
        page_text_data = []
        
        for page_num in range(min(doc.page_count, 10)):
            page = doc[page_num]
            
            # Convert to high-quality image
            mat = fitz.Matrix(1.5, 1.5)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            page_images.append(img)
            
            # Extract text with coordinates
            text_instances = extract_text_with_coordinates(page)
            page_text_data.append(text_instances)
            
            # Page info
            full_text = page.get_text()
            pages_data.append({
                'page_num': page_num + 1,
                'text': full_text,
                'word_count': len(full_text.split()) if full_text else 0,
                'image_size': img.size
            })
        
        doc.close()
        os.unlink(tmp_path)
        
        return pages_data, metadata, page_images, page_text_data
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return [], {}, [], []

def create_selectable_pdf_viewer(page_image, text_instances, page_num):
    """Create a PDF viewer with selectable text overlays."""
    
    # Convert image to base64
    img_buffer = io.BytesIO()
    page_image.save(img_buffer, format='PNG')
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    img_width, img_height = page_image.size
    
    # Generate unique component ID
    component_id = f"pdf_viewer_{page_num}_{int(time.time())}"
    
    # Build HTML with embedded JavaScript
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ 
                margin: 0; 
                padding: 20px; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #f8f9fa;
            }}
            
            .pdf-container {{
                position: relative;
                display: inline-block;
                background: white;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                overflow: hidden;
                margin: 0 auto;
                max-width: 100%;
            }}
            
            .pdf-image {{
                display: block;
                width: 100%;
                max-width: 900px;
                height: auto;
                user-select: none;
            }}
            
            .text-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: auto;
                z-index: 10;
            }}
            
            .text-element {{
                position: absolute;
                cursor: text;
                user-select: text;
                color: rgba(0,0,0,0.01);
                font-family: Arial, sans-serif;
                line-height: 1;
                white-space: nowrap;
                padding: 0;
                margin: 0;
                overflow: visible;
                border-radius: 2px;
                transition: background-color 0.2s ease;
            }}
            
            .text-element:hover {{
                background-color: rgba(0, 123, 255, 0.1);
            }}
            
            .text-element::selection {{
                background-color: rgba(255, 193, 7, 0.7);
                color: #000;
            }}
            
            .selection-popup {{
                position: fixed;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                z-index: 1000;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                border: 2px solid rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
                user-select: none;
            }}
            
            .selection-popup:hover {{
                transform: translateY(-2px) scale(1.05);
                box-shadow: 0 12px 40px rgba(0,0,0,0.4);
            }}
            
            .selection-popup:active {{
                transform: translateY(0) scale(0.98);
            }}
            
            .text-preview {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                border: 2px solid #28a745;
                border-radius: 12px;
                padding: 16px;
                max-width: 320px;
                box-shadow: 0 6px 24px rgba(0,0,0,0.15);
                z-index: 999;
                font-size: 13px;
                transform: translateX(100%);
                opacity: 0;
                transition: all 0.3s ease;
            }}
            
            .text-preview.show {{
                transform: translateX(0);
                opacity: 1;
            }}
            
            .preview-header {{
                font-weight: 600;
                color: #28a745;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .preview-content {{
                color: #333;
                line-height: 1.4;
                max-height: 100px;
                overflow-y: auto;
                word-wrap: break-word;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background: #f8f9fa;
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }}
            
            .instructions {{
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                border-radius: 12px;
                margin-bottom: 20px;
                border: 1px solid #2196f3;
            }}
            
            .instructions h3 {{
                margin: 0 0 10px 0;
                color: #1976d2;
                font-size: 18px;
            }}
            
            .instructions p {{
                margin: 5px 0;
                color: #424242;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="instructions">
            <h3>📖 Interactive Text Selection</h3>
            <p><strong>Click and drag</strong> to select mathematical text directly from the PDF</p>
            <p>A <strong>"🎬 Generate Video"</strong> popup will appear when you make a selection</p>
            <p><em>Tip: Press Escape to clear selection</em></p>
        </div>
        
        <div class="pdf-container">
            <img src="data:image/png;base64,{img_base64}" 
                 class="pdf-image" 
                 id="pdfImage"
                 draggable="false">
            
            <div class="text-overlay" id="textOverlay">
    """
    
    # Add text elements with precise positioning
    for i, text_instance in enumerate(text_instances[:200]):  # Limit for performance
        if not text_instance["text"].strip():
            continue
            
        x0, y0, x1, y1 = text_instance["bbox"]
        
        # Calculate percentage-based positioning
        left_pct = (x0 / img_width) * 100
        top_pct = (y0 / img_height) * 100
        width_pct = ((x1 - x0) / img_width) * 100
        height_pct = ((y1 - y0) / img_height) * 100
        
        # Estimate font size
        font_size = max(8, (y1 - y0) * 0.85)
        
        # Escape text for HTML
        text_content = text_instance["text"].replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        
        html_code += f"""
            <div class="text-element" 
                 style="left: {left_pct}%; top: {top_pct}%; 
                        width: {width_pct}%; height: {height_pct}%;
                        font-size: {font_size}px;"
                 data-text="{text_content}"
                 data-index="{i}">
                {text_content}
            </div>
        """
    
    # Add JavaScript functionality
    html_code += f"""
            </div>
        </div>
        
        <div class="text-preview" id="textPreview">
            <div class="preview-header">
                <span>✨ Selected Text</span>
                <span style="font-size: 11px; opacity: 0.7;" id="charCount"></span>
            </div>
            <div class="preview-content" id="previewContent"></div>
        </div>

        <script>
            let currentSelection = '';
            let selectionPopup = null;
            let textPreview = document.getElementById('textPreview');
            let isGenerating = false;

            function clearPopup() {{
                if (selectionPopup) {{
                    selectionPopup.remove();
                    selectionPopup = null;
                }}
            }}

            function hidePreview() {{
                textPreview.classList.remove('show');
            }}

            function showPreview(text) {{
                const previewContent = document.getElementById('previewContent');
                const charCount = document.getElementById('charCount');
                
                previewContent.textContent = text.substring(0, 300) + (text.length > 300 ? '...' : '');
                charCount.textContent = `${{text.length}} chars`;
                textPreview.classList.add('show');
                
                // Auto-hide after 8 seconds
                setTimeout(() => {{
                    hidePreview();
                }}, 8000);
            }}

            function handleTextSelection() {{
                setTimeout(() => {{
                    const selection = window.getSelection();
                    const selectedText = selection.toString().trim();
                    
                    clearPopup();
                    
                    if (selectedText.length > 3) {{
                        currentSelection = selectedText;
                        showSelectionPopup(selection);
                        showPreview(selectedText);
                    }} else {{
                        hidePreview();
                    }}
                }}, 50);
            }}

            function showSelectionPopup(selection) {{
                if (selection.rangeCount === 0) return;
                
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();
                
                selectionPopup = document.createElement('div');
                selectionPopup.className = 'selection-popup';
                selectionPopup.innerHTML = '🎬 Generate Video';
                
                // Position popup above selection
                const popupX = rect.left + (rect.width / 2) - 80;
                const popupY = rect.top - 60;
                
                selectionPopup.style.left = Math.max(20, Math.min(window.innerWidth - 160, popupX)) + 'px';
                selectionPopup.style.top = Math.max(20, popupY) + 'px';
                
                selectionPopup.onclick = function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (!isGenerating && currentSelection.length > 3) {{
                        generateVideo();
                    }}
                }};
                
                document.body.appendChild(selectionPopup);
            }}

            function generateVideo() {{
                if (isGenerating || currentSelection.length < 3) return;
                
                isGenerating = true;
                selectionPopup.innerHTML = '⏳ Processing...';
                selectionPopup.style.cursor = 'not-allowed';
                selectionPopup.style.opacity = '0.7';
                
                // Send data to Streamlit parent window
                const message = {{
                    type: 'GENERATE_VIDEO_REQUEST',
                    data: {{
                        text: currentSelection,
                        page: {page_num},
                        timestamp: Date.now(),
                        component_id: '{component_id}'
                    }}
                }};
                
                // Try multiple methods to communicate with Streamlit
                try {{
                    // Method 1: Post message to parent
                    if (window.parent && window.parent !== window) {{
                        window.parent.postMessage(message, '*');
                    }}
                    
                    // Method 2: Use Streamlit's sendMessage if available
                    if (window.parent && window.parent.sendMessageToStreamlit) {{
                        window.parent.sendMessageToStreamlit(message);
                    }}
                    
                    // Method 3: Store in sessionStorage for Streamlit to pick up
                    sessionStorage.setItem('pendingVideoGeneration', JSON.stringify(message.data));
                    
                    // Method 4: Dispatch custom event
                    const event = new CustomEvent('streamlitVideoRequest', {{
                        detail: message.data
                    }});
                    window.dispatchEvent(event);
                    
                    console.log('Video generation request sent:', message);
                    
                }} catch (error) {{
                    console.error('Error sending message:', error);
                }}
                
                // Clean up UI after delay
                setTimeout(() => {{
                    clearPopup();
                    hidePreview();
                    window.getSelection().removeAllRanges();
                    isGenerating = false;
                }}, 2000);
            }}

            // Event listeners
            document.addEventListener('mouseup', handleTextSelection);
            document.addEventListener('touchend', handleTextSelection);
            
            // Clear selection when clicking outside
            document.addEventListener('click', function(e) {{
                if (!e.target.closest('.text-overlay') && 
                    !e.target.closest('.selection-popup') && 
                    !e.target.closest('.text-preview')) {{
                    clearPopup();
                    hidePreview();
                }}
            }});
            
            // Keyboard shortcuts
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    clearPopup();
                    hidePreview();
                    window.getSelection().removeAllRanges();
                    currentSelection = '';
                    isGenerating = false;
                }}
                
                if ((e.ctrlKey || e.metaKey) && e.key === 'g' && currentSelection.length > 3) {{
                    e.preventDefault();
                    generateVideo();
                }}
            }});
            
            // Listen for messages from parent
            window.addEventListener('message', function(event) {{
                if (event.data && event.data.type === 'CLEAR_SELECTION') {{
                    clearPopup();
                    hidePreview();
                    window.getSelection().removeAllRanges();
                    currentSelection = '';
                    isGenerating = false;
                }}
            }});
            
            // Signal that component is ready
            console.log('PDF viewer component loaded successfully');
            console.log('Text elements count:', {len(text_instances[:200])});
            
            // Notify parent that component is ready
            try {{
                const readyMessage = {{
                    type: 'COMPONENT_READY',
                    component_id: '{component_id}',
                    page: {page_num}
                }};
                
                if (window.parent) {{
                    window.parent.postMessage(readyMessage, '*');
                }}
            }} catch (e) {{
                console.log('Could not notify parent of component ready state');
            }}
        </script>
    </body>
    </html>
    """
    
    return html_code

def process_selected_text_video(selected_text, page_num):
    """Process video generation from selected text."""
    
    if not selected_text or len(selected_text.strip()) < 3:
        st.warning("⚠️ Selected text is too short for video generation.")
        return False
    
    # Create progress container
    progress_container = st.empty()
    
    with progress_container.container():
        # Show processing state
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
            <h3>🎬 Generating Video from Your Selection</h3>
            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; 
                        padding: 1rem; margin: 1rem 0; font-family: monospace; 
                        font-size: 14px; max-height: 120px; overflow-y: auto;">
                "{selected_text[:400]}{'...' if len(selected_text) > 400 else ''}"
            </div>
            <p>🚀 Processing with GitHub AI and Manim...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize generator
            generator = MathVideoGenerator()
            
            # Progress updates
            status_text.text("🧠 AI analyzing your mathematical content...")
            progress_bar.progress(25)
            time.sleep(1)
            
            status_text.text("📝 Generating Manim animation code...")
            progress_bar.progress(50)
            time.sleep(1)
            
            status_text.text("🎬 Rendering video (this may take 2-4 minutes)...")
            progress_bar.progress(75)
            
            # Generate video
            video_path = generator.create_video(
                math_topic=selected_text,
                difficulty="intermediate",
                duration=60,
                quality="medium_quality"
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Video generation completed successfully!")
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
                    'method': 'direct_selection',
                    'word_count': len(selected_text.split()),
                    'char_count': len(selected_text)
                }
                st.session_state.generated_videos.append(video_info)
                
                # Success message
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                            border: 2px solid #28a745; border-radius: 15px; padding: 2rem; 
                            margin: 2rem 0; animation: slideInUp 0.6s ease-out;">
                    <h3>🎉 Video Generated Successfully!</h3>
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <div><strong>📄 Source:</strong> Page {page_num}</div>
                        <div><strong>📊 Words:</strong> {len(selected_text.split())}</div>
                        <div><strong>📏 Characters:</strong> {len(selected_text)}</div>
                        <div><strong>⏰ Time:</strong> {time.strftime('%H:%M:%S')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display video
                st.subheader("🎬 Your Generated Mathematical Video")
                
                try:
                    with open(video_path, 'rb') as video_file:
                        video_bytes = video_file.read()
                    
                    st.video(video_bytes)
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download Video",
                            data=video_bytes,
                            file_name=f"selected_math_video_p{page_num}_{int(time.time())}.mp4",
                            mime="video/mp4",
                            key=f"download_selected_{page_num}_{int(time.time())}"
                        )
                    
                    with col2:
                        if st.button("🔄 Generate Another", key=f"regenerate_{int(time.time())}"):
                            st.rerun()
                    
                    with col3:
                        file_size = os.path.getsize(video_path) / (1024 * 1024)
                        st.metric("📦 Size", f"{file_size:.1f} MB")
                    
                    with col4:
                        if st.button("📋 Show Details", key=f"details_{int(time.time())}"):
                            st.json(video_info)
                    
                    return True
                
                except Exception as e:
                    st.error(f"Error displaying video: {str(e)}")
                    return False
            
            else:
                st.error("❌ Failed to generate video. Please try again.")
                return False
        
        except Exception as e:
            st.error(f"❌ Error during video generation: {str(e)}")
            progress_container.empty()
            return False

def main():
    """Main application with direct selection functionality."""
    initialize_session_state()
    
    # Enhanced styling
    st.markdown("""
    <style>
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 2rem;
            font-weight: 300;
        }
        
        .stats-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e9ecef;
        }
        
        .feature-box {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 0 10px 10px 0;
            margin: 1rem 0;
        }
        
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-title">📚 Direct Selection PDF Video Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Select text directly • Generate videos instantly • No sidebar needed</p>', unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "📁 Upload Mathematical PDF Document",
        type=['pdf'],
        help="Choose textbooks, papers, problem sets, or any mathematical content"
    )
    
    if uploaded_file is not None:
        # Process PDF if needed
        if (st.session_state.pdf_document is None or 
            st.session_state.pdf_document != uploaded_file.name):
            
            with st.spinner("🔍 Processing PDF for direct text selection..."):
                pages_data, metadata, page_images, page_text_data = convert_pdf_with_text_overlay(uploaded_file)
                
                if pages_data:
                    st.session_state.pdf_pages = pages_data
                    st.session_state.pdf_metadata = metadata
                    st.session_state.page_images = page_images
                    st.session_state.page_text_blocks = page_text_data
                    st.session_state.pdf_document = uploaded_file.name
                    st.success(f"✅ PDF processed! Ready for direct text selection on {len(pages_data)} pages.")
                else:
                    st.error("❌ Failed to process PDF. Please try another file.")
                    return
        
        # Display metadata
        if st.session_state.pdf_metadata:
            metadata = st.session_state.pdf_metadata
            
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📄 Pages", metadata.get('page_count', 0))
            with col2:
                st.metric("📁 Size", f"{metadata.get('file_size', 0) / 1024:.1f} KB")
            with col3:
                st.metric("🎥 Videos", len(st.session_state.generated_videos))
            with col4:
                available = len([v for v in st.session_state.generated_videos if os.path.exists(v.get('path', ''))])
                st.metric("✅ Ready", available)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
        <div class="feature-box">
            <h4>🎯 Direct Text Selection Instructions:</h4>
            <ul style="margin: 0.5rem 0;">
                <li><strong>📖 Navigate:</strong> Use the page controls below to browse your PDF</li>
                <li><strong>🖱️ Select:</strong> Click and drag directly on the PDF to select any mathematical text</li>
                <li><strong>💫 Generate:</strong> Click the "🎬 Generate Video" popup that appears over your selection</li>
                <li><strong>⌨️ Shortcuts:</strong> Ctrl+G after selecting, or Escape to clear</li>
                <li><strong>📥 Download:</strong> Videos appear immediately with download buttons</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Page navigation
        if st.session_state.pdf_pages:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("⬅️ Previous Page", disabled=st.session_state.current_page <= 0):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col2:
                page_options = [f"Page {i+1} ({page['word_count']} words)" 
                              for i, page in enumerate(st.session_state.pdf_pages)]
                
                selected_page = st.selectbox(
                    "📖 Current Page:",
                    range(len(st.session_state.pdf_pages)),
                    index=st.session_state.current_page,
                    format_func=lambda x: page_options[x],
                    key="direct_page_selector"
                )
                
                if selected_page != st.session_state.current_page:
                    st.session_state.current_page = selected_page
                    st.rerun()
            
            with col3:
                if st.button("➡️ Next Page", disabled=st.session_state.current_page >= len(st.session_state.pdf_pages) - 1):
                    st.session_state.current_page += 1
                    st.rerun()
            
            # Display interactive PDF page
            if st.session_state.current_page < len(st.session_state.pdf_pages):
                page_info = st.session_state.pdf_pages[st.session_state.current_page]
                page_image = st.session_state.page_images[st.session_state.current_page]
                text_instances = st.session_state.page_text_blocks[st.session_state.current_page]
                
                st.subheader(f"📄 Page {page_info['page_num']} - Direct Text Selection")
                
                # Create and display the interactive viewer
                interactive_html = create_selectable_pdf_viewer(
                    page_image, 
                    text_instances, 
                    page_info['page_num']
                )
                
                # Display with sufficient height
                components.html(interactive_html, height=800, scrolling=True)
        
        # Check for pending video generation (from sessionStorage)
        check_generation_js = """
        <script>
        const pendingGeneration = sessionStorage.getItem('pendingVideoGeneration');
        if (pendingGeneration) {
            const data = JSON.parse(pendingGeneration);
            sessionStorage.removeItem('pendingVideoGeneration');
            
            // Send to Streamlit via custom event
            const event = new CustomEvent('streamlitGenerateVideo', {
                detail: data
            });
            window.parent.document.dispatchEvent(event);
        }
        </script>
        """
        components.html(check_generation_js, height=0)
        
        # Manual testing section
        st.divider()
        
        with st.expander("🧪 Manual Testing (Fallback Method)", expanded=False):
            st.write("If direct selection doesn't work, you can manually test the video generation:")
            
            test_text = st.text_area(
                "Enter mathematical content:",
                placeholder="Type mathematical content here for testing...",
                height=80,
                key="manual_testing_input"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎬 Generate Test Video", type="primary", key="manual_test") and test_text:
                    success = process_selected_text_video(test_text, st.session_state.current_page + 1)
                    if success:
                        st.balloons()
            
            with col2:
                if st.button("🔄 Clear Test Input", key="clear_test"):
                    st.rerun()
        
        # Video gallery
        if st.session_state.generated_videos:
            st.divider()
            st.header("🎬 Generated Videos Gallery")
            
            # Sort by newest first
            sorted_videos = sorted(st.session_state.generated_videos, key=lambda x: x['timestamp'], reverse=True)
            
            for i, video_info in enumerate(sorted_videos):
                with st.expander(
                    f"🎥 Video {i+1} | Page {video_info['page']} | {video_info['topic'][:60]}...", 
                    expanded=(i == 0)
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**📄 Source:** Page {video_info['page']} ({video_info.get('method', 'unknown')})")
                        st.write(f"**📝 Content:** {video_info.get('full_text', video_info['topic'])[:250]}{'...' if len(video_info.get('full_text', '')) > 250 else ''}")
                        st.write(f"**📊 Stats:** {video_info.get('word_count', 'N/A')} words, {video_info.get('char_count', 'N/A')} characters")
                        st.write(f"**⏰ Generated:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(video_info['timestamp']))}")
                        
                        # Video display
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
                        # Video stats
                        if os.path.exists(video_info['path']):
                            file_size = os.path.getsize(video_info['path']) / (1024 * 1024)
                            st.metric("📦 Size", f"{file_size:.1f} MB")
                            
                            # Download button
                            with open(video_info['path'], 'rb') as video_file:
                                st.download_button(
                                    label="📥 Download",
                                    data=video_file.read(),
                                    file_name=f"direct_selection_video_p{video_info['page']}_{i+1}.mp4",
                                    mime="video/mp4",
                                    key=f"direct_download_{i}",
                                    use_container_width=True
                                )
    
    else:
        # Upload prompt
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; 
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    border-radius: 20px; margin: 2rem 0; 
                    border: 3px dashed #667eea;">
            <h2 style="color: #667eea; margin-bottom: 1rem;">📁 Upload PDF for Direct Text Selection</h2>
            <p style="font-size: 1.4rem; color: #666; margin: 1.5rem 0; font-weight: 300;">
                Experience revolutionary PDF interaction
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                        gap: 1.5rem; margin: 2.5rem 0;">
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">🖱️ Direct Selection</h4>
                    <p style="color: #666; font-size: 0.95rem;">Click and drag text directly on PDF pages</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">💫 Floating UI</h4>
                    <p style="color: #666; font-size: 0.95rem;">Contextual popup menus appear on selection</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">⚡ Instant Videos</h4>
                    <p style="color: #666; font-size: 0.95rem;">Generate mathematical animations immediately</p>
                </div>
            </div>
            <p style="color: #888; font-style: italic; margin-top: 2rem;">
                Upload any mathematical PDF and start selecting text directly from the pages!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">
            🚀 Direct Selection PDF Video Generator
        </p>
        <p style="font-size: 0.95rem;">
            Revolutionary PDF Experience • Direct Text Selection • Floating Actions • Instant Generation
        </p>
        <p style="font-size: 0.85rem; color: #888; margin-top: 1rem;">
            Powered by GitHub AI • Manim • Advanced JavaScript • PyMuPDF
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
