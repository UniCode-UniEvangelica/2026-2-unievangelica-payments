import sys
import os

# Adiciona o diretório pai ao sys.path para garantir que o módulo 'app' seja encontrado,
# independente da pasta de onde o aluno rode o pytest.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

# ====================================================================
# ÁREA DO ALUNO
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
    valor_com_atraso = 100
    dias_atraso = 5

    valor_sem_atraso = 100
    dias_sem_atraso = 0

    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_com_atraso, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_sem_atraso, dias_sem_atraso)

    # Assert
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100


def test_validar_metodo_pagamento():
    # Arrange
    metodo_valido_1 = "pix"
    metodo_valido_2 = "cartao_credito"
    metodo_invalido_1 = "cheque"
    metodo_invalido_2 = "dinheiro"

    # Act
    resultado_valido_1 = validar_metodo_pagamento(metodo_valido_1)
    resultado_valido_2 = validar_metodo_pagamento(metodo_valido_2)
    resultado_invalido_1 = validar_metodo_pagamento(metodo_invalido_1)
    resultado_invalido_2 = validar_metodo_pagamento(metodo_invalido_2)

    # Assert
    assert resultado_valido_1 is True
    assert resultado_valido_2 is True
    assert resultado_invalido_1 is False
    assert resultado_invalido_2 is False


def test_processar_reembolso():
    # Arrange
    valor_pago_limite = 200
    valor_reembolso_limite = 200  # Caso de Valor Limite

    valor_pago_excedido = 200
    valor_reembolso_excedido = 201  # Caso de Valor Limite

    # Act
    resultado_limite = processar_reembolso(valor_pago_limite, valor_reembolso_limite)
    resultado_excedido = processar_reembolso(valor_pago_excedido, valor_reembolso_excedido)

    # Assert
    assert resultado_limite == 0
    assert resultado_excedido == -1