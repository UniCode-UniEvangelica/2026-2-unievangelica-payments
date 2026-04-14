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
    metodo_aceito = "pix"
    metodo_rejeitado = "cheque"
    
    # Act
    resultado_aceito = validar_metodo_pagamento(metodo_aceito)
    resultado_rejeitado = validar_metodo_pagamento(metodo_rejeitado)
    
    # Assert
    assert resultado_aceito is True
    assert resultado_rejeitado is False

def test_processar_reembolso():
    # Arrange
    valor_pago = 200.0
    reembolso_exato = 200.0
    reembolso_estourado = 201.0
    
    # Act
    resultado_exato = processar_reembolso(valor_pago, reembolso_exato)
    resultado_estourado = processar_reembolso(valor_pago, reembolso_estourado)
    
    # Assert
    assert resultado_exato == 0.0  # // Caso de Valor Limite
    assert resultado_estourado == -1  # // Caso de Valor Limite
