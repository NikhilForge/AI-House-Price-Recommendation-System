@echo off
REM ==================================
REM House Price Predictor - Quick Start
REM ==================================

echo ============================================
echo 🏠 House Price Predictor - Quick Start
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python 3 detected
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate
echo ✅ Virtual environment activated
echo.

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt --quiet
echo ✅ Dependencies installed
echo.

REM Create directories if they don't exist
echo 📁 Setting up directories...
if not exist "saved_models" mkdir saved_models
if not exist "templates" mkdir templates
if not exist "static" mkdir static
echo ✅ Directories created
echo.

REM Check for model files
echo 🔍 Checking for model files...

set MODEL_FOUND=0
set FEATURES_FOUND=0

if exist "saved_models\best_model.pkl" set MODEL_FOUND=1
if exist "best_model.pkl" set MODEL_FOUND=1

if exist "saved_models\feature_names.pkl" set FEATURES_FOUND=1
if exist "feature_names.pkl" set FEATURES_FOUND=1
if exist "feature_names.txt" set FEATURES_FOUND=1

if %MODEL_FOUND%==1 (
    echo ✅ Model file found
) else (
    echo ⚠️  Model file not found ^(best_model.pkl^)
)

if %FEATURES_FOUND%==1 (
    echo ✅ Feature names file found
) else (
    echo ⚠️  Feature names file not found
)

if exist "saved_models\scaler.pkl" (
    echo ✅ Scaler file found
) else if exist "scaler.pkl" (
    echo ✅ Scaler file found
) else (
    echo ℹ️  Scaler file not found ^(optional^)
)

echo.

REM Start server
if %MODEL_FOUND%==1 if %FEATURES_FOUND%==1 (
    echo ============================================
    echo 🚀 Starting server...
    echo ============================================
    echo.
    echo 📡 Server will be available at:
    echo    🌐 Web App: http://127.0.0.1:8000
    echo    📚 API Docs: http://127.0.0.1:8000/docs
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo ============================================
    echo ⚠️  SETUP REQUIRED
    echo ============================================
    echo.
    echo Please add the following files before running:
    
    if %MODEL_FOUND%==0 echo    • best_model.pkl ^(trained ML model^)
    if %FEATURES_FOUND%==0 echo    • feature_names.pkl or feature_names.txt
    
    echo.
    echo Place them in the 'saved_models\' directory or in the root directory.
    echo.
    echo Once files are added, run this script again:
    echo    start.bat
    echo.
    pause
)
