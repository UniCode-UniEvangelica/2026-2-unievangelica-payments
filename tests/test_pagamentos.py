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
    # Correção do bug matemático: 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0 
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    """
    MISSÃO: Implementar testes para validar_metodo_pagamento.
    """
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
    """
    MISSÃO: Implementar testes para processar_reembolso.
    """
    # --- Cenário 1: Reembolso Válido ---
    # Arrange
    valor_pago = 200.0
    valor_reembolso = 50.0
    # Act
    resultado_comum = processar_reembolso(valor_pago, valor_reembolso)
    # Assert
    assert resultado_comum == 150.0 # Sobra no saldo ou confirmação do valor

    # --- Cenário 2: Erro (Reembolso maior que o pago) ---
    # Arrange
    valor_tentativa_abusiva = 300.0
    # Act
    resultado_erro = processar_reembolso(valor_pago, valor_tentativa_abusiva)
    # Assert
    assert resultado_erro == -1

    # --- Cenário 3: Valor Limite ---
    # Act
    resultado_limite = processar_reembolso(valor_pago, valor_pago)
    # Assert
    assert resultado_limite == 0.0