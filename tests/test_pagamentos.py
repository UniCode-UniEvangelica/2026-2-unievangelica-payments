import pytest
from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

def test_calcular_desconto():
    # Arrange
    valor = 100
    percentual = 10

    # Act
    resultado = calcular_desconto(valor, percentual)

    # Assert
    assert resultado == 90

def test_aplicar_juros_atraso():
    # Arrange
    valor_pago = 100
    dias_atraso = 5
    dias_ok = 0

    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)

    # Assert
    # Juros simples de 1% ao dia: 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    # Arrange
    metodo_pix = "pix"
    metodo_cartao_credito = "cartao_credito"
    metodo_cartao_debito = "cartao_debito"
    metodo_boleto = "boleto"
    metodo_cheque = "cheque"
    metodo_cripto = "criptomoeda"

    # Act
    resultado_pix = validar_metodo_pagamento(metodo_pix)
    resultado_cartao_credito = validar_metodo_pagamento(metodo_cartao_credito)
    resultado_cartao_debito = validar_metodo_pagamento(metodo_cartao_debito)
    resultado_boleto = validar_metodo_pagamento(metodo_boleto)
    resultado_cheque = validar_metodo_pagamento(metodo_cheque)
    resultado_cripto = validar_metodo_pagamento(metodo_cripto)

    # Assert
    assert resultado_pix == True
    assert resultado_cartao_credito == True
    assert resultado_cartao_debito == True
    assert resultado_boleto == True
    assert resultado_cheque == False
    assert resultado_cripto == False

def test_processar_reembolso():
    # Arrange
    valor_pago = 200.00
    reembolso_exato = 200.00       # // Caso de Valor Limite
    reembolso_irregular = 201.00   # // Caso de Valor Limite

    # Act
    resultado_exato = processar_reembolso(valor_pago, reembolso_exato)          # // Caso de Valor Limite
    resultado_irregular = processar_reembolso(valor_pago, reembolso_irregular)  # // Caso de Valor Limite

    # Assert
    assert resultado_exato == 0.00         # // Caso de Valor Limite
    assert resultado_irregular == -1       # // Caso de Valor Limite
