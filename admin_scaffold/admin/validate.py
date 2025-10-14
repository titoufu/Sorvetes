#!/usr/bin/env python3
import csv, sys, re

PATH = sys.argv[1] if len(sys.argv) > 1 else "admin/ingredients_master.csv"

def fnum(s):
    return float(str(s).replace(",",".").strip())

def fbool(s):
    return str(s).strip().lower() in ("true","1","yes","y")

errs = []
ids = set()
with open(PATH, "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    line = 1
    for row in r:
        line += 1
        rid = row["id"].strip()
        if not re.match(r"^[a-z0-9_\-]+$", rid):
            errs.append((line,"id",f"id inválido: {rid}"))
        if rid in ids:
            errs.append((line,"id",f"id duplicado: {rid}"))
        ids.add(rid)
        for k in ("fat_pct","sugar_pct","solids_pct"):
            try:
                v = fnum(row[k])
                if not (0 <= v <= 100):
                    errs.append((line,k,f"{k} fora de 0..100: {v}"))
            except Exception:
                errs.append((line,k,f"{k} inválido: {row[k]}"))
        try:
            fat, sug, sol = fnum(row["fat_pct"]), fnum(row["sugar_pct"]), fnum(row["solids_pct"])
            if sol + 1e-6 < fat + sug:
                errs.append((line,"solids_pct",f"sólidos ({sol}) < gordura+açúcar ({fat+sug})"))
        except Exception:
            pass

if errs:
    print("Falhas de validação:")
    for ln, fld, msg in errs:
        print(f"  linha {ln} campo {fld}: {msg}")
    sys.exit(1)
print("OK: validação concluída.")
