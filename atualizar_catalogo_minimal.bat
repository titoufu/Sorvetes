@echo off
REM ===== Script minimalista: sem variáveis, sem IF/FOR, sem parênteses =====
REM Rode este arquivo a partir da pasta raiz do repositório (ex.: C:\Sorvetes)

python admin_scaffold\admin\validate.py admin_scaffold\admin\ingredients_master.csv
IF ERRORLEVEL 1 GOTO END

python admin_scaffold\admin\build_json.py admin_scaffold\admin\ingredients_master.csv site\ingredients_master.json

git add .
git commit -m "Atualiza catalogo via planilha Excel"
git push origin main

:END
pause
