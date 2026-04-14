import sys
import os

# Adiciona o diretório pai ao sys.path para garantir que o módulo 'app' seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

# ====================================================================
# ÁREA DO ALUNO - SOLUÇÃO REFATORADA (MISSÕES 1 A 4)
# ====================================================================

def test_calcular_desconto():
    # Arrange
    valor_normal = 100.0
    taxa_normal = 10.0
    valor_alto = 200.0
    taxa_alta = 25.0
    
    # Act
    resultado_normal = calcular_desconto(valor_normal, taxa_normal)
    resultado_alto = calcular_desconto(valor_alto, taxa_alta)
    
    # Assert
    assert resultado_normal == 90.0
    assert resultado_alto == 150.0


def test_aplicar_juros_atraso():
    # Arrange
    valor_base = 100.0
    dias_com_atraso = 10
    dias_sem_atraso = 0
    
    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_base, dias_com_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_base, dias_sem_atraso)
    
    # Assert
    # Correção: 1% ao dia sobre 100 por 10 dias = R$ 10,00. Total correto = 110.0
    assert resultado_com_atraso == 110.0
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    # Arrange
    metodo_pix = "PIX" # Testando também resiliência a letras maiúsculas
    metodo_cartao = "cartao_credito"
    metodo_invalido_cheque = "cheque"
    metodo_invalido_cripto = "bitcoin"
    
    # Act
    res_pix = validar_metodo_pagamento(metodo_pix)
    res_cartao = validar_metodo_pagamento(metodo_cartao)
    res_cheque = validar_metodo_pagamento(metodo_invalido_cheque)
    res_cripto = validar_metodo_pagamento(metodo_invalido_cripto)
    
    # Assert
    assert res_pix == True
    assert res_cartao == True
    assert res_cheque == False
    assert res_cripto == False


def test_processar_reembolso():
    # Arrange
    valor_pago = 200.0
    valor_reembolso_exato = 200.0
    valor_reembolso_estourado = 201.0
    
    # Act
    resultado_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_estourado = processar_reembolso(valor_pago, valor_reembolso_estourado)
    
    # Assert
    assert resultado_exato == 0.0  # Caso de Valor Limite
    assert resultado_estourado == -1  # Caso de Valor Limite