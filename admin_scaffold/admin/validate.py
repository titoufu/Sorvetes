#!/usr/bin/env python3
import csv, sys, re

PATH = sys.argv[1] if len(sys.argv) > 1 else "admin_scaffold/admin/ingredients_master.csv"
REQUIRED = ["id","name","category","fat_pct","sugar_pct","solids_pct","vegan","is_active","version"]

def sniff_delimiter(sample: str) -> str:
    try:
        return csv.Sniffer().sniff(sample, delimiters=";,").delimiter
    except Exception:
        return ";" if sample.count(";") >= sample.count(",") else ","

def normalize_header(header):
    if len(header) == 1 and ";" in header[0]:  # cabeçalho “colado”
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


def is_empty_row(row):
    return all((v is None) or (str(v).strip() == "") for v in row.values())

errors, ids = [], set()

with open(PATH, "r", encoding="utf-8-sig", newline="") as f:
    sample = f.read(4096)
    delim = sniff_delimiter(sample)
    f.seek(0)
    reader = csv.reader(f, delimiter=delim)
    header = next(reader, None)
    if header and len(header) == 1 and header[0].lower().startswith("sep="):
        header = next(reader, None)
    if not header:
        print("CSV sem cabeçalho."); sys.exit(1)
    header = normalize_header(header)

    # Valida cabeçalho mínimo
    missing = [k for k in REQUIRED if k not in header]
    if missing:
        print("Falha: cabeçalho ausente:", ", ".join(missing)); sys.exit(1)

    # Leitura linha a linha mapeando ao cabeçalho
    for ln, cells in enumerate(reader, start=2):
        # ignora linhas completamente vazias (ex.: ';;;;;;;;;;;;;')
        if all((c is None) or (str(c).strip()=="") for c in cells):
            continue
        # se vier “colado”, divide
        if len(cells) == 1 and ";" in cells[0] and delim != ";":
            cells = cells[0].split(";")
        row = dict(zip(header, cells + [""]*(len(header)-len(cells))))

        if is_empty_row(row): continue

        rid = (row.get("id","") or "").strip()
        name = (row.get("name","") or "").strip()
        if not rid or not name:  # ignora lixo
            errors.append((ln,"id/name","vazio"))
            continue

        if not re.match(r"^[a-z0-9_\-]+$", rid):
            errors.append((ln,"id",f"id inválido '{rid}'"))
        if rid in ids:
            errors.append((ln,"id",f"id duplicado '{rid}'"))
        ids.add(rid)

        def N(k):
            v = row.get(k,"")
            return None if (v is None or str(v).strip()=="") else fnum(v)

        fat, sug, sol = N("fat_pct"), N("sugar_pct"), N("solids_pct")
        for k,v in (("fat_pct",fat),("sugar_pct",sug),("solids_pct",sol)):
            if v is None: errors.append((ln,k,f"{k} vazio"))
            else:
                if not (0 <= v <= 100):
                    errors.append((ln,k,f"{k} fora de 0..100: {v}"))

        if all(x is not None for x in (fat,sug,sol)) and sol + 1e-6 < fat + sug:
            errors.append((ln,"solids_pct",f"sólidos ({sol}) < gordura+açúcar ({fat+sug})"))

if errors:
    print("Falhas de validação:")
    for ln, fld, msg in errors:
        print(f"  linha {ln}, campo '{fld}': {msg}")
    sys.exit(1)

print("OK: validação concluída sem erros.")
