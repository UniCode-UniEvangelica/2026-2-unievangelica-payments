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
    """
    MISSÃO: Implementar testes para validar_metodo_pagamento.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste pelo menos um método aceito (ex: 'pix') e um rejeitado (ex: 'cheque').
    """
    # Arrange
    metodo_valido_1 = "pix"
    metodo_valido_2 = "cartao_credito" # Ajustado de 'cartao' para 'cartao_credito de acordo com a função no caminho app/pagamentos.py'
    metodo_valido_3 = "cartao_debito"
    metodo_invalido = "cheque"
    metodo_vazio = ""

    # Act
    res_pix = validar_metodo_pagamento(metodo_valido_1)
    res_credito = validar_metodo_pagamento(metodo_valido_2)
    res_debito = validar_metodo_pagamento(metodo_valido_3)
    res_cheque = validar_metodo_pagamento(metodo_invalido)
    res_vazio = validar_metodo_pagamento(metodo_vazio)

    # Assert
    assert res_pix is True
    assert res_credito is True
    assert res_debito is True
    assert res_cheque is False
    assert res_vazio is False

def test_processar_reembolso():
    """
    MISSÃO: Implementar testes para processar_reembolso.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste o cenário de reembolso válido e o cenário de erro (-1).
    BÔNUS: Teste o valor limite (reembolso == valor_pago).
    """
    # Arrange
    valor_total = 250.50
    
    valor_limite_exato = 250.50
    valor_estourado = 251.50 # R$ 1.00 acima do limite
    valor_comum = 100.00

    # Act
    resultado_limite = processar_reembolso(valor_total, valor_limite_exato)
    resultado_erro = processar_reembolso(valor_total, valor_estourado)
    resultado_sucesso = processar_reembolso(valor_total, valor_comum)

    # Assert
    assert resultado_limite == 0.00 
    assert resultado_erro == -1 
    assert resultado_sucesso == 150.50