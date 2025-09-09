# AI-Powered Mathematical PDF Viewer

A sophisticated React-based PDF viewer with AI-powered mathematical visualization capabilities. This application allows users to select mathematical text from PDFs and generate educational videos or explanations using Manim and OpenAI's API.

## 🚀 Features

### Frontend (React + TailwindCSS)
- **PDF Viewing**: High-quality PDF rendering with react-pdf
- **Text Selection**: Intelligent text selection with automatic spacing correction
- **Floating UI**: Dynamic floating buttons that appear on text selection
- **Video Player**: Built-in video player for generated mathematical animations
- **Loading States**: Comprehensive progress tracking with real-time updates
- **Responsive Design**: Mobile-friendly interface with TailwindCSS

### Backend (Flask + Manim + AI)
- **AI Integration**: OpenAI GPT-4 and GitHub AI Models for content generation
- **Video Generation**: Manim-powered mathematical animations
- **RESTful API**: Clean API endpoints for video generation and status tracking
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Error Handling**: Robust error handling with detailed logging

## 📁 Project Structure

```
├── src/                          # React frontend
│   ├── components/
│   │   ├── PdfViewer.jsx        # Main PDF viewer component
│   │   ├── FloatingButton.jsx   # Selection UI component
│   │   ├── VideoPlayer.jsx      # Video playback modal
│   │   ├── LoadingModal.jsx     # Progress tracking modal
│   │   └── ExplanationViewer.jsx # Text explanation viewer
│   └── services/
│       └── api.js               # Backend API service
├── backend/aitesting/           # Flask backend
│   ├── flask_app.py            # Main Flask application
│   ├── math_video_generator.py # Manim video generation
│   ├── math_videos/            # Generated Manim scenes
│   └── media/                  # Generated video files
├── public/                     # Static assets
└── package.json               # Node.js dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- FFmpeg (for video processing)
- MiKTeX or TeX Live (for mathematical notation)

### Frontend Setup
```bash
npm install
npm start
```
The React app will start on `http://localhost:3000`

### Backend Setup
```bash
cd backend/aitesting
pip install -r requirements.txt

# Create .env file with your API keys
echo "OPENAI_API_KEY=your_openai_key" > .env
echo "GITHUB_TOKEN=your_github_token" >> .env

python flask_app.py
```
The Flask server will start on `http://localhost:5000`

### Quick Start Script
Use the provided batch file for easy startup:
```bash
./start-backend.bat
```

## 🎯 Usage

1. **Load PDF**: Upload a mathematical PDF document
2. **Select Text**: Highlight mathematical problems or concepts
3. **Generate Content**: Click the "Visualize" button that appears
4. **Choose Options**: Select difficulty level and video quality
5. **Watch & Learn**: View the generated mathematical animation

## 🔧 API Endpoints

- `POST /api/generate` - Generate mathematical video/explanation
- `GET /api/status/{task_id}` - Check generation progress
- `GET /api/videos` - List all generated videos
- `GET /api/setup` - Get backend configuration

## 🎨 Key Components

### PdfViewer.jsx
- Handles PDF rendering and text selection
- Manages floating button positioning
- Integrates with backend API for content generation
- Implements text spacing corrections for better readability

### MathVideoGenerator.py
- Generates Manim code using AI models
- Renders mathematical animations
- Handles video quality settings
- Provides error handling and logging

### FloatingButton.jsx
- Displays interactive selection UI
- Offers difficulty and quality options
- Manages user preferences
- Provides visual feedback

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
```

### Video Quality Settings
- **Low Quality**: 480p, faster generation
- **Medium Quality**: 720p, balanced performance
- **High Quality**: 1080p, best visual quality

### Difficulty Levels
- **Beginner**: Basic explanations with simple animations
- **Intermediate**: Moderate complexity with detailed steps
- **Advanced**: Complex mathematical concepts with full derivations

## 🚀 Recent Improvements

- Fixed text selection spacing issues in PDFs
- Improved Manim code generation with better error handling
- Enhanced video generation reliability
- Added comprehensive progress tracking
- Implemented fallback systems for robust operation
- Updated UI with better loading states and user feedback

## 🧪 Development

### Running Tests
```bash
npm test                    # Frontend tests
python -m pytest          # Backend tests
```

### Building for Production
```bash
npm run build              # Build React app
```

### Code Quality
- ESLint for JavaScript linting
- Prettier for code formatting
- Python Black for backend formatting

## 📚 Dependencies

### Frontend
- React 18.2.0
- react-pdf 7.7.1
- TailwindCSS 3.4.1
- Axios for API calls

### Backend
- Flask 3.1.2
- Manim 0.19.0
- OpenAI Python SDK
- CORS support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Repository**: [https://github.com/Trimpu/manim-integration](https://github.com/Trimpu/manim-integration)
- **Demo**: Available on request
- **Documentation**: See individual component files for detailed documentation

## 🆘 Support

For support, please open an issue on the GitHub repository or contact the development team.

---

Built with ❤️ using React, Flask, Manim, and AI technologies.
