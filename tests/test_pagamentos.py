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
    assert resultado_com_atraso == 105.0   # corrigido
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    """
    MISSÃO: Implementar testes para validar_metodo_pagamento.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste pelo menos um método aceito (ex: 'pix') e um rejeitado (ex: 'cheque').
    """
    # Arrange
    metodo_aceito = 'pix'
    metodo_rejeitado = 'cheque'
    
    # Act
    resultado_aceito = validar_metodo_pagamento(metodo_aceito)
    resultado_rejeitado = validar_metodo_pagamento(metodo_rejeitado)

    # Assert
    assert resultado_aceito == True
    assert resultado_rejeitado == False

def test_processar_reembolso():
    """
    MISSÃO: Implementar testes para processar_reembolso.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste o cenário de reembolso válido e o cenário de erro (-1).
    BÔNUS: Teste o valor limite (reembolso == valor_pago).
    """
    # Arrange
    valor_pago = 100
    valor_reembolso = 50
        
    # Act
    resultado_valido = processar_reembolso(valor_pago, valor_reembolso)
    resultado_invalido = processar_reembolso(valor_pago, valor_pago + valor_reembolso)
    resultado_limite = processar_reembolso(valor_pago, valor_pago)
    
    # Assert
    assert resultado_valido == 50
    assert resultado_invalido == -1
    assert resultado_limite == 0
