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
    # 100 + (100 * 0.01 * 5) deveria ser 105.0, não 150.02
    assert resultado_com_atraso == 105  # BUG INTENCIONAL
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
    """
    MISSÃO: Implementar testes para validar_metodo_pagamento.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste pelo menos um método aceito (ex: 'pix') e um rejeitado (ex: 'cheque').
    """
    # Arrange
    metodo = "pix"
    # Act
    resultado = validar_metodo_pagamento(metodo)
    # Assert
    assert resultado == True

def test_validar_metodo_pagamento_rejeitado():
    # Arrange
    metodo = "cheque"
    # Act
    resultado = validar_metodo_pagamento(metodo)
    # Assert
    assert resultado == False
    pass

def test_processar_reembolso():
    """
    MISSÃO: Implementar testes para processar_reembolso.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste o cenário de reembolso válido e o cenário de erro (-1).
    BÔNUS: Teste o valor limite (reembolso == valor_pago).
    """
def test_processar_reembolso_valido():

    # Arrange
    valor_pago = 100
    valor_reembolso = 50    
    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)
    # Assert
    assert resultado == 50
    pass

def test_processar_reembolso_invalido():
    # Arrange
    valor_pago = 100
    valor_reembolso = 150    
    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)
    # Assert
    assert resultado == -1
    pass

def test_processar_reembolso_limite(self):
    # Arrange
    valor_pago = 200
    reembolso_exato = 200
    reembolso_estouro = 201

    # Act
    resultado_exato = processar_reembolso(valor_pago, reembolso_exato)
    resultado_estouro = processar_reembolso(valor_pago, reembolso_estouro)
    # Assert
    assert resultado_exato == 0  #Caso de Valor Limite
    assert resultado_estouro == -1  #Caso de Valor Limitw
    pass