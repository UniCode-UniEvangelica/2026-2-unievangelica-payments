## 📋 Identificação do Aluno

> ⚠️ **ATENÇÃO:** PRs sem preenchimento correto desta seção **não serão avaliados.**

| Campo | Valor |
|:---|:---|
| **Nome completo** | <!-- Ex: João da Silva Souza --> |
| **Matrícula** | <!-- Ex: 2024001234 --> |
| **Turma** | <!-- A (Segundas) ou B (Quintas) --> |
| **Nome da branch** | <!-- Ex: pratica11/JoaoSilva-2024001234 --> |

---

## ✅ Checklist de Entrega

Marque todos os itens antes de submeter:

- [ ] A branch segue o padrão `pratica11/NomeSobrenome-Matricula`
- [ ] O bug de `test_aplicar_juros_atraso` foi identificado e corrigido
- [ ] `test_validar_metodo_pagamento` implementado com ≥ 2 asserts (aceito e rejeitado)
- [ ] `test_processar_reembolso` implementado com ≥ 2 asserts (válido e -1)
- [ ] Todos os testes passam (`python -m pytest tests/test_pagamentos.py -v`)
- [ ] Screenshot do terminal com os testes `PASSED` está anexada abaixo

---

## 🖼️ Screenshot dos Testes Passando

> Arraste a imagem aqui ou cole com Ctrl+V. O terminal deve mostrar `X passed` em verde.

<!-- Cole a imagem aqui -->

---

## 📝 Explicação Técnica (obrigatório — mínimo 3 frases)

> Não é apenas entregar o código. Explique com suas palavras o que você entendeu.

**1. Por que o teste `test_aplicar_juros_atraso` estava falhando?**

O teste falhava pois o resultado esperado era diferente do que a função retornava, que por sinal estava correto. A solução foi corrigir o teste para que ficasse de acordo com o valor esperado da função. Corrigindo isso conseguimos fazer com que o teste passa-se e que ficasse condizente com o que a função pedia.

**2. Qual a diferença entre um Stub e um Mock? Use um exemplo do contexto de pagamentos.**

Um Stub é uma substituição simples de uma dependência externa que apenas retorna um valor fixo, sem verificar como foi chamado. Um Mock além de substituir a dependência, ele também verifica se foi chamado corretamente, com quais argumentos e quantas vezes.

No contexto de pagamentos, um Stub seria substituir a função validar_metodo_pagamento para sempre retornar True, sem se preocupar em como ela foi chamada — apenas garantindo que o restante do fluxo funcione. Já um Mock seria verificar, por exemplo, se processar_reembolso foi chamado exatamente uma vez com os argumentos corretos (valor_pago=150, reembolso=150), garantindo que a lógica de negócio acionou a função no momento certo.

**3. O que é Branch Coverage e por que ela é mais rigorosa que Statement Coverage?**

Statement Coverage verifica se cada linha de código foi executada ao menos uma vez durante os testes. Já o Branch Coverage verifica se cada possível caminho de uma decisão (if/else) foi testado, tanto o caminho verdadeiro quanto o falso.

Por exemplo, na função aplicar_juros_atraso, um único teste com dias_atraso=5 garante 100% de Statement Coverage, pois a linha de juros é executada. Porém, o Branch Coverage exige que também se teste dias_atraso=0, cobrindo o caminho em que não há atraso. Por isso o Branch Coverage é mais rigoroso: ele encontra bugs que ficam escondidos em caminhos alternativos do código que o Statement Coverage simplesmente ignora.

---

## 🔗 Referência Bibliográfica usada

> Cite ao menos uma referência (Delamaro, Pytest docs, Martin Fowler, etc.)

<!-- Ex: DELAMARO, M. Introdução ao Teste de Software. Cap. Caixa-Branca. -->

---

*Qualquer PR com campos vazios ou sem a explicação técnica será marcado como **incompleto** e não receberá nota.*
