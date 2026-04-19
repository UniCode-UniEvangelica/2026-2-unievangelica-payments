#!/usr/bin/env python3
"""
Testes de INTEGRAÇÃO — Módulo Carrinho (SQLite :memory:)
Aula 11 — Teste de Software (2026.1) | UniCode UniEvangelica

=======================================================================
⚠️  POR QUE ESTE ARQUIVO É DIFERENTE DE test_pagamentos.py?
=======================================================================

  test_pagamentos.py       →  TESTE UNITÁRIO
  ─────────────────────       ─────────────────────────────────────────
  • Testa funções puras       • Sem banco de dados real
  • Usa Stubs/Mocks            • Sem rede, sem arquivo externo
  • Rápido: < 1ms por teste   • Isola a LÓGICA de negócio

  test_carrinho_integracao.py →  TESTE DE INTEGRAÇÃO
  ────────────────────────────   ──────────────────────────────────────
  • Testa módulo + banco real  • SQLite real (em memória)
  • Sem Mocks — toca o banco!  • Verifica PERSISTÊNCIA dos dados
  • Um pouco mais lento        • Isola via fixture (banco novo p/ cada teste)

=======================================================================
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
    """
    Fixture que entrega uma conexão SQLite ':memory:' com a tabela
    'carrinho' já criada.

    O banco EM MEMÓRIA é:
      ✅ Criado do zero antes de cada teste (setup)
      ✅ Destruído automaticamente ao fim de cada teste (teardown)
      ✅ Completamente isolado — um teste não suja o outro
    """
    conn = sqlite3.connect(":memory:")   # banco vive apenas na RAM
    criar_tabela(conn)                   # cria a estrutura da tabela
    yield conn                           # entrega para o teste
    conn.close()                         # teardown: banco destruído aqui


# =====================================================================
# GRUPO 1 — Testes de Inserção e Persistência
# =====================================================================

def test_item_persiste_no_banco(db):
    # Arrange
    adicionar_item(db, "Produto A", 100.0, 2)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Produto A"
    assert itens[0]["preco"] == 100.0
    assert itens[0]["quantidade"] == 2


def test_multiplos_itens_persistem(db):
    # Arrange
    adicionar_item(db, "A", 10, 1)
    adicionar_item(db, "B", 20, 2)
    adicionar_item(db, "C", 30, 3)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    # Assert
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto inválido", -10, 1)


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
    adicionar_item(db, "A", 10.0, 2)   # 20
    adicionar_item(db, "B", 5.0, 4)    # 20
    adicionar_item(db, "C", 2.5, 2)    # 5

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 45.0


# =====================================================================
# GRUPO 3 — Testes de Limpeza do Carrinho
# =====================================================================

def test_limpar_remove_todos_os_itens(db):
    # Arrange
    adicionar_item(db, "A", 10, 1)
    adicionar_item(db, "B", 20, 1)

    # Act
    limpar_carrinho(db)

    # Assert
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0


def test_pode_adicionar_apos_limpar(db):
    # Arrange
    adicionar_item(db, "A", 10, 1)
    limpar_carrinho(db)

    # Act
    adicionar_item(db, "B", 20, 2)
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "B"