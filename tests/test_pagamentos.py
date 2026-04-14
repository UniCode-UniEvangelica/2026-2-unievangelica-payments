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
    # 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    # Arrange
    metodo_pix = "pix"
    metodo_credito = "cartao_credito"
    metodo_debito = "cartao_debito"
    metodo_boleto = "boleto"
    metodo_invalido = "cheque"

    # Act
    resultado_pix = validar_metodo_pagamento(metodo_pix)
    resultado_credito = validar_metodo_pagamento(metodo_credito)
    resultado_debito = validar_metodo_pagamento(metodo_debito)
    resultado_boleto = validar_metodo_pagamento(metodo_boleto)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)

    # Assert
    assert resultado_pix is True
    assert resultado_credito is True
    assert resultado_debito is True
    assert resultado_boleto is True
    assert resultado_invalido is False


def test_processar_reembolso():
    # Arrange
    valor_pago = 200
    reembolso_limite = 200      # Caso de Valor Limite
    reembolso_excedido = 201    # Caso de Valor Limite

    # Act
    resultado_limite = processar_reembolso(valor_pago, reembolso_limite)
    resultado_excedido = processar_reembolso(valor_pago, reembolso_excedido)

    # Assert
    assert resultado_limite == 0
    assert resultado_excedido == -1