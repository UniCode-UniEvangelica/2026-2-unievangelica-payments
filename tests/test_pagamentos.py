import pytest
from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)
import sqlite3

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
    assert resultado_com_atraso == 105.0   # corrigido
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    # Arrange
    metodo_valido_pix = "pix"
    metodo_valido_cartao_credito = "cartao_credito"
    metodo_valido_cartao_debito = "cartao_debito"
    metodo_valido_boleto = "boleto"
    metodo_invalido = "cheque"
    metodo_vazio = ""
    
    # Act
    resultado_pix = validar_metodo_pagamento(metodo_valido_pix)
    resultado_cartao_credito = validar_metodo_pagamento(metodo_valido_cartao_credito)
    resultado_cartao_debito = validar_metodo_pagamento(metodo_valido_cartao_debito)
    resultado_boleto = validar_metodo_pagamento(metodo_valido_boleto)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    resultado_vazio = validar_metodo_pagamento(metodo_vazio)
    
    # Assert
    assert resultado_pix is True
    assert resultado_cartao_credito is True
    assert resultado_cartao_debito is True
    assert resultado_boleto is True
    assert resultado_invalido is False
    assert resultado_vazio is False


def test_processar_reembolso():
    # Arrange
    valor_pago = 200
    valor_reembolso_valido = 100
    valor_reembolso_exato = 200   # Caso de Valor Limite (reembolso = pagamento)
    valor_reembolso_invalido = 201  # Caso de Valor Limite (reembolso > pagamento)
    
    # Act
    resultado_valido = processar_reembolso(valor_pago, valor_reembolso_valido)
    resultado_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_invalido = processar_reembolso(valor_pago, valor_reembolso_invalido)
    
    # Assert
    assert resultado_valido == 100  # 200 - 100 = 100 (saldo restante)
    assert resultado_exato == 0     # 200 - 200 = 0 (reembolso integral)
    assert resultado_invalido == -1  # Reembolso inválido


# =====================================================================
# TESTES EXPANDIDOS — Cobertura de agências (if/else), Valores Limite
# =====================================================================

def test_calcular_desconto_valores_limite():
    """Testa desconto com valores limite (zero, 100%, etc)."""
    # Sem desconto (0%)
    assert calcular_desconto(100, 0) == 100
    
    # Desconto total (100%)
    assert calcular_desconto(100, 100) == 0
    
    # Valor zero
    assert calcular_desconto(0, 10) == 0
    
    # Desconto pequeno
    assert calcular_desconto(100, 1) == 99
    
    # Valor grande com desconto pequeno  
    assert calcular_desconto(1000, 5) == 950


def test_aplicar_juros_atraso_valores_limite():
    """Testa juros de atraso com diferentes dias e valores."""
    # Nenhum atraso (dias = 0)
    assert aplicar_juros_atraso(100, 0) == 100
    
    # Um dia de atraso (1% = 1 real)
    assert aplicar_juros_atraso(100, 1) == 101
    
    # Valor zero
    assert aplicar_juros_atraso(0, 5) == 0
    
    # Valor grande com atraso grande
    assert aplicar_juros_atraso(1000, 10) == 1100  # 1000 + (1000 * 0.01 * 10)
    
    # Atraso de 30 dias (30%)
    assert aplicar_juros_atraso(100, 30) == 130


def test_validar_metodo_pagamento_case_insensitive():
    """Testa se a validação é case-insensitive."""
    # Maiúsculas
    assert validar_metodo_pagamento("PIX") is True
    assert validar_metodo_pagamento("CARTAO_CREDITO") is True
    
    # Mistas
    assert validar_metodo_pagamento("Boleto") is True
    assert validar_metodo_pagamento("CarTao_Debito") is True


