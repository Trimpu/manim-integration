@echo off
echo 🎬 Starting AI Math Video Backend...
echo.

cd backend/aitesting

echo Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo Checking if .env file exists...
if not exist .env (
    echo ❌ .env file not found!
    echo Please copy .env.template to .env and add your GitHub token
    echo.
    echo Opening setup instructions...
    start "" "../../INTEGRATION_GUIDE.md"
    pause
    exit /b 1
)

echo ✅ Environment file found
echo.

echo Installing Python dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install dependencies
    echo Trying alternative pip installation...
    py -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ pip installation failed. Please install pip manually
        echo Try: python -m ensurepip --upgrade
        pause
        exit /b 1
    )
)

echo.
echo 🚀 Starting Flask server on http://localhost:5000
echo.
echo Backend API endpoints:
echo   - POST /api/generate - Generate math videos
echo   - GET /api/status/^<task_id^> - Check progress
echo   - GET /api/setup - Check configuration
echo.
echo Keep this window open while using the PDF viewer
echo.

python flask_app.py
