import sqlite3
import pytest
from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho
)


# ===========================================================================
# FIXTURE — banco em memória, isolado por teste
# ===========================================================================

@pytest.fixture
def db():
    # Arrange: cria banco zerado na RAM
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn          # entrega conexão para o teste
    conn.close()        # destrói o banco ao fim do teste


# ===========================================================================
# MISSÃO 1 — Inserção e persistência
# ===========================================================================

def test_item_persiste_no_banco(db):
    # Arrange
    nome      = "Notebook Gamer"
    preco     = 4799.99
    quantidade = 1

    # Act
    adicionar_item(db, nome, preco, quantidade)
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"]       == nome
    assert itens[0]["preco"]      == preco
    assert itens[0]["quantidade"] == quantidade


def test_multiplos_itens_persistem(db):
    # Arrange
    adicionar_item(db, "Mouse Gamer",      249.90, 1)
    adicionar_item(db, "Teclado Mecânico", 479.00, 2)
    adicionar_item(db, "Monitor 27'",     1899.00, 1)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    # Arrange
    nome       = "Produto Inválido"
    preco_ruim = -10.00
    quantidade = 1

    # Act + Assert
    with pytest.raises(ValueError):
        adicionar_item(db, nome, preco_ruim, quantidade)


# ===========================================================================
# MISSÃO 2 — Cálculo de total
# ===========================================================================

def test_carrinho_vazio_retorna_zero(db):
    # Arrange: banco vazio, nenhum insert

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 0.0


def test_total_considera_quantidade(db):
    # Arrange
    preco      = 50.00
    quantidade = 3

    # Act
    adicionar_item(db, "Fone de Ouvido", preco, quantidade)
    total = calcular_total(db)

    # Assert
    assert total == 150.0   # 50.00 × 3 = 150.0


def test_total_multiplos_itens(db):
    # Arrange
    adicionar_item(db, "Webcam HD",    299.00, 2)   # 598.00
    adicionar_item(db, "Hub USB",       89.90, 3)   # 269.70
    adicionar_item(db, "Suporte Notebook", 149.00, 1) # 149.00

    # Act
    total = calcular_total(db)

    # Assert
    assert round(total, 2) == 1016.70   # 598.00 + 269.70 + 149.00


# ===========================================================================
# MISSÃO 3 — Limpeza do carrinho
# ===========================================================================

def test_limpar_remove_todos_os_itens(db):
    # Arrange
    adicionar_item(db, "SSD 1TB",   379.00, 1)
    adicionar_item(db, "Memória RAM", 219.00, 2)

    # Act
    limpar_carrinho(db)

    # Assert
    assert listar_itens(db)  == []
    assert calcular_total(db) == 0.0


def test_pode_adicionar_apos_limpar(db):
    # Arrange: adiciona, limpa, adiciona de novo
    adicionar_item(db, "Item Antigo", 100.00, 1)
    limpar_carrinho(db)
    adicionar_item(db, "Item Novo",   250.00, 1)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Item Novo"