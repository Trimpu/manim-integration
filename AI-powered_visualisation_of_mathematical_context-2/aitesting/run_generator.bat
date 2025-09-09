@echo off
echo Math Video Generator - Easy Launch
echo ================================

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file with your GitHub token:
    echo GITHUB_TOKEN=your_github_token_here
    echo.
    echo Get your token from: https://github.com/settings/tokens
    pause
    exit /b 1
)

REM Run the main application
echo Starting Math Video Generator...
echo.
D:\VSCODE\aitesting\.venv\Scripts\python.exe math_video_generator.py

pause
