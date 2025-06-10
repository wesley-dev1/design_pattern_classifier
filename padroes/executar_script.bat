@echo off
SETLOCAL

REM Caminho da pasta do script .py
cd /d "%~dp0"

REM Define manualmente a API KEY (use com cautela se for um arquivo público)
set GOOGLE_GENAI_API_KEY=API KEY AQUI
setx GOOGLE_GENAI_API_KEY "%GOOGLE_GENAI_API_KEY%" >nul

REM Nome do ambiente virtual
set VENV_DIR=.venv

REM Verifica se o Python está disponível
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Python não encontrado no PATH.
    echo Instale o Python e marque "Add Python to PATH".
    pause
    exit /b
)

REM Cria ambiente virtual se necessário
if not exist %VENV_DIR% (
    echo Criando ambiente virtual...
    python -m venv %VENV_DIR%
)

REM Ativa o ambiente
call %VENV_DIR%\Scripts\activate.bat

REM Instala dependências
python -m pip install --upgrade pip
pip install google-genai

REM Executa o script principal
python "menu_design_pattern_classifier_gui.py"

pause
ENDLOCAL
