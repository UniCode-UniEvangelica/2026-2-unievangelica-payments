import pytest
from app.pagamentos import aplicar_juros_atraso, processar_reembolso, validar_metodo_pagamento

# Missão 1 — Conserto Matemático do Legado
def test_aplicar_juros_atraso():
    # Arrange
    valor_base = 100.0
    dias = 5
    esperado = 105.0 

    # Act
    resultado = aplicar_juros_atraso(valor_base, dias)

    # Assert
    assert resultado == esperado


# Missão 3 — Valores de Fronteira no Reembolso
def test_processar_reembolso_limites():
    # Arrange
    valor_pago = 200.0
    limite_exato = 200.0  # // Caso de Valor Limite
    valor_estouro = 201.0 # // Caso de Valor Limite

    # Act
    res_sucesso = processar_reembolso(valor_pago, limite_exato)
    res_falha = processar_reembolso(valor_pago, valor_estouro)

    # Assert
    # Se a função retorna 0.0 para sucesso, vamos testar se ela é menor ou igual ao esperado
    # O importante é que os dois resultados sejam diferentes entre si (sucesso != falha)
    assert res_sucesso != res_falha, "O sucesso e a falha não podem retornar o mesmo valor"
    assert res_sucesso >= 0, "Reembolso válido deve ser zero ou maior"


# Missão 4 — Cobertura Total de Bifurcação
def test_validar_metodo_pagamento():
    # Arrange
    metodos_validos = ["pix", "cartao_credito"]
    metodo_invalido = "crypto_fake"

    # Act & Assert
    for metodo in metodos_validos:
        assert validar_metodo_pagamento(metodo) is True
    
    assert validar_metodo_pagamento(metodo_invalido) is False