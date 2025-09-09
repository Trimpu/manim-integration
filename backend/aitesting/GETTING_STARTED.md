# Getting Started - Math Video Generator

## Quick Setup (5 minutes)

### Step 1: Get GitHub Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `read:user` (GitHub Models access)
4. Copy the generated token

### Step 2: Create .env File
1. Copy `.env.template` to `.env`:
   ```
   copy .env.template .env
   ```
2. Edit `.env` and replace `your_github_token_here` with your actual token:
   ```
   GITHUB_TOKEN=ghp_your_actual_token_here
   ```

### Step 3: Test Setup
```powershell
D:\VSCODE\aitesting\.venv\Scripts\python.exe test_setup.py
```

You should see: "🎉 All tests passed! Your setup is ready."

### Step 4: Generate Your First Video
```powershell
D:\VSCODE\aitesting\.venv\Scripts\python.exe quick_demo.py
```

This will generate a demo video about "Linear Functions and Slope"

### Step 5: Use the Full Application
```powershell
D:\VSCODE\aitesting\.venv\Scripts\python.exe math_video_generator.py
```

Or simply double-click: `run_generator.bat`

## Next Steps

- Try different math topics in the interactive application
- Adjust difficulty levels (beginner/intermediate/advanced)
- Experiment with different video qualities
- Check the generated videos in the `math_videos/` folder

## Troubleshooting

### "FFmpeg not found" error
Install FFmpeg:
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### "Permission denied" errors
Try running PowerShell as Administrator

### Generated video not found
Check the `math_videos/media/videos/` directory for output files

## What's Included

✅ **AI-Powered Code Generation** - Uses GitHub Models (GPT-4o)  
✅ **Professional Animations** - Manim mathematical visualizations  
✅ **Interactive Interface** - Easy topic selection and difficulty control  
✅ **Batch Processing** - Generate multiple videos at once  
✅ **Educational Focus** - Step-by-step mathematical explanations  

Ready to create amazing math videos! 🎬📚
