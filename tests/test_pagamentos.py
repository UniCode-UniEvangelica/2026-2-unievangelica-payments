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
# ÁREA DO ALUNO — Aluno Teste do Prof. Carlos | Matrícula: 99821234
# ====================================================================

def test_calcular_desconto():
    # Teste Correto: 10% de desconto sobre 100 deve ser 90
    assert calcular_desconto(100, 10) == 90
    # Teste Correto: 50% de desconto sobre 200 deve ser 100
    assert calcular_desconto(200, 50) == 100

def test_aplicar_juros_atraso():
    # CORREÇÃO DO BUG: juros simples = valor + (valor * 0.01 * dias)
    # Fórmula: 100 + (100 * 0.01 * 5) = 105.0
    assert aplicar_juros_atraso(100, 5) == 105.0
    assert aplicar_juros_atraso(100, 0) == 100

def test_validar_metodo_pagamento():
    # Arrange + Act + Assert

    # Branch True: métodos aceitos
    assert validar_metodo_pagamento("pix") == True
    assert validar_metodo_pagamento("CARTAO_CREDITO") == True  # case-insensitive

    # Branch False: método rejeitado
    assert validar_metodo_pagamento("cheque") == False
    assert validar_metodo_pagamento("cripto") == False

def test_processar_reembolso():
    # Branch True: reembolso válido (menor ou igual ao pago)
    assert processar_reembolso(200.0, 50.0) == 150.0
    assert processar_reembolso(100.0, 100.0) == 0.0   # valor exato (boundary)

    # Branch False: reembolso inválido → retorna -1
    assert processar_reembolso(100.0, 150.0) == -1
