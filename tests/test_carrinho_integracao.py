import sqlite3
import pytest
from app.carrinho_db import (
    criar_tabela, 
    adicionar_item, 
    listar_itens, 
    calcular_total, 
    limpar_carrinho
)

@pytest.fixture
def db():
    """Fixture que cria um banco em memória para cada teste."""
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()

# --- Missão 1: Inserção e Persistência ---

def test_item_persiste_no_banco(db):
    # Arrange: insere um item
    adicionar_item(db, "Teclado Mecânico", 250.00, 1)
    
    # Act: recupera os itens
    itens = listar_itens(db)
    
    # Assert: o item está lá com os dados corretos
    assert len(itens) == 1
    assert itens[0]["nome"] == "Teclado Mecânico"
    assert itens[0]["preco"] == 250.00
    assert itens[0]["quantidade"] == 1

def test_multiplos_itens_persistem(db):
    # Arrange: insere 3 itens distintos
    adicionar_item(db, "Mouse", 120.00, 1)
    adicionar_item(db, "Monitor", 1200.00, 2)
    adicionar_item(db, "Pad", 50.00, 5)
    
    # Act: lista os itens
    itens = listar_itens(db)
    
    # Assert: exatamente 3 itens retornados
    assert len(itens) == 3

def test_preco_negativo_lanca_value_error(db):
    # Assert: ValueError deve ser lançado ao tentar inserir preço negativo
    with pytest.raises(ValueError):
        adicionar_item(db, "Item Inválido", -10.00, 1)

# --- Missão 2: Cálculo de Total ---

def test_carrinho_vazio_retorna_zero(db):
    # Arrange: banco vazio (nenhum insert realizado)
    
    # Act: calcula o total
    total = calcular_total(db)
    
    # Assert: deve retornar 0.0
    assert total == 0.0

def test_total_considera_quantidade(db):
    # Arrange: insere 3 unidades de R$ 50,00
    adicionar_item(db, "Camiseta", 50.00, 3)
    
    # Act: calcula total
    total = calcular_total(db)
    
    # Assert: total == 150.0 (50 * 3)
    assert total == 150.0

def test_total_multiplos_itens(db):
    # Arrange: 3 itens com preços e quantidades diferentes
    adicionar_item(db, "Item A", 10.00, 2) # 20.0
    adicionar_item(db, "Item B", 5.00, 1)  # 5.0
    adicionar_item(db, "Item C", 100.00, 1) # 100.0
    
    # Act: calcula total
    total = calcular_total(db)
    
    # Assert: total == soma correta (125.0)
    assert total == 125.0

# --- Missão 3: Limpeza do Carrinho ---

def test_limpar_remove_todos_os_itens(db):
    # Arrange: adiciona 2 itens
    adicionar_item(db, "Item 1", 10.0, 1)
    adicionar_item(db, "Item 2", 20.0, 1)
    
    # Act: limpa o carrinho
    limpar_carrinho(db)
    
    # Assert: listar_itens retorna vazio e total retorna 0.0
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0

def test_pode_adicionar_apos_limpar(db):
    # Arrange: adiciona, limpa, adiciona de novo
    adicionar_item(db, "Item Antigo", 50.0, 1)
    limpar_carrinho(db)
    adicionar_item(db, "Item Novo", 99.0, 1)
    
    # Act: recupera itens
    itens = listar_itens(db)
    
    # Assert: somente o último item existe
    assert len(itens) == 1
    assert itens[0]["nome"] == "Item Novo"