## 📋 Identificação do Aluno

> ⚠️ **ATENÇÃO:** PRs sem preenchimento correto desta seção **não serão avaliados.**

| Campo | Valor |
|:---|:---|
| **Nome completo** | <!-- Erick Nepomuceno Ribeiro Silva --> |
| **Matrícula** | <!-- 2310817 --> |
| **Turma** | <!-- B --> |
| **Nome da branch** | <!-- Ex: pratica11/ErickNepomuceno-2310817 --> |

---

## ✅ Checklist de Entrega

Marque todos os itens antes de submeter:

- [x] A branch segue o padrão `pratica11/NomeSobrenome-Matricula`
- [x] O bug de `test_aplicar_juros_atraso` foi identificado e corrigido
- [x] `test_validar_metodo_pagamento` implementado com ≥ 2 asserts (aceito e rejeitado)
- [x] `test_processar_reembolso` implementado com ≥ 2 asserts (válido e -1)
- [x] Todos os testes passam (`python -m pytest tests/test_pagamentos.py -v`)
- [x] Screenshot do terminal com os testes `PASSED` está anexada abaixo

---

## 🖼️ Screenshot dos Testes Passando

> Arraste a imagem aqui ou cole com Ctrl+V. O terminal deve mostrar `X passed` em verde.

![alt text](image.png)

---

## 📝 Explicação Técnica (obrigatório — mínimo 3 frases)

> Não é apenas entregar o código. Explique com suas palavras o que você entendeu.

**1. Por que o teste `test_aplicar_juros_atraso` estava falhando?**

Estava falhando pois o valor esperado na função não era matematicamente lógico de acordo com a porcentagem de juros definida

**2. Qual a diferença entre um Stub e um Mock? Use um exemplo do contexto de pagamentos.**

Um Stub é um objeto simulado que retorna valores pré-definidos, sem verificar como foi utilizado. Ele serve apenas para substituir uma dependência externa e controlar o retorno.

Já um Mock também simula uma dependência, mas além disso, ele verifica interações, como se um método foi chamado, quantas vezes e com quais parâmetros.

**3. O que é Branch Coverage e por que ela é mais rigorosa que Statement Coverage?**

Branch Coverage verifica se todas as decisões do código foram testadas em todos os seus caminhos possíveis.

Já o Statement Coverage verifica apenas se todas as linhas foram executadas pelo menos uma vez.

Ela é mais rigorosa porque não basta executar o código — é preciso garantir que todas as decisões foram realmente testadas, cobrindo diferentes cenários.

---

## 🔗 Referência Bibliográfica usada

> Cite ao menos uma referência (Delamaro, Pytest docs, Martin Fowler, etc.)

DELAMARO, M. Introdução ao Teste de Software. Cap. Caixa-Branca.

---

*Qualquer PR com campos vazios ou sem a explicação técnica será marcado como **incompleto** e não receberá nota.*
