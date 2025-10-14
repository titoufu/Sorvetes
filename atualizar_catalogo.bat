@echo off
echo ===========================================
echo  Atualizando catálogo de ingredientes...
echo ===========================================
python admin_scaffold/admin/validate.py admin_scaffold/admin/ingredients_master.csv
if errorlevel 1 (
    echo [ERRO] Validação falhou. Corrija o CSV antes de prosseguir.
    pause
    exit /b
)
python admin_scaffold/admin/build_json.py admin_scaffold/admin/ingredients_master.csv site/ingredients_master.json
echo.
echo [OK] JSON gerado com sucesso.
echo.
git add .
git commit -m "Atualiza catálogo via planilha Excel"
git push origin main
echo.
echo [OK] Alterações enviadas ao GitHub!
pause
