# Manim Integration - AI-Powered Mathematical PDF Viewer

An advanced React-based PDF viewer with integrated AI-powered mathematical visualization using Manim (Mathematical Animation Engine). This project enables users to select mathematical content from PDFs and generate educational video explanations.

## 🚀 Features

- **Interactive PDF Viewer**: Built with React and react-pdf for seamless document viewing
- **Text Selection with Spacing Fix**: Improved text extraction that properly handles word spacing
- **AI-Powered Video Generation**: Uses GitHub AI Models (GPT-4o) to create mathematical explanations
- **Manim Integration**: Generates educational mathematical animations automatically
- **Floating Action Buttons**: Context-sensitive UI for selected text
- **Real-time Progress Tracking**: Live updates during video generation
- **Quality Control**: Multiple difficulty levels and video quality options

## 🛠️ Tech Stack

### Frontend
- **React 18.2.0**: Modern React with hooks and functional components
- **TailwindCSS 3.4.1**: Utility-first CSS framework for styling
- **react-pdf 7.7.1**: PDF rendering and interaction
- **pdfjs-dist 3.11.174**: Core PDF processing engine

### Backend
- **Flask 3.1.2**: Lightweight Python web framework
- **Manim 0.19.0**: Mathematical Animation Engine
- **OpenAI API**: Integration with GitHub AI Models
- **Python 3.13.7**: Modern Python runtime

## 📁 Project Structure

```
manim-integration/
├── src/                          # React frontend source
│   ├── components/
│   │   ├── PdfViewer.jsx         # Main PDF viewer component
│   │   ├── FloatingButton.jsx    # Selection action buttons
│   │   ├── VideoPlayer.jsx       # Video modal component
│   │   ├── LoadingModal.jsx      # Progress tracking UI
│   │   └── ExplanationViewer.jsx # Alternative content display
│   ├── services/
│   │   └── api.js                # Backend API communication
│   └── styles/                   # TailwindCSS styles
├── backend/
│   └── aitesting/
│       ├── flask_app.py          # Main Flask application
│       ├── math_video_generator.py # AI + Manim integration
│       ├── math_videos/          # Generated Manim scenes
│       └── media/                # Output videos (ignored)
├── public/                       # Static assets
└── docs/                         # Documentation
```

## 🚦 Getting Started

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (3.10 or higher)
- **FFmpeg** (for Manim video rendering)
- **GitHub AI Models API Token**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Trimpu/manim-integration.git
   cd manim-integration
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Set up Python environment**
   ```bash
   cd backend/aitesting
   pip install flask flask-cors openai manim python-dotenv
   ```

4. **Configure environment variables**
   
   Create `backend/aitesting/.env`:
   ```env
   GITHUB_TOKEN=your_github_ai_models_token_here
   ```

5. **Install FFmpeg** (Required for Manim)
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend/aitesting
   python flask_app.py
   ```
   Server runs on: `http://localhost:5000`

2. **Start the frontend development server**
   ```bash
   npm start
   ```
   Application runs on: `http://localhost:3000`

## 🎯 Usage

1. **Upload a PDF**: Use the file input to load a mathematical document
2. **Select Text**: Highlight mathematical content in the PDF
3. **Generate Video**: Click "Visualize" on the floating button
4. **Choose Settings**: Select difficulty level and video quality
5. **Watch Progress**: Monitor real-time generation status
6. **View Results**: Watch the generated educational video

## 🔧 Configuration

### Difficulty Levels
- **Beginner**: Basic explanations with simple visuals
- **Intermediate**: Standard mathematical depth
- **Advanced**: Complex derivations and detailed analysis

### Video Quality Options
- **Low Quality**: 480p, faster generation
- **Medium Quality**: 720p, balanced performance
- **High Quality**: 1080p, best visual fidelity

## 🐛 Troubleshooting

### Common Issues

1. **Text Selection Without Spaces**
   - Fixed with regex-based text processing
   - Automatic word boundary detection

2. **Manim Rendering Failures**
   - Ensure FFmpeg is properly installed
   - Check MiKTeX/LaTeX installation for mathematical notation
   - Verify Python dependencies

3. **API Token Issues**
   - Verify GitHub AI Models token in `.env`
   - Check token permissions and usage limits

### Debug Mode

The Flask server includes comprehensive error logging:
```python
# Disable debug mode in production
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Manim Community** for the excellent mathematical animation engine
- **GitHub AI Models** for providing GPT-4o integration
- **React PDF** team for robust PDF handling
- **TailwindCSS** for the utility-first styling approach

## 🔗 Related Projects

- [Manim Community Edition](https://github.com/ManimCommunity/manim)
- [React PDF](https://github.com/wojtekmaj/react-pdf)
- [GitHub AI Models](https://docs.github.com/en/copilot/github-copilot-chat)

---

Built with ❤️ for mathematical education and visualization.
