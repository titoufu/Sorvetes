#!/usr/bin/env python3
import csv, sys, json, os, datetime

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "admin_scaffold/admin/ingredients_master.csv"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "site/ingredients_master.json"

def sniff_delimiter(sample: str) -> str:
    try:
        return csv.Sniffer().sniff(sample, delimiters=";,").delimiter
    except Exception:
        return ";" if sample.count(";") >= sample.count(",") else ","

def normalize_header(header):
    if len(header) == 1 and ";" in header[0]:
        return [h.strip() for h in header[0].split(";")]
    return [h.strip() for h in header]

def fnum(s):
    s = (s or "").strip()
    if s == "": return None
    return float(s.replace(",", "."))

def fbool(s):
    s2 = (str(s) or "").strip().lower()
    if s2 in ("true","1","yes","y","sim","verdadeiro","v"): 
        return True
    if s2 in ("false","0","no","n","nao","não","falso","f"): 
        return False
    return False


def is_empty_row_values(cells):
    return all((c is None) or (str(c).strip()=="") for c in cells)

with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
    sample = f.read(4096)
    delim = sniff_delimiter(sample)
    f.seek(0)
    reader = csv.reader(f, delimiter=delim)

    header = next(reader, None)
    if header and len(header)==1 and header[0].lower().startswith("sep="):
        header = next(reader, None)
    if not header:
        raise SystemExit("CSV sem cabeçalho.")
    header = normalize_header(header)

    records = []
    for cells in reader:
        if is_empty_row_values(cells):
            continue
        if len(cells) == 1 and ";" in cells[0] and delim != ";":
            cells = cells[0].split(";")
        row = dict(zip(header, cells + [""]*(len(header)-len(cells))))

        rid = (row.get("id","") or "").strip()
        name = (row.get("name","") or "").strip()
        if not rid or not name:
            continue  # ignora lixo/linhas em branco

        # normaliza tipos
        for k in ("fat_pct","sugar_pct","solids_pct","density_g_ml"):
            if k in row:
                v = row[k]
                row[k] = None if (v is None or str(v).strip()=="") else fnum(v)
        for k in ("vegan","is_active"):
            if k in row: row[k] = fbool(row[k])

        records.append(row)

now = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00","Z")
manifest = {"schema_version":"1.0","updated_at":now,"count":len(records),"ingredients":records}

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as out:
    json.dump(manifest, out, ensure_ascii=False, indent=2)

print(f"Gerado {OUT_PATH} com {len(records)} ingredientes")
