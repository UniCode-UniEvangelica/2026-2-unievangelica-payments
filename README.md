# 🧪 ShopFast — Engenharia de Testes (Aula 11)

> **Missão QA Automation:** O sistema foi a produção com bugs. Seu trabalho é construir a malha de testes que impedirá que isso aconteça novamente.

---

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── pagamentos.py       # Funções de pagamento (desconto, juros, validação, reembolso)
│   └── carrinho_db.py      # Módulo de carrinho com persistência SQLite
├── tests/
│   ├── test_pagamentos.py        # Testes Unitários (Atividade Principal)
│   └── test_carrinho_integracao.py  # Testes de Integração — Lab Extra (SQLite :memory:)
└── .github/
    ├── workflows/
    │   ├── run-tests.yml      # CI: executa pytest a cada PR
    │   └── validate-pr.yml   # CI: valida padrão de branch e título do PR
    └── PULL_REQUEST_TEMPLATE.md
```

---

## ⚙️ Como executar os testes

### 1. Clone e configure o ambiente

```bash
git clone https://github.com/UniCode-UniEvangelica/2026-2-unievangelica-payments.git
cd 2026-2-unievangelica-payments
pip install pytest
```

### 2. Testes Unitários (Atividade Principal — `pratica11/`)

```bash
python -m pytest tests/test_pagamentos.py -v
```

> ⚠️ **Atenção:** Um teste vai falhar — isso é intencional. Sua missão é identificar e corrigir o bug.

### 3. Testes de Integração (Lab Extra — `lab11-extra/`)

```bash
python -m pytest tests/test_carrinho_integracao.py -v
```

> Os testes de integração usam um banco **SQLite em memória** (`:memory:`). Nenhuma instalação adicional é necessária.

### 4. Rodar tudo junto

```bash
python -m pytest -v
```

---

## ⚠️ O Bug Histórico (Incident Report #8924)

Se você abrir `tests/test_pagamentos.py`, vai encontrar um *Déjà vu* do Ciclo 01: a mesma falha de cálculo de **Juros de Atraso** continua assombrando a branch `main`.

**Sua missão no Ciclo 02** vai além de "fazer o teste passar":

| Técnica | Aplicação |
|:--|:--|
| 🔀 **Branch Coverage** | Cobrir todos os caminhos de `if/else` |
| 📏 **Boundary Value** | Testar os limites exatos dos valores |
| 🤖 **Mock/Stub** | Isolar dependências externas |
| 🗄️ **Integração Persistida** | Testar com SQLite real em memória |

---

## 📤 Como entregar (Pull Request via Fork)

> ⚠️ **O repositório é da organização UniCode-UniEvangelica. Você não tem permissão de escrita direta.** Por isso, o fluxo correto é via **Fork**.

### Passo 1 — Faça o Fork do repositório

1. Acesse: [https://github.com/UniCode-UniEvangelica/2026-2-unievangelica-payments](https://github.com/UniCode-UniEvangelica/2026-2-unievangelica-payments)
2. Clique no botão **Fork** (canto superior direito)
3. Confirme o fork para a **sua conta pessoal** do GitHub

### Passo 2 — Clone o SEU fork (não o original)

```bash
git clone https://github.com/SEU_USERNAME/2026-2-unievangelica-payments.git
cd 2026-2-unievangelica-payments
```

> ⚠️ Substitua `SEU_USERNAME` pelo seu usuário do GitHub.

### Passo 3 — Crie sua branch com o padrão obrigatório

```bash
git checkout -b pratica11/NomeSobrenome-Matricula
# Exemplo: git checkout -b pratica11/JoaoSilva-2024001
```

### Passo 4 — Implemente e teste localmente

```bash
pip install pytest
python -m pytest tests/test_pagamentos.py -v
```

### Passo 5 — Faça commit e push para o **seu fork**

```bash
git add tests/test_pagamentos.py
git commit -m "feat(pratica11): implementa estrutura AAA e valores limite"
git push origin pratica11/NomeSobrenome-Matricula
```

### Passo 6 — Abra o Pull Request para o repositório original

1. Acesse o **seu fork** no GitHub
2. Clique no botão **"Compare & pull request"** que aparecerá automaticamente
3. Verifique que o PR aponta de:
   - **base repository:** `UniCode-UniEvangelica/2026-2-unievangelica-payments` → `main`
   - **head repository:** `SEU_USERNAME/2026-2-unievangelica-payments` → `pratica11/NomeSobrenome-Matricula`
4. Título do PR deve conter `[Aula 11]` — ex: `[Aula 11] Pratica11/JoaoSilva-2024001`
5. Preencha o template do PR completamente — PRs incompletos não são avaliados

> **Lab Extra:** Para o laboratório de integração, use o prefixo `lab11-extra/NomeSobrenome-Matricula`

---

## 🏆 Critérios de Avaliação (1,0 pt)

| Critério | Peso |
|:--|:--|
| Bug do `test_aplicar_juros_atraso` corrigido (valor = 105.0) | 0,25 pt |
| Estrutura AAA explícita (`# Arrange`, `# Act`, `# Assert`) | 0,25 pt |
| `test_processar_reembolso` com casos de Valor Limite | 0,25 pt |
| Branch `pratica11/Nome-Matricula` + CI verde | 0,25 pt |
| **Total** | **1,0 pt** |

---

*Esp. Carlos Roberto Gomes Júnior | Teste de Software — Ciclo 02 | UniEvangelica*