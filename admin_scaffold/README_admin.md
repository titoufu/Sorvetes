Catálogo Mestre de Ingredientes — Guia do Administrador

Objetivo: Manter uma única fonte de verdade para os ingredientes do app (somente leitura para o usuário).
Fluxo oficial: Excel (.xlsx) → CSV (.csv) → validate.py → build_json.py → ingredients_master.json (GitHub Pages).
Automação local: atualizar_catalogo.bat (Windows).

1) Estrutura do repositório
/                 ← raiz do repositório
├─ admin_scaffold/
│  ├─ admin/
│  │  ├─ ingredients_master.csv        ← CSV oficial (editável via Excel)
│  │  ├─ validate.py                   ← valida CSV (faixas, ids, etc.)
│  │  ├─ build_json.py                 ← gera site/ingredients_master.json
│  │  └─ schema.json                   ← referência de campos
│  └─ README_admin.md                  ← este guia
├─ site/
│  └─ ingredients_master.json          ← gerado, publicado no Pages
├─ .github/workflows/
│  └─ publish-catalog.yml              ← valida + gera + publica
├─ atualizar_catalogo.bat              ← script Windows (automatiza tudo)
└─ config.json                         ← aponta para a URL pública do JSON


Importante: O workflow só funciona se estiver em .github/workflows na raiz do repo.

2) Arquivos principais

Editor em Excel (recomendado para editar):
Editor_Admin_Ingredientes_v2.xlsx (contém listas, validações e base pré-preenchida).
Use-o para editar e depois salve como CSV.

Fonte oficial (editável):
admin_scaffold/admin/ingredients_master.csv

Scripts (não edite a menos que saiba o que está fazendo):

admin_scaffold/admin/validate.py – valida campos, faixas e consistência.

admin_scaffold/admin/build_json.py – transforma CSV → JSON.

Automação local (Windows):
atualizar_catalogo.bat – roda validação, gera JSON, faz commit e push.

Saída publicada:
site/ingredients_master.json → vai para o GitHub Pages.

3) Esquema de dados (colunas do CSV)
Campo	Tipo	Regras / Observações
id	string	Único, minúsculo, a-z, 0-9, _ ou - (ex.: leite_coco_17)
name	string	Nome de exibição (ex.: “Leite de coco (17% gordura)”)
category	string	dairy, dairy_fat, dairy_powder, plant_milk, water, sugar, syrup, fruit, emulsifier, stabilizer, fat, cocoa, nut_paste, other
fat_pct	número	0–100 (aceita vírgula ou ponto)
sugar_pct	número	0–100 (aceita vírgula ou ponto)
solids_pct	número	0–100; deve ser ≥ fat_pct + sugar_pct
density_g_ml	número	Opcional. Se não souber, deixe em branco (default tratado no app)
vegan	boolean	true/false (dropdown no Excel)
allergens	string	Ex.: milk, eggs, soy, peanuts, tree_nuts (separe múltiplos por ;)
is_active	boolean	true/false (para descontinuar sem apagar)
notes	string	Observações (ex.: fonte do dado, alertas)
version	string	Versão semântica do ingrediente (ex.: 1.0.0)
updated_at	string	Pode ficar vazio; o JSON gerado registra data/hora atual
source_url	string	Link para rótulo/estudo/ficha técnica (opcional)
status	string	Ignorado na validação (usado somente no Excel para “OK/Ajustar”)

Separador: o sistema aceita ; ou , automaticamente.
Decimais: aceita vírgula ou ponto (são normalizados no build).

4) Fluxo de edição (Excel → CSV)

Abra o Excel e edite Editor_Admin_Ingredientes_v2.xlsx (ou sua cópia).

Salvar como… → CSV (UTF-8) e sobrescreva:

admin_scaffold/admin/ingredients_master.csv


O Excel pode usar ; como separador e , nos decimais — tudo ok.

Linhas completamente vazias são ignoradas no build.

5) Automatização no Windows (.bat)

Ambiente: PowerShell (no diretório raiz do repo)

Rode:

.\atualizar_catalogo.bat


O que o .bat faz:

Executa validate.py sobre ingredients_master.csv.

Executa build_json.py e gera site/ingredients_master.json.

git add . && git commit -m "Atualiza catálogo via planilha Excel" && git push origin main.

Se a validação falhar, o .bat para e mostra o erro (não faz commit).

Dica PowerShell: se aparecer “não reconhecido”, use .\atualizar_catalogo.bat.
(Por segurança, o PowerShell não executa arquivos do diretório atual sem .\.)

6) Publicação automática (GitHub Actions + Pages)

O arquivo .github/workflows/publish-catalog.yml:

Valida o CSV

Gera o JSON em site/ingredients_master.json

Publica no GitHub Pages

