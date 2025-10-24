@echo off
echo ========================================
echo   Atualizando lista de receitas...
echo ========================================

REM Caminho absoluto do Python (ajuste se necessário)
python atualizar_receitas.py

if %errorlevel%==0 (
    echo ----------------------------------------
    echo ✅ Atualização concluída com sucesso!
) else (
    echo ----------------------------------------
    echo ❌ Ocorreu um erro ao atualizar o JSON.
)
echo.
pause
