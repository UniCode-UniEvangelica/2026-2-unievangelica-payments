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
    assert resultado == 90.0



def test_aplicar_juros_atraso():
    # Arrange
    valor_pago   = 100
    dias_atraso  = 5
    dias_ok      = 0

    # Act
    resultado_com_atraso  = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso  = aplicar_juros_atraso(valor_pago, dias_ok)

    # Assert
    assert resultado_com_atraso == 105.0   # 100 + (100 * 0.01 * 5) = 105.0  ← CORRIGIDO (era 150.0)
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    # Arrange
    metodos_validos   = ["pix", "cartao_credito", "cartao_debito", "boleto"]
    metodos_invalidos = ["cheque", "transferencia", "dinheiro", "crypto", ""]

    # Act
    resultados_validos   = [validar_metodo_pagamento(m) for m in metodos_validos]
    resultados_invalidos = [validar_metodo_pagamento(m) for m in metodos_invalidos]

    # Assert
    assert all(resultados_validos),        "Todos os métodos aceitos devem retornar True"
    assert not any(resultados_invalidos),  "Todos os métodos inválidos devem retornar False"


def test_validar_metodo_pagamento_case_insensitive():
    """Garante que a validação é case-insensitive (ex: 'PIX' == 'pix')."""
    # Arrange
    metodo_maiusculo = "PIX"
    metodo_misto     = "Cartao_Credito"

    # Act
    resultado_maiusculo = validar_metodo_pagamento(metodo_maiusculo)
    resultado_misto     = validar_metodo_pagamento(metodo_misto)

    # Assert
    assert resultado_maiusculo is True
    assert resultado_misto     is True


def test_processar_reembolso_valor_parcial():
    """Reembolso parcial legítimo — saldo restante deve ser calculado corretamente."""
    # Arrange
    valor_pago       = 347.89
    valor_reembolso  = 199.43

    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)

    # Assert
    assert round(resultado, 2) == 148.46


def test_processar_reembolso_valor_limite_exato():  # Caso de Valor Limite
    """Reembolso bate exato no centavo do valor pago — saldo deve ser R$ 0,00."""
    # Arrange
    valor_pago      = 200.00
    valor_reembolso = 200.00  # Caso de Valor Limite

    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)

    # Assert
    assert resultado == 0.00  # Caso de Valor Limite


def test_processar_reembolso_estouro_fronteira():  # Caso de Valor Limite
    """Reembolso ultrapassa R$ 1,00 acima do valor pago — deve sinalizar devolução irregular."""
    # Arrange
    valor_pago      = 200.00
    valor_reembolso = 201.00  # Caso de Valor Limite — estoura a fronteira em R$ 1,00

    # Act
    resultado = processar_reembolso(valor_pago, valor_reembolso)

    # Assert
    assert resultado == -1  # Caso de Valor Limite