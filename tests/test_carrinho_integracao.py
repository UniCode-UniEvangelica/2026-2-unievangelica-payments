#!/usr/bin/env python3
"""
Testes de INTEGRAÇÃO — Módulo Carrinho (SQLite :memory:)
Aula 11 — Teste de Software (2026.1) | UniCode UniEvangelica
"""

import sqlite3
import pytest
import sys
import os

# Garante que o pacote 'app' é encontrado independente de onde o aluno rodar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho,
)


# =====================================================================
# FIXTURE — Banco de dados isolado por teste
# =====================================================================

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()


# =====================================================================
# GRUPO 1 — Testes de Inserção e Persistência
# =====================================================================

def test_item_persiste_no_banco(db):
    # Arrange
    adicionar_item(db, "Notebook", 2500.0, 1)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Notebook"
    assert itens[0]["preco"] == 2500.0
    assert itens[0]["quantidade"] == 1


def test_multiplos_itens_persistem(db):
    # Arrange
    adicionar_item(db, "Mouse", 50.0, 2)
    adicionar_item(db, "Teclado", 150.0, 1)
    adicionar_item(db, "Monitor", 800.0, 1)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    # Assert
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto inválido", -10.0, 1)


# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    # Act
    total = calcular_total(db)

    # Assert
    assert total == 0.0


def test_total_considera_quantidade(db):
    # Arrange
    adicionar_item(db, "Produto", 50.0, 3)

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 150.0


def test_total_multiplos_itens(db):
    # Arrange
    adicionar_item(db, "Produto A", 10.0, 2)   # 20
    adicionar_item(db, "Produto B", 30.0, 1)   # 30
    adicionar_item(db, "Produto C", 5.0, 4)    # 20

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 70.0


# =====================================================================
# GRUPO 3 — Testes de Limpeza do Carrinho
# =====================================================================

def test_limpar_remove_todos_os_itens(db):
    # Arrange
    adicionar_item(db, "Produto A", 10.0, 1)
    adicionar_item(db, "Produto B", 20.0, 1)

    # Act
    limpar_carrinho(db)

    # Assert
    itens = listar_itens(db)
    total = calcular_total(db)

    assert itens == []
    assert total == 0.0


def test_pode_adicionar_apos_limpar(db):
    # Arrange
    adicionar_item(db, "Produto A", 10.0, 1)
    limpar_carrinho(db)

    # Act
    adicionar_item(db, "Produto B", 20.0, 2)
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Produto B"