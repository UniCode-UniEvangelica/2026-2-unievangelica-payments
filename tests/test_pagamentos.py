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
    dias_minimo = 1
    
    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)
    resultado_atraso_minimo = aplicar_juros_atraso(valor_pago, dias_minimo)
    
    # Assert
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0
    assert resultado_atraso_minimo == 101.0

def test_validar_metodo_pagamento():
    # Arrange
    metodo_aceito = "pix"
    metodo_aceito_case_misto = "CaRtAo_CrEdItO"
    metodo_rejeitado = "cheque"
    
    # Act
    resultado_aceito = validar_metodo_pagamento(metodo_aceito)
    resultado_aceito_case_misto = validar_metodo_pagamento(metodo_aceito_case_misto)
    resultado_rejeitado = validar_metodo_pagamento(metodo_rejeitado)
    
    # Assert
    assert resultado_aceito is True
    assert resultado_aceito_case_misto is True
    assert resultado_rejeitado is False

def test_processar_reembolso():
    # Arrange
    valor_pago = 100.0
    reembolso_valido = 30.0
    reembolso_invalido = 150.0
    reembolso_limite = 100.0
    
    # Act
    resultado_valido = processar_reembolso(valor_pago, reembolso_valido)
    resultado_invalido = processar_reembolso(valor_pago, reembolso_invalido)
    resultado_limite = processar_reembolso(valor_pago, reembolso_limite)
    
    # Assert
    assert resultado_valido == 70.0
    assert resultado_invalido == -1
    assert resultado_limite == 0.0
