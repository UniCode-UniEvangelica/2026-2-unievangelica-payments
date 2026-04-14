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
    # Correção: juros simples de 1% ao dia
    # 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    # Arrange
    metodo_valido = "pix"
    metodo_valido_case = "PIX"
    metodo_invalido = "cheque"
    
    # Act
    resultado_valido = validar_metodo_pagamento(metodo_valido)
    resultado_valido_case = validar_metodo_pagamento(metodo_valido_case)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    assert resultado_valido is True
    assert resultado_valido_case is True
    assert resultado_invalido is False


def test_processar_reembolso():
    # Arrange
    valor_pago = 200
    reembolso_valido = 50
    reembolso_limite = 200   # Caso de Valor Limite
    reembolso_excedido = 201 # Caso de Valor Limite
    
    # Act
    resultado_valido = processar_reembolso(valor_pago, reembolso_valido)
    resultado_limite = processar_reembolso(valor_pago, reembolso_limite)
    resultado_excedido = processar_reembolso(valor_pago, reembolso_excedido)
    
    # Assert
    assert resultado_valido == 150
    assert resultado_limite == 0
    assert resultado_excedido == -1
