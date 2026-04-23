import sqlite3
import pytest
from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho,
)

# =====================================================================
# FIXTURE — O Coração do Teste de Integração
# =====================================================================

@pytest.fixture
def db():
    """
    Cria um banco SQLite em memória que é destruído após cada teste.
    Garante que um teste nunca interfira no resultado do outro.
    """
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()

# =====================================================================
# MISSÃO 1 — Inserção e Persistência
# =====================================================================

def test_item_persiste_no_banco(db):
    # Arrange: insere um item
    adicionar_item(db, "Teclado Mecânico", 250.0, 1)
    
    # Act: recupera os itens
    itens = listar_itens(db)
    
    # Assert: o item está lá com dados corretos
    assert len(itens) == 1
    assert itens[0]["nome"] == "Teclado Mecânico"
    assert itens[0]["preco"] == 250.0
    assert itens[0]["quantidade"] == 1

def test_multiplos_itens_persistem(db):
    # Arrange: insere 3 itens distintos
    adicionar_item(db, "Mouse", 120.0, 1)
    adicionar_item(db, "Monitor", 1200.0, 2)
    adicionar_item(db, "Cabo HDMI", 45.0, 3)
    
    # Act: lista os itens
    itens = listar_itens(db)
    
    # Assert: exatamente 3 itens retornados
    assert len(itens) == 3

def test_preco_negativo_lanca_value_error(db):
    # Assert: ValueError deve ser lançado se o preço for inválido
    with pytest.raises(ValueError):
        adicionar_item(db, "Item Bugado", -10.0, 1)

# =====================================================================
# MISSÃO 2 — Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    # Arrange: banco vazio (nenhum insert)
    # Act + Assert: calcular_total retorna 0.0
    assert calcular_total(db) == 0.0

def test_total_considera_quantidade(db):
    # Arrange: insere 3 unidades de R$ 50,00
    adicionar_item(db, "Pendrive", 50.0, 3)
    
    # Act & Assert: total == 150.0 (50 * 3)
    assert calcular_total(db) == 150.0

def test_total_multiplos_itens(db):
    # Arrange: 3 itens com preços e quantidades diferentes
    adicionar_item(db, "Item A", 10.0, 2) # 20.0
    adicionar_item(db, "Item B", 5.0, 4)  # 20.0
    adicionar_item(db, "Item C", 100.0, 1)# 100.0
    
    # Act & Assert: total == 140.0
    assert calcular_total(db) == 140.0

# =====================================================================
# MISSÃO 3 — Limpeza do Carrinho
# =====================================================================

def test_limpar_remove_todos_os_itens(db):
    # Arrange: adiciona 2 itens
    adicionar_item(db, "Item 1", 10.0, 1)
    adicionar_item(db, "Item 2", 20.0, 1)
    
    # Act: limpa o carrinho
    limpar_carrinho(db)
    
    # Assert: listar_itens retorna [] e total retorna 0.0
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0

def test_pode_adicionar_apos_limpar(db):
    # Arrange: adiciona, limpa, adiciona de novo
    adicionar_item(db, "Item Antigo", 99.0, 1)
    limpar_carrinho(db)
    adicionar_item(db, "Item Novo", 50.0, 1)
    
    # Act
    itens = listar_itens(db)
    
    # Assert: somente o último item existe
    assert len(itens) == 1
    assert itens[0]["nome"] == "Item Novo"