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
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    # Arrange
    metodo_pix = "pix"
    metodo_cartao_credito = "cartao_credito"
    metodo_cartao_debito = "cartao_debito"
    metodo_boleto = "boleto"
    metodo_maiusculo = "PIX"
    metodo_invalido = "cheque"
    
    # Act
    resultado_pix = validar_metodo_pagamento(metodo_pix)
    resultado_cartao_credito = validar_metodo_pagamento(metodo_cartao_credito)
    resultado_cartao_debito = validar_metodo_pagamento(metodo_cartao_debito)
    resultado_boleto = validar_metodo_pagamento(metodo_boleto)
    resultado_maiusculo = validar_metodo_pagamento(metodo_maiusculo)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    assert resultado_pix is True
    assert resultado_cartao_credito is True
    assert resultado_cartao_debito is True
    assert resultado_boleto is True
    assert resultado_maiusculo is True
    assert resultado_invalido is False

def test_processar_reembolso():
    # Arrange
    valor_pago = 200
    valor_reembolso_valido = 75
    valor_reembolso_limite = 200  # Caso de Valor Limite
    valor_reembolso_invalido = 201  # Caso de Valor Limite
    
    # Act
    resultado_valido = processar_reembolso(valor_pago, valor_reembolso_valido)
    resultado_limite = processar_reembolso(valor_pago, valor_reembolso_limite)
    resultado_invalido = processar_reembolso(valor_pago, valor_reembolso_invalido)
    
    # Assert
    assert resultado_valido == 125
    assert resultado_limite == 0
    assert resultado_invalido == -1