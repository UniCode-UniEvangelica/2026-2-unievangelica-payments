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
    # Missão 1 — Conserto Matemático do Legado
    # Arrange
    valor_pago = 100
    dias_atraso = 5
    dias_ok = 0
    
    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)
    
    # Assert
    # CORREÇÃO: O valor esperado foi alterado de 150.0 para 105.0 (1% ao dia)
    assert resultado_com_atraso == 105.0 
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    # Missão 4 — Cobertura Total de Bifurcação
    # Arrange
    metodo_1 = 'pix'
    metodo_2 = 'boleto'  # Trocando para boleto, que é o padrão comum
    metodo_invalido = 'cheque'
    
    # Act
    resultado_pix = validar_metodo_pagamento(metodo_1)
    resultado_boleto = validar_metodo_pagamento(metodo_2)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    # Verificamos se os métodos oficiais retornam True e o proibido retorna False
    assert resultado_pix is True
    assert resultado_boleto is True
    assert resultado_invalido is False

def test_processar_reembolso():
    # Missão 3 — Valores de Fronteira no Reembolso
    # Arrange
    valor_original = 200.00
    reembolso_total = 200.00
    reembolso_abusivo = 201.00
    
    # Act
    sucesso = processar_reembolso(valor_original, reembolso_total)
    erro_estouro = processar_reembolso(valor_original, reembolso_abusivo)
    
    # Assert
    assert sucesso == 0.0 # // Caso de Valor Limite
    assert erro_estouro == -1 # // Caso de Valor Limite