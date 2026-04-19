import sqlite3
import pytest
from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho,
)

@pytest.fixture
def db():
    """Cria um banco de dados em memória para cada teste."""
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()

# --- Testes de Inserção ---

def test_item_persiste_no_banco(db):
    adicionar_item(db, "Teclado Mecânico", 250.0, 1)
    itens = listar_itens(db)
    assert len(itens) == 1
    assert itens[0]["nome"] == "Teclado Mecânico"

def test_multiplos_itens_persistem(db):
    adicionar_item(db, "Mouse", 120.0, 1)
    adicionar_item(db, "Monitor", 1200.0, 2)
    itens = listar_itens(db)
    assert len(itens) == 2

def test_preco_negativo_lanca_value_error(db):
    with pytest.raises(ValueError):
        adicionar_item(db, "Erro", -10.0, 1)

# --- Testes de Cálculo ---

def test_carrinho_vazio_retorna_zero(db):
    assert calcular_total(db) == 0.0

def test_total_considera_quantidade(db):
    adicionar_item(db, "Camiseta", 50.0, 3)
    assert calcular_total(db) == 150.0

def test_total_multiplos_itens(db):
    adicionar_item(db, "Item A", 10.0, 2)
    adicionar_item(db, "Item B", 5.0, 1)
    assert calcular_total(db) == 25.0

# --- Testes de Limpeza ---

def test_limpar_remove_todos_os_itens(db):
    adicionar_item(db, "Item 1", 10.0, 1)
    limpar_carrinho(db)
    assert len(listar_itens(db)) == 0

def test_pode_adicionar_apos_limpar(db):
    adicionar_item(db, "Velho", 50.0, 1)
    limpar_carrinho(db)
    adicionar_item(db, "Novo", 30.0, 1)
    assert listar_itens(db)[0]["nome"] == "Novo"
