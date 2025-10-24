import os
import json
import subprocess
from datetime import datetime

# Caminho da pasta das receitas
PASTA_RECEITAS = os.path.join("docs", "Receitas Testadas")
ARQUIVO_SAIDA = os.path.join(PASTA_RECEITAS, "receitas_testadas.json")

def gerar_json_receitas():
    """Gera o arquivo receitas_testadas.json com base nos .txt da pasta."""
    if not os.path.isdir(PASTA_RECEITAS):
        print(f"❌ Pasta não encontrada: {PASTA_RECEITAS}")
        return False

    arquivos_txt = [
        f for f in os.listdir(PASTA_RECEITAS)
        if f.lower().endswith(".txt") and not f.startswith("~$")
    ]

    if not arquivos_txt:
        print("⚠️ Nenhum arquivo .txt encontrado.")
        return False

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

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON atualizado com {len(receitas)} receitas.")
    print(f"🕒 Última atualização: {dados['updated_at']}")
    return True

def executar_git():
    """Executa git add, commit e push."""
    try:
        subprocess.run(["git", "add", ARQUIVO_SAIDA], check=True)
        commit_msg = f"Atualiza lista de receitas ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Alterações enviadas ao GitHub com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro durante operações do Git: {e}")

if __name__ == "__main__":
    if gerar_json_receitas():
        executar_git()
