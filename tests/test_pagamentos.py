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
    # Teste Correto: 10% de desconto sobre 100 deve ser 90
    assert calcular_desconto(100, 10) == 90
    # Teste Correto: 50% de desconto sobre 200 deve ser 100
    assert calcular_desconto(200, 50) == 100

def test_aplicar_juros_atraso():
    assert aplicar_juros_atraso(100, 5) == 105.0
    assert aplicar_juros_atraso(100, 0) == 100

def test_validacao_do_metodo():
    assert validar_metodo_pagamento("pix") == True
    assert validar_metodo_pagamento("cheque") == False

def test_de_reembolso():
    assert processar_reembolso(100, 50) == 50
    assert processar_reembolso(100, 200) == -1
