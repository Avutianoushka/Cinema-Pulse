@echo off
REM =============================================================================
REM CinemaPulse - Local Development Runner (Windows)
REM =============================================================================
REM Usage: Double-click or run: run_local.bat
REM =============================================================================
echo ==========================================
echo 🎬 CinemaPulse - Local Development
echo ==========================================
REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)
echo ✅ Python found
REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)
REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
REM Install dependencies
echo 📥 Installing dependencies...
pip install flask --quiet
echo.
echo ==========================================
echo 🚀 Starting CinemaPulse...
echo ==========================================
echo.
echo 🌐 Open in browser: http://127.0.0.1:5000
echo 🛑 Press CTRL+C to stop
echo.
echo ==========================================
python app.py
pause
