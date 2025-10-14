#!/usr/bin/env python3
import csv, sys, re

PATH = sys.argv[1] if len(sys.argv) > 1 else "admin_scaffold/admin/ingredients_master.csv"

REQUIRED = ["id","name","category","fat_pct","sugar_pct","solids_pct","vegan","is_active","version"]

def sniff_delimiter(first_line: str) -> str:
    # Detecta ; vs , pelo cabeçalho
    return ";" if first_line.count(";") >= first_line.count(",") else ","

def fnum(s):
    s = (s or "").strip()
    if s == "": return None
    # troca vírgula por ponto
    return float(s.replace(",", "."))

def fbool(s):
    s2 = (str(s) or "").strip().lower()
    if s2 in ("true","1","yes","y","sim"): return True
    if s2 in ("false","0","no","n","nao","não",""): return False
    # mantém compatível com CSV “vazio” => False
    return False

def is_empty_row(row):
    # Linha vazia se todos os valores forem vazios
    return all((v is None) or (str(v).strip() == "") for v in row.values())

errors = []
ids = set()

with open(PATH, "r", encoding="utf-8-sig", newline="") as f:
    first = f.readline()
    if not first:
        print("Arquivo CSV vazio.")
        sys.exit(1)
    delim = sniff_delimiter(first)
    f.seek(0)
    reader = csv.DictReader(f, delimiter=delim)

    # Checagem de cabeçalho mínimo
    header = [h.strip() for h in (reader.fieldnames or [])]
    missing = [k for k in REQUIRED if k not in header]
    if missing:
        print("Falha: cabeçalho ausente:", ", ".join(missing))
        sys.exit(1)

    line = 1  # conta cabeçalho
    for row in reader:
        line += 1
        if is_empty_row(row):
            continue

        rid = (row.get("id","") or "").strip()
        if not re.match(r"^[a-z0-9_\-]+$", rid):
            errors.append((line, "id", f"id inválido '{rid}' (use a-z, 0-9, _ -)"))
        if rid in ids:
            errors.append((line, "id", f"id duplicado '{rid}'"))
        ids.add(rid)

        name = (row.get("name","") or "").strip()
        if not name:
            errors.append((line, "name", "nome vazio"))

        # Números (aceita vírgula)
        try:
            fat = fnum(row.get("fat_pct",""))
        except Exception:
            errors.append((line,"fat_pct",f"número inválido: {row.get('fat_pct')}")); fat=None
        try:
            sug = fnum(row.get("sugar_pct",""))
        except Exception:
            errors.append((line,"sugar_pct",f"número inválido: {row.get('sugar_pct')}")); sug=None
        try:
            sol = fnum(row.get("solids_pct",""))
        except Exception:
            errors.append((line,"solids_pct",f"número inválido: {row.get('solids_pct')}")); sol=None

        for k, v in (("fat_pct", fat), ("sugar_pct", sug), ("solids_pct", sol)):
            if v is None:
                errors.append((line, k, f"{k} vazio"))
            else:
                if not (0 <= v <= 100):
                    errors.append((line, k, f"{k} fora de 0..100: {v}"))

        if all(x is not None for x in (fat, sug, sol)) and sol + 1e-6 < fat + sug:
            errors.append((line, "solids_pct", f"sólidos ({sol}) < gordura+açúcar ({fat+sug})"))

        # Booleans básicos (não quebra se vier “true/false” em minúsculas)
        for key in ("vegan","is_active"):
            _ = fbool(row.get(key,""))

if errors:
    print("Falhas de validação:")
    for ln, fld, msg in errors:
        print(f"  linha {ln}, campo '{fld}': {msg}")
    sys.exit(1)

print("OK: validação concluída sem erros.")
