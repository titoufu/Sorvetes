# 🍦 Projeto Sorvetes — Continuação

Este documento consolida o **estado atual do projeto Sorvetes** e define o ponto de partida para a continuidade do desenvolvimento.  
Serve como referência para o **próximo ciclo de melhorias**, tanto de **UX/UI** quanto de **lógica e automação**.

---

## 🧩 Contexto do Projeto

**Nome:** Sorvetes  
**Objetivo:** Criar uma aplicação web para **montagem de receitas de sorvetes**, permitindo que:

- O **usuário** monte receitas personalizadas a partir de um catálogo de ingredientes.
- O **administrador** mantenha e publique o catálogo central de ingredientes.

---

## 🧑‍💻 Estrutura Atual do Repositório

```
Sorvetes/
│
├── site/
│   ├── index.html                ← Interface do usuário (funcional)
│   ├── ingredients_master.json   ← Catálogo de ingredientes (gerado automaticamente)
│   ├── manifest.webmanifest      ← Manifest PWA
│   ├── sw.js                     ← Service Worker
│   └── apple-touch-icon.png      ← Ícone
│
├── admin_scaffold/
│   ├── admin/
│   │   ├── build_json.py         ← Gera JSON a partir do Excel/CSV
│   │   ├── validate.py           ← Valida planilha
│   │   ├── schema.json           ← Esquema de validação
│   │   ├── ingredients_master.csv
│   │   └── ingredients_master.xlsx ← Fonte principal (editável)
│   └── README_admin.md           ← Manual do administrador
│
├── atualizar_catalogo.bat        ← Executa validação + geração + commit + push
├── config.json                   ← Define URL pública do catálogo
├── logs/                         ← Armazena logs de atualização
└── .github/workflows/
    └── publish-catalog.yml       ← Workflow de publicação no GitHub Pages
```

---

## ⚙️ Fluxo do Administrador

1. **Editar a planilha:**
   ```
   admin_scaffold/admin/ingredients_master.xlsx
   ```

2. **Gerar e publicar o catálogo:**
   ```
   .\atualizar_catalogo.bat
   ```
   Esse script realiza:
   - Validação da planilha (`validate.py`)
   - Geração de `ingredients_master.json` (`build_json.py`)
   - Commit + Push automáticos
   - Publicação no GitHub Pages

3. **Resultado publicado:**
   ```
   https://titoufu.github.io/Sorvetes/ingredients_master.json
   ```

4. O **site do usuário** lê esse arquivo automaticamente via `config.json`.

---

## 🧠 Lógica do Usuário (Front-End)

**Arquivo principal:** `site/index.html`

### Recursos já implementados

✅ **Presets de receitas:**
- Creme  
- Gelato  
- Fruta  

✅ **Cálculos automáticos:**
- Gordura (%)
- Açúcar (%)
- Sólidos (%)
- Contribuição individual por ingrediente

✅ **Cabeçalho fixo (sticky):**
Mostra gordura/açúcar/sólidos atuais vs alvo.

✅ **Temas:**
- Claro / Suave / Escuro

✅ **Catálogo dinâmico:**
Botão “Adicionar ingrediente (catálogo)” abre **modal** com busca dinâmica em  
[`ingredients_master.json`](https://titoufu.github.io/Sorvetes/ingredients_master.json)

✅ **Configuração centralizada:**
URL do catálogo definida em `config.json`:
```json
{
  "ingredients_catalog_url": "https://titoufu.github.io/Sorvetes/ingredients_master.json"
}
```

✅ **Persistência local (planejada):**
Futura implementação em `localStorage`.

---

## 🧾 Erros Corrigidos

| Problema                              | Causa                           | Solução                          |
| ------------------------------------- | -------------------------------- | -------------------------------- |
| Campos “undefined” no JSON            | Cabeçalhos incorretos no CSV     | Corrigido em `validate.py`       |
| `Cannot read properties of null`      | Modal carregado após script      | Corrigido movendo o modal antes  |
| `sw.js` / `manifest.webmanifest` 404  | Arquivos ausentes                | Adicionados corretamente         |
| Deploy Pages falhou (404)             | GitHub Pages desativado          | Ativado em *Settings → Pages*    |

---

## 🔗 URLs Importantes

| Finalidade            | URL                                                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Página do App         | [https://titoufu.github.io/Sorvetes/?t=now](https://titoufu.github.io/Sorvetes/?t=now)                                   |
| Catálogo JSON         | [https://titoufu.github.io/Sorvetes/ingredients_master.json](https://titoufu.github.io/Sorvetes/ingredients_master.json) |
| Repositório GitHub    | [https://github.com/titoufu/Sorvetes](https://github.com/titoufu/Sorvetes)                                               |
| Pasta Admin Principal | `/admin_scaffold/admin/`                                                                                                 |

---

## 🧱 Próximos Passos

### 🔹 1. Melhorias na Interface

- [ ] Ajustar layout e cores dos botões.  
- [ ] Corrigir espaçamento e responsividade do modal.  
- [ ] Melhorar feedback ao adicionar ingrediente (mensagem ou animação).  

### 🔹 2. Novas Funcionalidades

- [ ] Implementar persistência (`localStorage`) das receitas criadas.  
- [ ] Permitir salvar e nomear “receitas favoritas”.  
- [ ] Adicionar unidades de medida (g, ml, colher, etc.).  
- [ ] Permitir editar/remover ingredientes da lista.  

### 🔹 3. Validação do Catálogo

- [ ] Bloquear duplicatas de ingredientes.  
- [ ] Adicionar campos extras (densidade, categoria detalhada, etc.).  

### 🔹 4. Modo Admin Integrado (futuro)

- [ ] Painel opcional no site para upload direto do `.xlsx` e geração automática do JSON.  

---

## 🚀 Plano de Ação Imediato

| Etapa | Tarefa                                                                 | Responsável | Status |
| ------ | ---------------------------------------------------------------------- | ------------ | ------- |
| 1 | Corrigir espaçamento e centralização do modal de ingredientes | — | ⬜ |
| 2 | Adicionar feedback visual após “Adicionar ingrediente” | — | ⬜ |
| 3 | Implementar `localStorage` para salvar receita atual | — | ⬜ |
| 4 | Criar função “Salvar como favorita” e lista de receitas salvas | — | ⬜ |
| 5 | Atualizar documentação `README_admin.md` com novos campos | — | ⬜ |

---

## 🧭 Observações Finais

- O projeto já está **funcional e estável** no front-end.  
- A estrutura administrativa está automatizada e segura.  
- As próximas etapas visam **melhorar a usabilidade e experiência do usuário** sem alterar a base do fluxo atual.  

---

> 📅 **Última atualização deste documento:** Outubro de 2025  
>  
> ✨ Próxima milestone sugerida: `v1.1.0 — Persistência + UX`  
