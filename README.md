# 2026-2-unievangelica-payments-7ob

Atividade de testes unitários para o sistema de pagamentos.

## Estrutura do Projeto

- `app/pagamentos.py`: Módulo principal com funções de cálculo de desconto, juros, validação de pagamento e processamento de reembolso.
- `tests/test_pagamentos.py`: Arquivo de testes unitários usando pytest.

## Como executar os testes

1. Ative o ambiente virtual (se aplicável):
   ```
   source .venv/bin/activate
   ```

2. Instale as dependências (se necessário):
   ```
   pip install pytest
   ```

3. Execute os testes:
   ```
   python -m pytest tests/test_pagamentos.py -v
   ```

## ⚠️ O Retorno ao Ciclo 01 (Flashback)

Se você observar o arquivo `tests/test_pagamentos.py`, vai perceber um *Déjà vu*. A mesma falha de cálculo matemático do "Juros de Atraso" (que vimos no Ciclo 01) continua assombrando a ramificação `main` deste repositório! 

**Sua missão no Ciclo 02 (Turma 7oB):** 
Não basta apenas "fazer o teste passar" como fizemos de forma iniciante. Agora você aplicará o rigor da **Engenharia de Teste Unitário**:
- Cobertura de Decisão Lógica (Branch Coverage)
- Análise de Valor Limite (Boundary Value)
- Isolamento contra serviços externos (Mock/Stub)
- Testes de Integração Persistida (SQLite em Memória)

Abra o arquivo de testes, extermine esse bug histórico e construa a malha de testes impenetrável da Aula 11!