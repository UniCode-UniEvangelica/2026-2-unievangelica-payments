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
    nome, preco, qtd = "Teclado", 150.0, 1
    
    # Act
    adicionar_item(db, nome, preco, qtd)
    itens = listar_itens(db)
    
    # Assert
    assert len(itens) == 1
    # Acesso via índice (tupla): [1] é o nome, [2] é o preço
    assert itens[0][1] == nome
    assert itens[0][2] == preco

def test_multiplos_itens_persistem(db):
    # Arrange
    itens_para_add = [("Item 1", 10.0, 1), ("Item 2", 20.0, 2), ("Item 3", 30.0, 3)]
    
    # Act
    for item in itens_para_add:
        adicionar_item(db, *item)
    itens_no_banco = listar_itens(db)
    
    # Assert
    assert len(itens_no_banco) == 3

def test_preco_negativo_lanca_value_error(db):
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        adicionar_item(db, "Item Inválido", -10.0, 1)


# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    # Arrange & Act
    total = calcular_total(db)
    
    # Assert
    assert total == 0.0

def test_total_considera_quantidade(db):
    # Arrange
    adicionar_item(db, "Mouse Gamer", 50.0, 3)
    
    # Act
    total = calcular_total(db)
    
    # Assert
    assert total == 150.0

def test_total_multiplos_itens(db):
    # Arrange
    adicionar_item(db, "A", 10.0, 2) # 20
    adicionar_item(db, "B", 5.0, 4)  # 20
    
    # Act
    total = calcular_total(db)
    
    # Assert
    assert total == 40.0


# =====================================================================
# GRUPO 3 — Testes de Limpeza do Carrinho
# =====================================================================

def test_limpar_remove_todos_os_itens(db):
    # Arrange
    adicionar_item(db, "Item", 10.0, 1)
    
    # Act
    limpar_carrinho(db)
    itens = listar_itens(db)
    total = calcular_total(db)
    
    # Assert
    assert len(itens) == 0
    assert total == 0.0

def test_pode_adicionar_apos_limpar(db):
    # Arrange
    adicionar_item(db, "Antigo", 10.0, 1)
    limpar_carrinho(db)
    
    # Act
    adicionar_item(db, "Novo", 20.0, 1)
    itens = listar_itens(db)
    
    # Assert
    assert len(itens) == 1
    # Acesso via índice (tupla)
    assert itens[0][1] == "Novo"