def test_processar_reembolso_valores_limite():
    """Testa reembolso com valores extremos."""
    # Reembolso zero
    assert processar_reembolso(100, 0) == 100
    
    # Valor pago zero com reembolso zero
    assert processar_reembolso(0, 0) == 0
    
    # Valor pago com reembolso um centavo a mais (limite)
    assert processar_reembolso(100, 100.01) == -1
    
    # Reembolso parcial pequeno
    assert processar_reembolso(100, 1) == 99


# =====================================================================
# TESTE DE INTEGRAÇÃO — Persistência em SQLite :memory:
# =====================================================================

@pytest.fixture
def db_transacao():
    """Fixture que cria banco de dados SQLite em memória para testes."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    
    # Cria tabela de transações de pagamento
    cur.execute("""
        CREATE TABLE transacoes_pagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_original REAL NOT NULL,
            tipo_operacao TEXT NOT NULL,
            valor_final REAL NOT NULL,
            parametro TEXT
        )
    """)
    conn.commit()
    
    yield conn
    
    conn.close()


def test_integracao_transacoes_desconto(db_transacao):
    """Testa desconto persisted no banco de dados."""
    # Arrange
    cur = db_transacao.cursor()
    valor_original = 100
    taxa_desconto = 10
    valor_com_desconto = calcular_desconto(valor_original, taxa_desconto)
    
    # Act
    cur.execute("""
        INSERT INTO transacoes_pagamento (valor_original, tipo_operacao, valor_final, parametro)
        VALUES (?, ?, ?, ?)
    """, (valor_original, "desconto", valor_com_desconto, f"{taxa_desconto}%"))
    db_transacao.commit()
    
    # Assert
    cur.execute("SELECT valor_final FROM transacoes_pagamento WHERE tipo_operacao = 'desconto'")
    resultado = cur.fetchone()[0]
    assert resultado == 90
    
    # Verifica persistência (query novamente)
    cur.execute("SELECT COUNT(*) FROM transacoes_pagamento")
    assert cur.fetchone()[0] == 1


def test_integracao_transacoes_juros(db_transacao):
    """Testa juros de atraso persistidos no banco de dados."""
    # Arrange
    cur = db_transacao.cursor()
    valor_original = 100
    dias_atraso = 5
    valor_com_juros = aplicar_juros_atraso(valor_original, dias_atraso)
    
    # Act
    cur.execute("""
        INSERT INTO transacoes_pagamento (valor_original, tipo_operacao, valor_final, parametro)
        VALUES (?, ?, ?, ?)
    """, (valor_original, "juros_atraso", valor_com_juros, f"{dias_atraso} dias"))
    db_transacao.commit()
    
    # Assert
    cur.execute("SELECT valor_final FROM transacoes_pagamento WHERE tipo_operacao = 'juros_atraso'")
    resultado = cur.fetchone()[0]
    assert resultado == 105.0


def test_integracao_multiplas_transacoes(db_transacao):
    """Testa múltiplas transações no mesmo banco."""
    # Arrange
    cur = db_transacao.cursor()
    
    # Act
    operacoes = [
        (100, "desconto", calcular_desconto(100, 10), "10%"),
        (100, "juros", aplicar_juros_atraso(100, 5), "5 dias"),
        (200, "reembolso", processar_reembolso(200, 50), "reembolso_50"),
    ]
    
    for val_orig, tipo, val_final, param in operacoes:
        cur.execute("""
            INSERT INTO transacoes_pagamento (valor_original, tipo_operacao, valor_final, parametro)
            VALUES (?, ?, ?, ?)
        """, (val_orig, tipo, val_final, param))
    
    db_transacao.commit()
    
    # Assert
    cur.execute("SELECT COUNT(*) FROM transacoes_pagamento")
    assert cur.fetchone()[0] == 3
    
    # Verifica que os valores foram corretos
    cur.execute("SELECT SUM(valor_final) FROM transacoes_pagamento")
    soma = cur.fetchone()[0]
    assert soma == (90 + 105.0 + 150)