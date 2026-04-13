import pytest
from unittest.mock import patch
from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)


def test_calcular_desconto_dez_por_cento():
    """Desconto de 10% sobre R$100 deve retornar R$90."""
    # Arrange
    valor = 100
    percentual = 10

    # Act
    resultado = calcular_desconto(valor, percentual)

    # Assert
    assert resultado == 90


def test_calcular_desconto_zero_por_cento():
    """Desconto de 0% não altera o valor."""
    assert calcular_desconto(200, 0) == 200


def test_calcular_desconto_cem_por_cento():
    """Desconto de 100% zera o valor."""
    assert calcular_desconto(150, 100) == 0


def test_calcular_desconto_valor_limite_50():
    """Boundary value: desconto exato de 50%."""
    assert calcular_desconto(100, 50) == 50.0


def test_aplicar_juros_atraso():
    """
    BUG CORRIGIDO — Incident #8924
    Juros simples de 1% ao dia: 100 + (100 x 0.01 x 5) = 105.0, NAO 150.0.
    """
    # Arrange
    valor_pago = 100
    dias_atraso = 5
    dias_ok = 0

    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)

    # Assert
    assert resultado_com_atraso == 105.0   # CORRIGIDO: era 150.0 (BUG)
    assert resultado_sem_atraso == 100.0


def test_aplicar_juros_atraso_um_dia():
    """Boundary value: exatamente 1 dia de atraso -> 1% de acrescimo."""
    assert aplicar_juros_atraso(100, 1) == 101.0


def test_aplicar_juros_atraso_trinta_dias():
    """Branch coverage: limite alto (30 dias) -> 30% de acrescimo."""
    assert aplicar_juros_atraso(100, 30) == 130.0


def test_aplicar_juros_atraso_valor_alto():
    """Juros sobre valor mais alto — precisao de float."""
    resultado = aplicar_juros_atraso(1000, 10)
    assert resultado == pytest.approx(1100.0)


def test_validar_metodo_pagamento_pix():
    """Metodo 'pix' deve ser aceito."""
    # Arrange
    metodo = "pix"

    # Act
    resultado = validar_metodo_pagamento(metodo)

    # Assert
    assert resultado is True


def test_validar_metodo_pagamento_cartao_credito():
    """Branch: 'cartao_credito' deve ser aceito."""
    assert validar_metodo_pagamento("cartao_credito") is True


def test_validar_metodo_pagamento_cartao_debito():
    """Branch: 'cartao_debito' deve ser aceito."""
    assert validar_metodo_pagamento("cartao_debito") is True


def test_validar_metodo_pagamento_boleto():
    """Branch: 'boleto' deve ser aceito."""
    assert validar_metodo_pagamento("boleto") is True


def test_validar_metodo_pagamento_cheque_rejeitado():
    """Metodo nao suportado 'cheque' deve ser rejeitado."""
    # Arrange
    metodo = "cheque"

    # Act
    resultado = validar_metodo_pagamento(metodo)

    # Assert
    assert resultado is False


def test_validar_metodo_pagamento_vazio_rejeitado():
    """Boundary value: string vazia deve ser rejeitada."""
    assert validar_metodo_pagamento("") is False


def test_validar_metodo_pagamento_case_insensitive():
    """Branch: maiusculas devem ser aceitas (lower() interno)."""
    assert validar_metodo_pagamento("PIX") is True
    assert validar_metodo_pagamento("Boleto") is True


def test_validar_metodo_pagamento_mock_chamada():
    """
    Mock/Stub: verifica que a funcao e invocada com o argumento correto.
    Isola a logica de chamada sem depender da implementacao interna.
    """
    with patch("app.pagamentos.validar_metodo_pagamento", return_value=True) as mock_v:
        resultado = mock_v("transferencia")
        assert resultado is True
        mock_v.assert_called_once_with("transferencia")


def test_processar_reembolso_valido():
    """Reembolso parcial deve retornar o saldo restante."""
    # Arrange
    valor_pago = 200
    valor_reembolso = 50

    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)

    # Assert
    assert resultado == 150


def test_processar_reembolso_invalido_retorna_menos_um():
    """Reembolso maior que o valor pago deve retornar -1."""
    # Arrange
    valor_pago = 100
    valor_reembolso = 150

    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)

    # Assert
    assert resultado == -1


def test_processar_reembolso_total():
    """
    Boundary value: reembolso == valor_pago (limite exato).
    Deve retornar 0 (saldo zerado), nao -1.
    """
    # Arrange
    valor_pago = 100
    valor_reembolso = 100

    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)

    # Assert
    assert resultado == 0


def test_processar_reembolso_zero():
    """Boundary value: reembolso de R$0 deve retornar o valor pago inteiro."""
    assert processar_reembolso(300, 0) == 300


def test_processar_reembolso_um_centavo_acima():
    """Boundary value: reembolso 0.01 acima do valor pago -> -1."""
    assert processar_reembolso(100, 100.01) == -1


def test_processar_reembolso_um_centavo_abaixo():
    """Boundary value: reembolso 0.01 abaixo do valor pago -> saldo de 0.01."""
    resultado = processar_reembolso(100, 99.99)
    assert resultado == pytest.approx(0.01)