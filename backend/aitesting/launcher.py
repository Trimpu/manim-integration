"""
Frontend Launcher - Choose Your Interface
Select between different frontend options for the Math Video Generator
"""

import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Math Video Generator - Launcher",
    page_icon="🚀",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
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
        margin-bottom: 3rem;
    }
    
    .app-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .feature-list {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .feature-list ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .feature-list li {
        margin: 0.3rem 0;
        color: #495057;
    }
    
    .launch-button {
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .recommended-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main launcher interface."""
    
    # Header
    st.markdown('<h1 class="main-title">🚀 Math Video Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose your preferred interface to start creating mathematical videos</p>', unsafe_allow_html=True)
    
    # Interface options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="app-card">
            <h3>📚 PDF Video Generator <span class="recommended-badge">RECOMMENDED</span></h3>
            <p><strong>Perfect for your use case!</strong></p>
            <p>Upload PDF documents, select mathematical content, and generate instant video explanations.</p>
            
            <div class="feature-list">
                <h5>✨ Features:</h5>
                <ul>
                    <li>📄 PDF viewer with text extraction</li>
                    <li>🔍 Interactive text selection</li>
                    <li>🤖 AI-powered video generation</li>
                    <li>📊 Document analysis</li>
                    <li>🎬 Video gallery</li>
                    <li>📥 Download videos</li>
                </ul>
            </div>
            
            <p><strong>Best for:</strong> Students, teachers, researchers working with PDF documents</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch PDF Video Generator", key="pdf_app", use_container_width=True):
            st.success("🎉 Launching PDF Video Generator...")
            st.markdown("""
            **Run this command in your terminal:**
            ```bash
            streamlit run advanced_pdf_app.py
            ```
            """)
            st.info("The advanced PDF interface will open in a new browser tab!")
    
    with col2:
        st.markdown("""
        <div class="app-card">
            <h3>🎬 Simple Video Generator</h3>
            <p>Clean, straightforward interface for direct video generation.</p>
            
            <div class="feature-list">
                <h5>✨ Features:</h5>
                <ul>
                    <li>📝 Direct text input</li>
                    <li>⚙️ Video customization</li>
                    <li>🎥 Quality settings</li>
                    <li>📊 Progress tracking</li>
                    <li>💾 Easy downloads</li>
                </ul>
            </div>
            
            <p><strong>Best for:</strong> Quick video generation without PDF processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Simple Generator", key="simple_app", use_container_width=True):
            st.success("🎉 Launching Simple Video Generator...")
            st.markdown("""
            **Run this command in your terminal:**
            ```bash
            streamlit run streamlit_app.py
            ```
            """)
            st.info("The simple interface will open in a new browser tab!")
    
    # Alternative methods
    st.divider()
    
    st.markdown("""
    ### 🛠️ Alternative Methods
    
    If you prefer command-line interfaces:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📋 Interactive CLI**
        ```bash
        python math_video_generator.py
        ```
        Menu-driven interface with options
        """)
    
    with col2:
        st.markdown("""
        **📝 Direct Input**
        ```bash
        python direct_prompt.py
        ```
        Modify code and run directly
        """)
    
    with col3:
        st.markdown("""
        **📖 Multi-line Input**
        ```bash
        python multiline_prompt.py
        ```
        Handle long, complex prompts
        """)
    
    # Quick start guide
    st.divider()
    
    with st.expander("📖 Quick Start Guide", expanded=False):
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Ensure Setup is Complete:**
           - ✅ GitHub token configured in `.env` file
           - ✅ Dependencies installed (`manim`, `openai`, etc.)
           - ✅ FFmpeg installed for video rendering
        
        2. **Choose Your Interface:**
           - **PDF Generator**: For working with PDF documents
           - **Simple Generator**: For direct text input
        
        3. **Create Your First Video:**
           - Enter or select mathematical content
           - Choose difficulty and settings
           - Click generate and wait 2-5 minutes
           - Download your professional video!
        
        ### 🎯 Tips for Best Results:
        
        - **Clear Content**: Use well-formatted mathematical problems
        - **Appropriate Length**: 1-3 paragraphs work best
        - **Specific Topics**: Focus on single concepts
        - **Quality vs Speed**: Higher quality = longer rendering time
        
        ### 🔧 Troubleshooting:
        
        - **Token Issues**: Check your `.env` file has correct GitHub token
        - **Long Filenames**: App automatically shortens them
        - **Rendering Fails**: Try lower quality or simpler content
        - **PDF Issues**: Ensure PDF has selectable text
        """)
    
    # Current status
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #e8f5e8; border-radius: 8px;">
            <h4 style="color: #28a745; margin: 0;">✅ System Status</h4>
            <p style="margin: 0.5rem 0;">All systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Check if files exist
        pdf_app_exists = os.path.exists("advanced_pdf_app.py")
        simple_app_exists = os.path.exists("streamlit_app.py")
        
        status_color = "#28a745" if pdf_app_exists and simple_app_exists else "#ffc107"
        status_text = "Ready" if pdf_app_exists and simple_app_exists else "Partial"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: #e3f2fd; border-radius: 8px;">
            <h4 style="color: {status_color}; margin: 0;">📱 Apps Available</h4>
            <p style="margin: 0.5rem 0;">{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fff3e0; border-radius: 8px;">
            <h4 style="color: #ff9800; margin: 0;">🎥 Ready to Create</h4>
            <p style="margin: 0.5rem 0;">Choose interface above</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #666;">
        <p>🎓 <strong>Math Video Generator</strong> - Transforming Mathematical Education</p>
        <p>Powered by GitHub AI + Manim + Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
