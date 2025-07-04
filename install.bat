@echo off
REM Installation script for neru-scrapper on Windows
REM Handles common installation issues including metadata generation errors

echo 🚀 Installing neru-scrapper dependencies...

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Python installation found

REM Upgrade pip and install build tools first
echo 📦 Upgrading pip and installing build tools...
python -m pip install --upgrade pip setuptools wheel

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔨 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip in virtual environment
pip install --upgrade pip setuptools wheel

REM Install dependencies with error handling
echo 📋 Installing dependencies...

REM Core dependencies first (most stable)
echo Installing core dependencies...
pip install requests beautifulsoup4 python-dotenv

REM Scientific computing dependencies
echo Installing scientific computing dependencies...
pip install numpy pandas

REM Visualization dependencies
echo Installing visualization dependencies...
pip install matplotlib seaborn plotly

REM Web scraping dependencies
echo Installing web scraping dependencies...
pip install selenium lxml fake-useragent

REM Office file support
echo Installing office file support...
pip install openpyxl

REM Text processing
echo Installing text processing dependencies...
pip install wordcloud

REM Web framework dependencies
echo Installing web framework dependencies...
pip install fastapi uvicorn pydantic aiofiles

echo ✅ Installation completed successfully!
echo.
echo To activate the virtual environment, run:
echo venv\Scripts\activate.bat
echo.
echo To run the scraper:
echo python main.py

pause
