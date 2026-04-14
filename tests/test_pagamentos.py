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
    # Juros simples: valor + (valor × 0.01 × dias)
    # 100 + (100 × 0.01 × 5) = 100 + 5.0 = 105.0  ✅ corrigido (era 150.0)
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    """
    Testa se validar_metodo_pagamento aceita métodos válidos
    e rejeita métodos não suportados.
    """
    # Arrange
    metodo_aceito = "pix"
    metodo_rejeitado = "cheque"

    # Act
    resultado_aceito   = validar_metodo_pagamento(metodo_aceito)
    resultado_rejeitado = validar_metodo_pagamento(metodo_rejeitado)

    # Assert
    assert resultado_aceito   is True   # 'pix' deve ser aceito
    assert resultado_rejeitado is False  # 'cheque' deve ser rejeitado


def test_processar_reembolso():
    """
    processar_reembolso(valor_pago, valor_reembolso) retorna o SALDO RESTANTE,
    ou seja: valor_pago - valor_reembolso.
    Retorna -1 quando o reembolso solicitado excede o valor pago.
    """
    # ── Cenário 1: reembolso parcial válido ──────────────────────────
    # Arrange
    valor_pago      = 200.0
    valor_reembolso = 50.0

    # Act
    resultado_valido = processar_reembolso(valor_pago, valor_reembolso)

    # Assert — saldo restante: 200 - 50 = 150.0
    assert resultado_valido == 150.0

    # ── Cenário 2 (BÔNUS): valor-limite — reembolso == valor pago ────
    # Arrange
    reembolso_total = 200.0

    # Act
    resultado_limite = processar_reembolso(valor_pago, reembolso_total)

    # Assert — saldo restante: 200 - 200 = 0.0
    assert resultado_limite == 0.0

    # ── Cenário 3: reembolso inválido (maior que o valor pago) ───────
    # Arrange
    reembolso_invalido = 300.0

    # Act
    resultado_erro = processar_reembolso(valor_pago, reembolso_invalido)

    # Assert
    assert resultado_erro == -1