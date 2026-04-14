import pytest

from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso,
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
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    # Arrange
    metodo_pix = "pix"
    metodo_cartao_credito = "cartao_credito"
    metodo_cartao_debito = "cartao_debito"
    metodo_boleto = "boleto"
    metodo_invalido = "cheque"
    metodo_invalido_vazio = ""

    # Act
    resultado_pix = validar_metodo_pagamento(metodo_pix)
    resultado_cartao_credito = validar_metodo_pagamento(metodo_cartao_credito)
    resultado_cartao_debito = validar_metodo_pagamento(metodo_cartao_debito)
    resultado_boleto = validar_metodo_pagamento(metodo_boleto)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    resultado_invalido_vazio = validar_metodo_pagamento(metodo_invalido_vazio)

    # Assert
    assert resultado_pix is True
    assert resultado_cartao_credito is True
    assert resultado_cartao_debito is True
    assert resultado_boleto is True
    assert resultado_invalido is False
    assert resultado_invalido_vazio is False


def test_processar_reembolso():
    # Arrange
    valor_pago = 200.00
    valor_reembolso_exato = 200.00  # // Caso de Valor Limite
    valor_reembolso_irregular = 201.00  # // Caso de Valor Limite
    valor_reembolso_parcial = 73.45

    # Act
    resultado_reembolso_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_reembolso_irregular = processar_reembolso(valor_pago, valor_reembolso_irregular)
    resultado_reembolso_parcial = processar_reembolso(valor_pago, valor_reembolso_parcial)

    # Assert
    assert resultado_reembolso_exato == 0.0
    assert resultado_reembolso_irregular == -1
    assert resultado_reembolso_parcial == pytest.approx(126.55)