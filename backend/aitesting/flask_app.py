"""
Flask Web API for Math Video Generator
RESTful API backend for the math video generator.
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import json
from pathlib import Path
import threading
import time
# Try to import the full video generator, fall back to simple generator
try:
    from math_video_generator import MathVideoGenerator
    print("Using full video generator with Manim")
except ImportError:
    print("Manim not available - video generation will not work")
    MathVideoGenerator = None

app = Flask(__name__)
CORS(app)

# Global variables for tracking generation status
generation_status = {}

def generate_video_async(task_id, topic, difficulty, duration, quality):
    """Generate video asynchronously and update status."""
    try:
        generation_status[task_id] = {"status": "generating", "progress": 0, "message": "Initializing..."}
        
        if MathVideoGenerator is None:
            generation_status[task_id] = {
                "status": "failed", 
                "progress": 0, 
                "message": "Video generation not available - Manim not installed"
            }
            return
        
        generator = MathVideoGenerator()
        generation_status[task_id] = {"status": "generating", "progress": 20, "message": "Generating Manim code..."}
        
        video_path = generator.create_video(topic, difficulty, duration, quality)
        
        if video_path:
            generation_status[task_id] = {
                "status": "completed", 
                "progress": 100, 
                "message": "Video generated successfully!",
                "video_path": video_path,
                "content_type": "video"
            }
        else:
            generation_status[task_id] = {
                "status": "failed", 
                "progress": 0, 
                "message": "Failed to generate video"
            }
            
    except Exception as e:
        print(f"Error in video generation: {str(e)}")
        import traceback
        traceback.print_exc()
        generation_status[task_id] = {
            "status": "failed", 
            "progress": 0, 
            "message": f"Error: {str(e)}"
        }

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_video():
    """API endpoint to start video generation."""
    try:
        data = request.json
        topic = data.get('topic', '').strip()
        difficulty = data.get('difficulty', 'intermediate')
        duration = int(data.get('duration', 45))
        quality = data.get('quality', 'medium_quality')
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        # Generate unique task ID
        task_id = f"task_{int(time.time())}"
        
        # Start generation in background
        thread = threading.Thread(
            target=generate_video_async, 
            args=(task_id, topic, difficulty, duration, quality)
        )
        thread.start()
        
        return jsonify({"task_id": task_id, "status": "started"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status/<task_id>')
def get_status(task_id):
    """Get the status of a generation task."""
    status = generation_status.get(task_id, {"status": "not_found", "message": "Task not found"})
    return jsonify(status)

@app.route('/api/videos')
def list_videos():
    """List all generated videos."""
    videos = []
    media_path = Path("media/videos")
    
    if media_path.exists():
        for folder in media_path.iterdir():
            if folder.is_dir():
                for quality_folder in folder.iterdir():
                    if quality_folder.is_dir():
                        video_files = list(quality_folder.glob("*.mp4"))
                        if video_files:
                            video = video_files[0]
                            videos.append({
                                "name": folder.name.replace("_", " ").title(),
                                "path": str(video),
                                "size": video.stat().st_size,
                                "created": video.stat().st_mtime
                            })
    
    return jsonify(videos)

@app.route('/api/download/<path:file_path>')
def download_file(file_path):
    """Download a generated file (video or explanation)."""
    try:
        file_path = Path(file_path)
        if file_path.exists():
            if file_path.suffix == '.mp4':
                return send_file(file_path, as_attachment=True)
            elif file_path.suffix == '.json':
                # For JSON explanation files, return the content
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return jsonify(data)
            else:
                return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/setup')
def check_setup():
    """Check if the application is properly configured."""
    try:
        # Check environment
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return jsonify({"status": "error", "message": "GITHUB_TOKEN not configured"})
        
        # Test generator initialization
        MathVideoGenerator()
        
        return jsonify({"status": "ok", "message": "Setup complete"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Run without debug mode to prevent auto-reload issues during video generation
    app.run(debug=False, host='0.0.0.0', port=5000)
