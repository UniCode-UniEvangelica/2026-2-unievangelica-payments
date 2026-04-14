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
    metodo_valido = "pix"
    metodo_invalido = "cheque"
    
    # Act
    resultado_valido = validar_metodo_pagamento(metodo_valido)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    assert resultado_valido is True
    assert resultado_invalido is False


def test_processar_reembolso():
    # Arrange
    valor_pago = 100
    
    # Act
    reembolso_valido = processar_reembolso(valor_pago, 50)
    reembolso_invalido = processar_reembolso(valor_pago, 150)
    reembolso_limite = processar_reembolso(valor_pago, 100)
    
    # Assert
    assert reembolso_valido == 50     
    assert reembolso_invalido == -1   
    assert reembolso_limite == 0     