#!/usr/bin/env python3

import sqlite3
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho,
)


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()


# =========================
# GRUPO 1
# =========================

def test_item_persiste_no_banco(db):
    adicionar_item(db, "Produto A", 100.0, 2)
    itens = listar_itens(db)

    assert len(itens) == 1
    assert itens[0]["nome"] == "Produto A"
    assert itens[0]["preco"] == 100.0
    assert itens[0]["quantidade"] == 2


def test_multiplos_itens_persistem(db):
    adicionar_item(db, "A", 10, 1)
    adicionar_item(db, "B", 20, 2)
    adicionar_item(db, "C", 30, 3)

    itens = listar_itens(db)

    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto inválido", -10, 1)


# =========================
# GRUPO 2
# =========================

def test_carrinho_vazio_retorna_zero(db):
    total = calcular_total(db)
    assert total == 0.0


def test_total_considera_quantidade(db):
    adicionar_item(db, "Produto", 50.0, 3)

    total = calcular_total(db)
    assert total == 150.0


def test_total_multiplos_itens(db):
    adicionar_item(db, "A", 10.0, 2)
    adicionar_item(db, "B", 5.0, 4)
    adicionar_item(db, "C", 2.5, 2)

    total = calcular_total(db)
    assert total == 45.0


# =========================
# GRUPO 3
# =========================

def test_limpar_remove_todos_os_itens(db):
    adicionar_item(db, "A", 10, 1)
    adicionar_item(db, "B", 20, 1)

    limpar_carrinho(db)

    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0


def test_pode_adicionar_apos_limpar(db):
    adicionar_item(db, "A", 10, 1)
    limpar_carrinho(db)

    adicionar_item(db, "B", 20, 2)
    itens = listar_itens(db)

    assert len(itens) == 1
    assert itens[0]["nome"] == "B"