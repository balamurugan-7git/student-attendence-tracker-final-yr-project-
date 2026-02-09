@echo off
echo ==============================================
echo Online Examination System - Automated Tester
echo ==============================================

echo [1/4] Installing dependencies...
python -m pip install flask requests

echo [2/4] Initializing Database...
python db_setup.py

echo [3/4] Seeding Test Data...
python seed_data.py

echo [4/4] Starting Server and Running Integration Tests...
echo (Note: Starting server in background...)
start /b python app.py

timeout /t 5

echo Running tests...
python automated_test.py

echo ==============================================
echo Verification Complete.
echo ==============================================
pause
