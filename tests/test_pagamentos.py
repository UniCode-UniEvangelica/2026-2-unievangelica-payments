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
    metodos_aceitos = ["pix", "cartao_credito", "cartao_debito", "boleto"]
    pagamento_invalido = "cheque"
    pagamento_em_branco = ''
    # Act
    
    resultado_invalido = validar_metodo_pagamento(pagamento_invalido)
    resultado_em_branco = validar_metodo_pagamento(pagamento_em_branco)
    # Assert

    for metodo in metodos_aceitos:
        assert validar_metodo_pagamento(metodo) is True

    assert resultado_invalido is False
    assert resultado_em_branco is False
  

def test_processar_reembolso():
    """
    MISSÃO: Implementar testes para processar_reembolso.
    Use a estrutura AAA (Arrange, Act, Assert).
    Dica: Teste o cenário de reembolso válido e o cenário de erro (-1).
    BÔNUS: Teste o valor limite (reembolso == valor_pago).
    """
    # Arrange
    valor_pago = 500
    valor_reembolso_certo = 200
    valor_reembolso_incorreto = 501
    valor_reembolso_limite = 500  #caso valor limite 
    
    # Act
    resultado_certo = processar_reembolso(valor_pago,valor_reembolso_certo)
    resultado_incorreto = processar_reembolso(valor_pago,valor_reembolso_incorreto)
    resutado_limite = processar_reembolso(valor_pago,valor_reembolso_limite)

    # Assert
    assert resultado_certo == 300
    assert resultado_incorreto == -1
    assert resutado_limite == 0
    