Pré-requisitos (uma vez só):

Repo → Settings → Pages → Build and deployment: GitHub Actions.

Repo → Settings → Actions → General → Allow all actions e Read and write permissions.

URL pública do catálogo:

https://<seu-usuario>.github.io/<seu-repo>/ingredients_master.json


Exemplo do projeto:

https://titoufu.github.io/Sorvetes/ingredients_master.json


Se não atualizar, use cache-busting:

https://.../ingredients_master.json?t=now

7) Boas práticas e governança

Branch main protegida (PR obrigatório, revisão por outro admin).

Versionamento por ingrediente (version) quando alterar composição.

is_active=false para descontinuar sem apagar histórico.

id estável: não renomeie ids; crie um novo e desative o antigo.

Auditoria: commits claros; opcional incluir data/hora no .bat.

8) Padrões por categoria (orientações úteis)

Frutas (polpa):

solids_pct ≈ °Brix da fruta.

sugar_pct ≈ 0,9 × solids_pct (açúcares são a maior parte dos sólidos).

fat_pct costuma ser ~0–1%.

Ex.: manga 15°Brix → solids=15, sugar≈13.5, fat≈0.6.

Xaropes (glicose, mel):

solids_pct < 100 por causa da água (ex.: glicose 42DE solids=80).

sugar_pct geralmente ≈ solids_pct (para simplificação prática).

Cacau/chocolate:

Cacau 22–24%: fat≈22, solids≈96.

Chocolate 70%: fat≈39–43, sugar≈~28, solids=100.

Lácteos:

Leite integral: fat≈3.2, solids≈12.5.

Creme 35%: fat=35, solids≈37.

Leite condensado: fat≈8, sugar≈55, solids≈73.

Oleaginosas (pastas 100%):

Pistache ~fat=45, sugar=10, solids≈96.

Avelã ~fat=60, sugar=6, solids≈96.

Regra de ouro da consistência: solids_pct ≥ fat_pct + sugar_pct.
Se violar, ajuste os números (ou revise a fonte).

9) Solução de problemas (FAQ)

Q: O .bat diz KeyError: 'id' (ou cabeçalho ausente).
A: A primeira linha do CSV deve ser o cabeçalho exato:

id;name;category;fat_pct;sugar_pct;solids_pct;density_g_ml;vegan;allergens;is_active;notes;version;updated_at;source_url;status


(Se usar vírgula, também funciona.)

Q: Números com vírgula (ex.: 12,5) quebram?
A: Não. Os scripts aceitam vírgula (convertem para ponto internamente).

Q: Linhas cheias de ;;;;;;;;; contam como ingrediente?
A: Não. Linhas vazias são ignoradas no build.

Q: O Actions não aparece em “Actions”.
A: Garanta que o workflow está em .github/workflows/publish-catalog.yml na raiz, e que você está na branch main.

Q: Erro 404 ao publicar no Pages.
A: Ative Pages: Settings → Pages → GitHub Actions e rode o workflow novamente.

Q: Quero editar só no VS Code, sem Excel.
A: Pode. Edite diretamente o CSV — os validadores vão conferir o formato e faixas.

10) Remoção de formatos antigos

O formato .asc não é mais utilizado.
Remova-o do projeto (ou mova para admin_scaffold/admin/old/ se quiser guardar histórico).

Exemplo:

git rm admin_scaffold/admin/ingredients_master.asc
git commit -m "Remove formato .asc (substituído por Excel→CSV→JSON)"
git push origin main

11) Script .bat (referência)

Se precisar recriar, este é o conteúdo recomendado de atualizar_catalogo.bat:

@echo off
echo ===========================================
echo  Atualizando catálogo de ingredientes...
echo ===========================================
python admin_scaffold/admin/validate.py admin_scaffold/admin/ingredients_master.csv
if errorlevel 1 (
    echo [ERRO] Validação falhou. Corrija o CSV antes de prosseguir.
    pause
    exit /b
)
python admin_scaffold/admin/build_json.py admin_scaffold/admin/ingredients_master.csv site/ingredients_master.json
echo.
echo [OK] JSON gerado com sucesso.
echo.
git add .
git commit -m "Atualiza catálogo via planilha Excel"
git push origin main
echo.
echo [OK] Alterações enviadas ao GitHub!
pause


Dica: para rodar no PowerShell, use .\atualizar_catalogo.bat.

12) URL oficial do catálogo (para o app)

Defina no config.json (na raiz do repo) a URL pública do JSON:

{
  "ingredients_catalog_url": "https://titoufu.github.io/Sorvetes/ingredients_master.json",
  "catalog_version": "1.0.0",
  "updated_at": "2025-10-14"
}


O app do usuário lerá esse endpoint para listar os ingredientes disponíveis.