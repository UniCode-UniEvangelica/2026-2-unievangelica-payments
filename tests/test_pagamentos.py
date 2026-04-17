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
    # Missão 1: Conserto Matemático do Legado
    # 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0 
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    # Arrange
    metodo_valido_1 = "pix"
    metodo_valido_2 = "cartao_credito"
    metodo_invalido = "cheque"
    
    # Act
    resultado_valido_1 = validar_metodo_pagamento(metodo_valido_1)
    resultado_valido_2 = validar_metodo_pagamento(metodo_valido_2)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    assert resultado_valido_1 is True
    assert resultado_valido_2 is True
    assert resultado_invalido is False

def test_processar_reembolso():
    # Arrange
    valor_pago = 200
    valor_reembolso_exato = 200 # // Caso de Valor Limite
    valor_reembolso_vencido = 201 # // Caso de Valor Limite
    
    # Act
    resultado_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_vencido = processar_reembolso(valor_pago, valor_reembolso_vencido)
    
    # Assert
    assert resultado_exato == 0
    assert resultado_vencido == -1
