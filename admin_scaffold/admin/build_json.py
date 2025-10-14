#!/usr/bin/env python3
import csv, sys, json, os, datetime

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "admin/ingredients_master.csv"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "site/ingredients_master.json"

now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

with open(CSV_PATH, "r", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
manifest = {"schema_version":"1.0","updated_at":now,"count":len(data),"ingredients":data}
with open(OUT_PATH, "w", encoding="utf-8") as out:
    json.dump(manifest, out, ensure_ascii=False, indent=2)
print(f"Gerado {OUT_PATH} com {len(data)} ingredientes")
