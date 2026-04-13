import pytest
from app.pagamentos import calcular_desconto, aplicar_juros_atraso, validar_metodo_pagamento, processar_reembolso

# 1. Teste de Desconto (Opcional, mas bom ter)
def test_calcular_desconto():
    # Arrange
    # Act
    resultado = calcular_desconto(100, 10)
    # Assert
    assert resultado == 90

# 2. Missão 1: Conserto Matemático (Juros 1% ao dia)
def test_aplicar_juros_atraso():
    # Arrange
    # Act
    resultado = aplicar_juros_atraso(100.0, 5)
    # Assert
    assert resultado == 105.0  # Corrigido de 150 para 105

# 3. Missão 3: Valores de Fronteira no Reembolso
def test_processar_reembolso_limites():
    # Arrange
    valor_pago = 200.0
    limite_exato = 200.0  # // Caso de Valor Limite
    estouro = 201.0       # // Caso de Valor Limite
    # Act
    res_sucesso = processar_reembolso(valor_pago, limite_exato)
    res_falha = processar_reembolso(valor_pago, estouro)
    # Assert
    assert res_sucesso != res_falha

# 4. Missão 4: Cobertura de Métodos (Bifurcação)
def test_validar_metodo_pagamento_bifurcacao():
    # Arrange & Act & Assert
    assert validar_metodo_pagamento("pix") is True
    assert validar_metodo_pagamento("cartao_credito") is True
    assert validar_metodo_pagamento("metodo_invalido") is False