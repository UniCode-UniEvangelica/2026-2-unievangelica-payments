import pytest
from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

# ==============================
# MISSÃO 1
# ==============================

def test_aplicar_juros_atraso():
    # Arrange
    valor_pago = 100
    dias_atraso = 5
    dias_ok = 0

    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)

    # Assert
    assert resultado_com_atraso == 105.0  # Correção matemática: 1% ao dia
    assert resultado_sem_atraso == 100.0





def test_calcular_desconto():
    # Arrange
    valor = 100
    percentual = 10

    # Act
    resultado = calcular_desconto(valor, percentual)

    # Assert
    assert resultado == 90.0


# ==============================
# MISSÃO 4 — COBERTURA TOTAL
# ==============================

def test_validar_metodo_pagamento():
    # Arrange
    metodos_validos = ["pix", "cartao_credito", "cartao_debito", "boleto"]
    metodos_invalidos = ["cheque", "dinheiro", "crypto", ""]

    # Act
    resultados_validos = [validar_metodo_pagamento(m) for m in metodos_validos]
    resultados_invalidos = [validar_metodo_pagamento(m) for m in metodos_invalidos]

    # Assert
    assert all(resultados_validos)       # Todos válidos devem retornar True
    assert not any(resultados_invalidos) # Nenhum inválido deve retornar True


# ==============================
# MISSÃO 3 — FRONTEIRA
# ==============================

def test_processar_reembolso():
    # Arrange
    valor_pago = 200.00
    reembolso_limite = 200.00     # Caso de Valor Limite
    reembolso_estouro = 201.00    # Caso de Valor Limite

    # Act
    resultado_limite = processar_reembolso(valor_pago, reembolso_limite)
    resultado_estouro = processar_reembolso(valor_pago, reembolso_estouro)

    # Assert
    assert resultado_limite == 0.00   # Caso de Valor Limite
    assert resultado_estouro == -1    # Caso de Valor Limite
