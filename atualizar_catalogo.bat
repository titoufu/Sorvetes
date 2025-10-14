@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ===================== PATHS (relative to this .bat) =====================
set "ROOT=%~dp0"
set "CSV=%ROOT%admin_scaffold\admin\ingredients_master.csv"
set "VALIDATE=%ROOT%admin_scaffold\admin\validate.py"
set "BUILD=%ROOT%admin_scaffold\admin\build_json.py"
set "OUTJSON=%ROOT%site\ingredients_master.json"
set "LOGDIR=%ROOT%logs"
rem ========================================================================

rem Make LOGDIR
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

rem Build a portable timestamp from %DATE% and %TIME% (locale-agnostic-ish)
set "TS_RAW=%DATE%_%TIME%"
set "TS=%TS_RAW: =0%"
set "TS=%TS::=-%"
set "TS=%TS:/=-%"
set "TS=%TS:\=-%"
set "TS=%TS:.=-%"
set "TS=%TS:,=-%"
set "TS=%TS%%RANDOM%"
set "LOGFILE=%LOGDIR%\atualizacao_%TS%.log"

echo ===========================================
echo  Atualizando catálogo de ingredientes...
echo ===========================================
echo [INICIO] %DATE% %TIME%  > "%LOGFILE%"
echo ROOT: %ROOT%            >> "%LOGFILE%"
echo CSV: %CSV%              >> "%LOGFILE%"
echo JSON: %OUTJSON%         >> "%LOGFILE%"
echo ------------------------------------------------ >> "%LOGFILE%"

rem --------- Locate CSV if missing ---------
if not exist "%CSV%" (
  echo [WARN] CSV não encontrado no caminho padrão. Tentando localizar...
  echo [WARN] Tentando localizar CSV... >> "%LOGFILE%"
  for /f "delims=" %%F in ('dir /s /b "%ROOT%ingredients_master.csv" 2^>nul') do (
    set "CSV=%%F"
  )
)

if not exist "%CSV%" (
  echo [ERRO] CSV não encontrado. Verifique se salvou como CSV em admin_scaffold\admin\ingredients_master.csv
  echo [ERRO] CSV não encontrado. >> "%LOGFILE%"
  goto :EOF
)

if not exist "%VALIDATE%" (
  echo [ERRO] validate.py não encontrado: %VALIDATE%
  echo [ERRO] validate.py não encontrado: %VALIDATE% >> "%LOGFILE%"
  goto :EOF
)
if not exist "%BUILD%" (
  echo [ERRO] build_json.py não encontrado: %BUILD%
  echo [ERRO] build_json.py não encontrado: %BUILD% >> "%LOGFILE%"
  goto :EOF
)

rem Detect Python
set "PY=python"
%PY% --version >nul 2>&1
if errorlevel 1 (
  set "PY=python3"
  %PY% --version >nul 2>&1
  if errorlevel 1 (
    echo [ERRO] Python não encontrado (python/python3).
    echo [ERRO] Python não encontrado (python/python3). >> "%LOGFILE%"
    goto :EOF
  )
)

rem --------- VALIDATION ---------
echo.
echo [1/4] Validando CSV...
echo [VALIDATE] %DATE% %TIME% >> "%LOGFILE%"
"%PY%" "%VALIDATE%" "%CSV%"
if errorlevel 1 (
  echo [ERRO] Validação falhou. Corrija o CSV antes de prosseguir.
  echo [ERRO] Validação falhou. >> "%LOGFILE%"
  goto :EOF
)
echo [OK] Validação concluída. >> "%LOGFILE%"

rem --------- BUILD JSON ---------
echo.
echo [2/4] Gerando JSON...
echo [BUILD] %DATE% %TIME% >> "%LOGFILE%"
"%PY%" "%BUILD%" "%CSV%" "%OUTJSON%"
if errorlevel 1 (
  echo [ERRO] Falha ao gerar JSON.
  echo [ERRO] Falha ao gerar JSON. >> "%LOGFILE%"
  goto :EOF
)
echo [OK] JSON gerado: "%OUTJSON%"
echo [OK] JSON gerado. >> "%LOGFILE%"

rem --------- GIT ADD / COMMIT / PUSH ---------
echo.
echo [3/4] Preparando commit...
cd /d "%ROOT%"
git add -A
git diff --cached --quiet
if errorlevel 1 (
  set "NEEDCOMMIT=1"
) else (
  set "NEEDCOMMIT=0"
)

if "%NEEDCOMMIT%"=="0" (
  echo [INFO] Nenhuma mudança para commit.
  echo [INFO] Nenhuma mudança para commit. >> "%LOGFILE%"
  goto DEPLOY_INFO
)

echo [4/4] Efetuando commit e push...
set "MSG=Atualiza catálogo via planilha Excel (%TS%)"
git commit -m "%MSG%"
if errorlevel 1 (
  echo [ERRO] Falha no commit.
  echo [ERRO] Falha no commit. >> "%LOGFILE%"
  goto :EOF
)
git push origin main
if errorlevel 1 (
  echo [ERRO] Falha no push.
  echo [ERRO] Falha no push. >> "%LOGFILE%"
  goto :EOF
)
echo [OK] Alterações enviadas ao GitHub!
echo [OK] Alterações enviadas ao GitHub! >> "%LOGFILE%"
goto END

:DEPLOY_INFO
echo [INFO] Se apenas o CSV mudou sem gerar diff, verifique normalização (linhas/decimais) ou rode novamente após novas edições.
echo [INFO] Sem mudanças; nada foi enviado. >> "%LOGFILE%"

:END
echo ------------------------------------------------ >> "%LOGFILE%"
echo [FIM] %DATE% %TIME% >> "%LOGFILE%"
echo.
echo Log salvo em: %LOGFILE%
echo.
pause
endlocal
