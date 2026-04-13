import sys
import os

# Adiciona o diretório pai ao sys.path para garantir que o módulo "app" seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

def test_calcular_desconto():
    assert calcular_desconto(100, 10) == 90
    assert calcular_desconto(200, 50) == 100

def test_aplicar_juros_atraso():
    # Bug corrigido: expectativa 105.0 para 1% ao dia
    assert aplicar_juros_atraso(100, 5) == 105.0
    assert aplicar_juros_atraso(100, 0) == 100

def test_validar_metodo_pagamento():
    # Teste de ramos do if/else
    assert validar_metodo_pagamento("pix") == True
    assert validar_metodo_pagamento("cheque") == False
    assert validar_metodo_pagamento("CARTAO_CREDITO") == True

def test_processar_reembolso():
    # Reembolso válido
    assert processar_reembolso(100.0, 30.0) == 70.0
    # Reembolso inválido (regra de negócio)
    assert processar_reembolso(100.0, 150.0) == -1
