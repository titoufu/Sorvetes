# Fluxo do Administrador — Catálogo Mestre
Edite **apenas** `admin/ingredients_master.csv`. Abra PR para `main`.

## Validar localmente
```bash
python3 admin/validate.py admin/ingredients_master.csv
```

## Gerar JSON localmente
```bash
python3 admin/build_json.py admin/ingredients_master.csv site/ingredients_master.json
```

## Publicação (GitHub Pages via Actions)
Workflow gera `site/ingredients_master.json` e publica em Pages.
URL típica: https://<user>.github.io/<repo>/ingredients_master.json
