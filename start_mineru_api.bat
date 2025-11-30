@echo off
title Start Mineru Service AND Run Converter

echo [INFO] Activating Anaconda environment: mineru (for API Server)
call conda activate mineru

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate conda environment 'mineru'.
    echo Please make sure Anaconda is installed and the 'mineru' environment exists.
    pause
    exit /b
)

echo [INFO] Setting environment variable MINERU_MODEL_SOURCE=modelscope
set MINERU_MODEL_SOURCE=modelscope

echo [INFO] Starting Mineru API service (in 'mineru' env) in a NEW window...
echo (Access API docs at http://127.0.0.1:8000/docs)

:: Use the START command to launch the server in a new window
:: This command will use the currently activated 'mineru' environment
START "Mineru API Server" mineru-api --host 0.0.0.0 --port 8000

echo.
echo [INFO] Waiting 10 seconds for the API server to initialize...
echo (If your server starts slowly, you may need to increase this time.)
echo.

:: Wait for 10 seconds. ping is a "sleep" trick that works on all Windows versions.
:: 127.0.0.1 -n 11 means ping 11 times, 1 second each, for a 10-second total wait.
ping 127.0.0.1 -n 11 > nul

echo.
echo [INFO] Activating 'python311' environment for client script...
call conda activate python311

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate conda environment 'python311'.
    echo Please make sure the 'python311' environment exists.
    pause
    exit /b
)

echo.
echo [INFO] Server should be ready. Launching Python conversion script (using 'python311' env)...
echo [WARN] Please make sure the 'requests' library is installed in your 'python311' environment.
echo [WARN] (You can install it by running 'conda activate python311' then 'pip install requests')
echo.

:: Run the Python script
:: Because we activated 'python311', this 'python' command will use that environment
python "%~dp0convert_pdfs_in_folder.py"

echo.
echo [INFO] Python script has finished.
echo The Mineru API server is still running in its separate window.
echo You must close that window manually when you are done.
echo.
pause