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
    # TODO: Corrigir o erro matemático abaixo (Juros simples de 1% ao dia)
    # 100 + (100 * 0.01 * 5) deveria ser 105.0, não 150.0
    assert resultado_com_atraso == 105.0   # BUG INTENCIONAL
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    # Arrange
    metodo_valido = "pix"
    metodo_valido_maiusculo = "PIX"
    metodo_invalido = "cheque"
    metodo_vazio = ""

    # Act
    resultado_valido = validar_metodo_pagamento(metodo_valido)
    resultado_valido_maiusculo = validar_metodo_pagamento(metodo_valido_maiusculo)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    resultado_vazio = validar_metodo_pagamento(metodo_vazio)

    # Assert
    assert resultado_valido == True
    assert resultado_valido_maiusculo == True
    assert resultado_invalido == False
    assert resultado_vazio == False

def test_processar_reembolso():
    
    # Arrange
    valor_pago = 200
    reembolso_valido = 150
    reembolso_limite = 200      # Caso de Valor Limite
    reembolso_excedente = 201   # Caso de Valor Limite

    # Act
    resultado_valido = processar_reembolso(valor_pago, reembolso_valido)
    resultado_limite = processar_reembolso(valor_pago, reembolso_limite)
    resultado_excedente = processar_reembolso(valor_pago, reembolso_excedente)

    # Assert
    assert resultado_valido == 50
    assert resultado_limite == 0
    assert resultado_excedente == -1