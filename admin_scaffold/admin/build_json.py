#!/usr/bin/env python3
import csv, sys, json, os, datetime

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "admin_scaffold/admin/ingredients_master.csv"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "site/ingredients_master.json"

REQUIRED = ["id","name","category","fat_pct","sugar_pct","solids_pct","vegan","is_active","version"]

def sniff_delimiter(first_line: str) -> str:
    return ";" if first_line.count(";") >= first_line.count(",") else ","

def fnum(s):
    s = (s or "").strip()
    if s == "": return None
    return float(s.replace(",", "."))

def fbool(s):
    s2 = (str(s) or "").strip().lower()
    if s2 in ("true","1","yes","y","sim"): return True
    if s2 in ("false","0","no","n","nao","não",""): return False
    return False

def is_empty_row(row: dict) -> bool:
    # considera vazia se todos os campos estão vazios
    return all((v is None) or (str(v).strip() == "") for v in row.values())

with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
    first = f.readline()
    if not first:
        raise SystemExit("Arquivo CSV vazio.")
    delim = sniff_delimiter(first)
    f.seek(0)
    reader = csv.DictReader(f, delimiter=delim)

    header = [h.strip() for h in (reader.fieldnames or [])]
    missing = [k for k in REQUIRED if k not in header]
    if missing:
        raise SystemExit("Cabeçalho ausente: " + ", ".join(missing))

    data = []
    for row in reader:
        if is_empty_row(row):  # <<< ignora linhas vazias
            continue

        norm = dict(row)      # mantém colunas extras (ex.: status)
        # números
        for k in ("fat_pct","sugar_pct","solids_pct","density_g_ml"):
            if k in norm:
                v = norm[k]
                norm[k] = None if (v is None or str(v).strip()=="") else float(str(v).replace(",", "."))
        # booleanos
        for k in ("vegan","is_active"):
            if k in norm:
                norm[k] = fbool(norm[k])

        # saneamento mínimo – se faltar id/name, ignora
        if not (str(norm.get("id","")).strip() and str(norm.get("name","")).strip()):
            continue

        data.append(norm)

now = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00","Z")

manifest = {
    "schema_version":"1.0",
    "updated_at": now,
    "count": len(data),
    "ingredients": data
}

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as out:
    json.dump(manifest, out, ensure_ascii=False, indent=2)

print(f"Gerado {OUT_PATH} com {len(data)} ingredientes")
