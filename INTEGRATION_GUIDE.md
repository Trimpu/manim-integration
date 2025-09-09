# 🎬 React PDF Viewer with AI Mathematical Visualization

Your React PDF viewer is now integrated with AI-powered mathematical visualization! Here's how to get everything running:

## 🚀 Quick Setup

### 1. **Backend Setup**
```bash
# Navigate to backend directory
cd backend/aitesting

# Install Python dependencies
pip install -r requirements.txt

# Setup environment variables
# Copy the .env template and add your GitHub token
copy .env.template .env
# Edit .env file and add your GitHub Personal Access Token

# Start the Flask backend
python flask_app.py
```

### 2. **Frontend Setup** (if not done already)
```bash
# Install React dependencies
npm install

# Start React development server
npm start
```

## 🎯 How It Works

1. **📄 Load a PDF** - Click "Open PDF" to select a mathematical textbook/document
2. **✏️ Select Text** - Highlight any mathematical problem or concept
3. **✨ Generate Video** - Click the floating "Visualize" button that appears
4. **⚙️ Customize** - Use the settings button for difficulty/quality options
5. **🎬 Watch & Learn** - AI generates a personalized math animation video!

## 🔧 Features

### Frontend (React)
- ✅ **PDF Viewer** with continuous scrolling
- ✅ **Text Selection** with floating action buttons
- ✅ **Video Generation** with progress tracking
- ✅ **Video Player** modal for viewing results
- ✅ **Backend Status** indicator in toolbar
- ✅ **Responsive Design** with TailwindCSS

### Backend (Flask + AI)
- ✅ **GitHub AI Models** integration (GPT-4o)
- ✅ **Manim** mathematical animation engine
- ✅ **Async Video Generation** with progress tracking
- ✅ **RESTful API** for frontend communication
- ✅ **Video Quality Options** (Low/Medium/High)
- ✅ **Difficulty Levels** (Beginner/Intermediate/Advanced)

## 📋 API Endpoints

- `POST /api/generate` - Start video generation
- `GET /api/status/{task_id}` - Check generation progress
- `GET /api/download/{video_path}` - Download generated video
- `GET /api/setup` - Check backend configuration
- `GET /api/videos` - List all generated videos

## ⚠️ Prerequisites

1. **Python 3.8+** installed
2. **Node.js & npm** installed
3. **FFmpeg** installed (for video rendering)
4. **GitHub Personal Access Token** with AI Models access

## 🔑 GitHub Token Setup

1. Go to https://github.com/settings/tokens
2. Create a new Personal Access Token
3. Give it access to GitHub AI Models
4. Copy the token to your `.env` file

## 🎮 Usage Tips

- **Mathematical Content**: Works best with algebra, calculus, geometry problems
- **Text Selection**: Select complete mathematical expressions for best results
- **Video Quality**: Choose "Low" for quick previews, "High" for final videos
- **Difficulty**: Match the level to your target audience

## 🛠️ Troubleshooting

### Backend Issues
- **"Backend Offline"**: Make sure Flask server is running on port 5000
- **"Config Error"**: Check your GitHub token in the `.env` file
- **Video Generation Fails**: Ensure FFmpeg is properly installed

### Frontend Issues
- **Button Not Appearing**: Check browser console for JavaScript errors
- **CORS Issues**: Make sure Flask-CORS is installed and configured

## 📁 Project Structure

```
/
├── src/                          # React Frontend
│   ├── components/
│   │   ├── PdfViewer.jsx        # Main PDF viewer with AI integration
│   │   ├── FloatingButton.jsx   # Text selection popup
│   │   ├── VideoPlayer.jsx      # Video display modal
│   │   ├── LoadingModal.jsx     # Generation progress
│   │   └── Toolbar.jsx          # Controls & status
│   └── services/
│       └── api.js               # Backend API communication
├── backend/                     # Python Flask Backend
│   └── aitesting/
│       ├── flask_app.py         # Main API server
│       ├── math_video_generator.py # AI video generation
│       └── requirements.txt     # Python dependencies
└── README.md                    # This file
```

Your AI-powered PDF viewer is ready to transform mathematical learning! 🎓✨
