import os
import json
from datetime import datetime

# Caminho da pasta onde estão as receitas
PASTA_RECEITAS = os.path.join("site", "Receitas Testadas")
ARQUIVO_SAIDA = os.path.join(PASTA_RECEITAS, "receitas_testadas.json")

def gerar_json_receitas():
    # Garantir que a pasta existe
    if not os.path.isdir(PASTA_RECEITAS):
        print(f"❌ Pasta não encontrada: {PASTA_RECEITAS}")
        return

    # Listar arquivos .txt
    arquivos_txt = [f for f in os.listdir(PASTA_RECEITAS) if f.lower().endswith(".txt")]

    if not arquivos_txt:
        print("⚠️ Nenhum arquivo .txt encontrado.")
        return

    # Montar estrutura JSON
    receitas = []
    for nome in sorted(arquivos_txt):
        titulo = (
            nome.replace("_", " ")
                .replace(".txt", "")
                .replace("%20", " ")
                .strip()
        )
        receitas.append({
            "titulo": titulo,
            "arquivo": nome
        })

    dados = {
        "schema_version": "1.0",
        "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(receitas),
        "receitas": receitas
    }

    # Gravar JSON formatado
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo '{ARQUIVO_SAIDA}' atualizado com {len(receitas)} receitas.")
    print("🕒 Última atualização:", dados["updated_at"])

if __name__ == "__main__":
    gerar_json_receitas()
