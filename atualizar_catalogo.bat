@echo off
REM ========================================
REM Atualiza o catálogo de ingredientes no site
REM ========================================

echo Gerando arquivo ingredients_master.json...
python atualizar_receitas.py

REM Copia o arquivo gerado para a pasta /docs
if exist ingredients_master.json (
    echo Movendo ingredients_master.json para /docs...
    move /Y ingredients_master.json docs\ingredients_master.json
) else (
    echo ⚠️  Arquivo ingredients_master.json não encontrado!
)

echo.
echo ✅ Catálogo atualizado com sucesso em docs\ingredients_master.json
pause
