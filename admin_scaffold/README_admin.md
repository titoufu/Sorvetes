# 📘 Catálogo Mestre de Ingredientes — Guia do Administrador

Este documento é o **guia completo de administração** do catálogo de ingredientes do projeto Sorvetes.  
Ele reúne as informações técnicas do repositório e o **procedimento oficial para atualização segura** do arquivo `ingredients_master.csv`.

---

## 🧭 0️⃣ Procedimento de Atualização Segura

Este fluxo garante que as atualizações do catálogo ocorram com segurança, validação automática e histórico auditável via Pull Request e GitHub Actions.

### 1️⃣ Abrir o projeto localmente

```bash
cd C:\Sorvetes
git checkout main
git pull origin main
```

### 2️⃣ Editar o CSV

Edite o arquivo:

```
admin_scaffold/admin/ingredients_master.csv
```

Verifique:
- Cabeçalhos intactos
- Campos obrigatórios preenchidos
- Pontos decimais com `.` (não `,`)
- Ordem das colunas preservada

### 3️⃣ Criar branch temporária

```bash
git checkout -b atualizar-catalogo-AAAA-MM-DD
```

Exemplo:
```bash
git checkout -b atualizar-catalogo-2025-10-24
```

### 4️⃣ Commit e  push

```bash
git add admin_scaffold/admin/ingredients_master.csv
git commit -m "chore(catalogo): atualização de ingredientes"
git push -u origin atualizar-catalogo-2025-10-24
```

O terminal mostrará o link para abrir o Pull Request.

### 5️⃣ Criar Pull Request

1. Clique no link mostrado após o push.  
2. Verifique título e descrição.  
3. Clique em **Create pull request**.

### 6️⃣ Aprovar e fazer merge

1. Vá até **Files changed → Review changes → Approve → Submit review**  
2. Clique em **Merge pull request → Confirm merge**

Após o merge, o **workflow `Publicar catálogo`** é executado automaticamente.

### 7️⃣ Acompanhar o workflow

Vá em **Actions → Publicar catálogo**.  
Você verá as etapas:

```
🔒 Verificar autor do commit
✅ Validar CSV
🧱 Gerar JSON do catálogo
🚀 Commit e push automáticos
```

> Se aparecer “Autor detectado: titoufu” e “Commit automático feito por github-actions[bot]”, o processo foi concluído com sucesso.

### 8️⃣ Verificar publicação

Acesse:

```
site/ingredients_master.json
```

ou o link público:

```
https://titoufu.github.io/Sorvetes/ingredients_master.json?t=now
```

### 9️⃣ Limpeza pós-merge

```bash
git checkout main
git pull origin main
git branch -d atualizar-catalogo-AAAA-MM-DD
git push origin --delete atualizar-catalogo-AAAA-MM-DD
```

---

## 🧱 1️⃣ Estrutura do Repositório

O repositório contém os arquivos e pastas que definem o catálogo e o site público de consulta:

```
/admin_scaffold/
│
├─ /admin/
│   ├─ ingredients_master.csv     → Catálogo principal de ingredientes
│   ├─ build_json.py              → Gera o JSON oficial
│   ├─ validate.py                → Valida dados do CSV
│   ├─ README_admin.md            → Este documento
│
├─ /site/
│   ├─ index.html                 → Página principal do catálogo
│   ├─ ingredients_master.json    → Arquivo JSON publicado
│
├─ /.github/workflows/
│   ├─ publish-catalog.yml        → Workflow automático de publicação
│
├─ atualizar_catalogo.bat         → Script local opcional para testes
└─ ...
```

---

## 🧩 2️⃣ Arquivos Principais

### `validate.py`
Script de validação de integridade do CSV.  
Verifica:
- IDs duplicados  
- Campos obrigatórios vazios  
- Faixas de valores (ex: gordura, açúcares, sólidos)  
- Consistência de somatórios (ex: `fat_pct + sugar_pct ≤ solids_pct`)  

### `build_json.py`
Converte o CSV validado em `ingredients_master.json`.  
Adiciona campos automáticos:
- `"schema_version"`  
- `"updated_at"` (data UTC ISO8601)  
- `"count"` (número de ingredientes)  
- `"ingredients": [...]`

### `publish-catalog.yml`
Workflow GitHub Actions que executa:
1. `validate.py`
2. `build_json.py`
3. Faz commit automático do JSON gerado.

Inclui verificação de autor (só `titoufu` e `github-actions[bot]` são permitidos).

### `atualizar_catalogo.bat`
Script local para gerar e validar o JSON sem enviar PR.  
Útil para testes antes do commit oficial.

---

## 🧰 3️⃣ Fluxo de Automação

1. Um commit no CSV dispara o workflow **Publicar catálogo**.  
2. O GitHub Actions valida e gera o JSON.  
3. O bot faz commit automático.  
4. O site é atualizado no GitHub Pages.  

---

## 🧪 4️⃣ Testes Locais

Executar validação:
```bash
python admin_scaffold/admin/validate.py admin_scaffold/admin/ingredients_master.csv
```

Gerar JSON manualmente:
```bash
python admin_scaffold/admin/build_json.py admin_scaffold/admin/ingredients_master.csv site/ingredients_master.json
```

Verificar resultado:
```bash
type site\ingredients_master.json
```

---

## 🔐 5️⃣ Segurança

| Proteção | Descrição |
|-----------|------------|
| 🔒 Branch `main` protegida | Nenhum push direto |
| 🔑 Verificação de autor no workflow | Apenas `titoufu` ou `github-actions[bot]` publicam |
| 🤖 Commits automáticos | JSON gerado via Actions, nunca manualmente |
| 🧩 Revisão obrigatória | Todo update passa por Pull Request |
| 📜 Histórico rastreável | Cada alteração fica registrada com logs e datas |

---

## 💬 6️⃣ Dicas Finais

- Sempre atualize a branch `main` antes de criar uma nova.  
- Prefira nomes de branch descritivos (`atualizar-catalogo-YYYY-MM-DD`).  
- Não edite o JSON manualmente.  
- Use os scripts locais apenas para validação prévia.  
- Em caso de erro no workflow, verifique o log em **Actions → Publicar catálogo**.

---

**Autor:** `titoufu`  
**Workflow:** `.github/workflows/publish-catalog.yml`  
**Última revisão:** 24 de outubro de 2025
