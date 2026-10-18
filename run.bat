@echo off
echo ================================================
echo  Intelligent Market Research Assistant
echo  Powered by IBM Granite + IBM WatsonX
echo ================================================
echo.

:: Install dependencies
echo [1/3] Installing Python dependencies...
pip install -r requirements.txt --quiet

echo [2/3] Starting Flask backend server...
echo.

:: Start the Flask app
python app.py
