@echo off
REM Mineru WebUI (Gradio) Service Start Script
REM This script is used to activate the Mineru Conda environment, set the model source, and start the WebUI service.

set "CONDA_ENV_NAME=mineru"
set "MINERU_MODEL_SOURCE=modelscope"
set "WEBUI_HOST=0.0.0.0"
set "WEBUI_PORT=7860"

echo ==================================================
echo   Preparing to start Mineru WebUI Service
echo ==================================================

REM Activate Conda Environment
echo [INFO] Activating Conda Environment: %CONDA_ENV_NAME%...
call conda activate %CONDA_ENV_NAME%

if errorlevel 1 (
    echo [ERROR] Conda environment activation failed. Check if the environment name is correct or if "conda init" has been run.
    echo [ERROR] If running from a standard CMD window, ensure Conda is properly initialized.
    pause
    goto :EOF
)

REM Set Model Source Environment Variable
echo [INFO] Setting model source: %MINERU_MODEL_SOURCE%...
set MINERU_MODEL_SOURCE=%MINERU_MODEL_SOURCE%

REM Start WebUI Service
echo [INFO] Starting Mineru WebUI (Gradio) service...
echo Access Address (Web UI): http://127.0.0.1:%WEBUI_PORT%
mineru-gradio --server-name %WEBUI_HOST% --server-port %WEBUI_PORT%

REM Keep the window open until the service stops or the user presses a key
pause