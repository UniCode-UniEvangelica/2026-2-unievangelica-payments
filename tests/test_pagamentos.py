import sys
import os

# Garante que o módulo 'app' seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

# ====================================================================
# TESTES
# ====================================================================

def test_calcular_desconto():
    # Arrange
    valor1 = 100
    taxa1 = 10

    valor2 = 200
    taxa2 = 50

    # Act
    resultado1 = calcular_desconto(valor1, taxa1)
    resultado2 = calcular_desconto(valor2, taxa2)

    # Assert
    assert resultado1 == 90
    assert resultado2 == 100


def test_aplicar_juros_atraso():
    # Arrange
    valor = 100
    dias_atraso = 5

    valor_sem_atraso = 100
    dias_sem_atraso = 0

    # Act
    resultado = aplicar_juros_atraso(valor, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_sem_atraso, dias_sem_atraso)

    # Assert
    assert resultado == 105.0   # CORREÇÃO DO BUG
    assert resultado_sem_atraso == 100


def test_validar_metodo_pagamento():
    # Arrange
    metodo1 = "pix"
    metodo2 = "cartao_credito"
    metodo3 = "cartao_debito"
    metodo4 = "boleto"

    metodo_invalido1 = "cheque"
    metodo_invalido2 = "dinheiro"

    # Act
    resultado1 = validar_metodo_pagamento(metodo1)
    resultado2 = validar_metodo_pagamento(metodo2)
    resultado3 = validar_metodo_pagamento(metodo3)
    resultado4 = validar_metodo_pagamento(metodo4)

    resultado_invalido1 = validar_metodo_pagamento(metodo_invalido1)
    resultado_invalido2 = validar_metodo_pagamento(metodo_invalido2)

    # Assert
    assert resultado1 is True
    assert resultado2 is True
    assert resultado3 is True
    assert resultado4 is True

    assert resultado_invalido1 is False
    assert resultado_invalido2 is False


def test_processar_reembolso():
    # Arrange
    valor_pago = 200
    valor_reembolso_exato = 200  # Caso de Valor Limite

    valor_pago2 = 200
    valor_reembolso_excedido = 201  # Caso de Valor Limite

    # Act
    resultado_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_excedido = processar_reembolso(valor_pago2, valor_reembolso_excedido)

    # Assert
    assert resultado_exato == 0
    assert resultado_excedido == -1