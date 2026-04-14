import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
    # CORRIGIDO: 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0

def test_validar_metodo_pagamento():
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
    # Arrange
    valor_total = 200.0
    valor_reembolso_valido = 50.0
    valor_reembolso_limite = 200.0
    valor_reembolso_maior = 250.0
    
    # Act
    res_sucesso = processar_reembolso(valor_total, valor_reembolso_valido)
    res_limite = processar_reembolso(valor_total, valor_reembolso_limite)
    res_erro = processar_reembolso(valor_total, valor_reembolso_maior)
    
    # Assert
    assert res_sucesso == 150.0  # Saldo restante após reembolso
    assert res_limite == 0.0     # Reembolso total
    assert res_erro == -1        # Erro por tentar reembolsar mais que o pago