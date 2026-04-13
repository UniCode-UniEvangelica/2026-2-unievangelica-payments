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
    """
    Fixture que entrega uma conexao SQLite ':memory:' com a tabela
    'carrinho' ja criada.
 
    O banco EM MEMORIA e:
      OK Criado do zero antes de cada teste (setup)
      OK Destruido automaticamente ao fim de cada teste (teardown)
      OK Completamente isolado — um teste nao suja o outro
    """
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()
 

def test_item_persiste_no_banco(db):
    """Verifica que um item inserido realmente fica no banco."""
    # Arrange
    nome = "Notebook"
    preco = 3500.00
    quantidade = 1
 
    # Act
    adicionar_item(db, nome, preco, quantidade)
    itens = listar_itens(db)
 
    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Notebook"
    assert itens[0]["preco"] == 3500.00
    assert itens[0]["quantidade"] == 1
 
 
def test_multiplos_itens_persistem(db):
    """Insere 3 itens distintos e verifica que todos sao retornados."""
    # Arrange
    adicionar_item(db, "Teclado", 300.00, 1)
    adicionar_item(db, "Mouse", 150.00, 2)
    adicionar_item(db, "Monitor", 1200.00, 1)
 
    # Act
    itens = listar_itens(db)
 
    # Assert
    assert len(itens) == 3
    nomes = [i["nome"] for i in itens]
    assert "Teclado" in nomes
    assert "Mouse" in nomes
    assert "Monitor" in nomes
 
 
def test_preco_negativo_lanca_value_error(db):
    """Preco negativo deve lancar ValueError antes de tocar o banco."""
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto Invalido", -10.00, 1)
 
 
def test_quantidade_zero_lanca_value_error(db):
    """Boundary value: quantidade == 0 deve lancar ValueError."""
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto", 50.00, 0)
 
 
def test_quantidade_negativa_lanca_value_error(db):
    """Branch coverage: quantidade negativa tambem deve lancar ValueError."""
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto", 50.00, -5)
 
 
def test_adicionar_item_retorna_id(db):
    """adicionar_item deve retornar o id (rowid) gerado pelo banco."""
    # Arrange / Act
    id_gerado = adicionar_item(db, "SSD", 500.00, 1)
 
    # Assert
    assert isinstance(id_gerado, int)
    assert id_gerado >= 1
 

def test_carrinho_vazio_retorna_zero(db):
    """Banco vazio: calcular_total deve retornar 0.0."""
    # Arrange — nenhum item inserido (fixture entrega banco limpo)
 
    # Act
    total = calcular_total(db)
 
    # Assert
    assert total == 0.0
 
 
def test_total_considera_quantidade(db):
    """3 unidades de R$50,00 devem totalizar R$150,00."""
    # Arrange
    adicionar_item(db, "Caneta", 50.00, 3)
 
    # Act
    total = calcular_total(db)
 
    # Assert
    assert total == 150.0
 
 
def test_total_multiplos_itens(db):
    """
    3 itens com precos e quantidades variadas.
    Total = (10 x 2) + (25 x 1) + (100 x 3) = 20 + 25 + 300 = 345.0
    """
    # Arrange
    adicionar_item(db, "Borracha", 10.00, 2)
    adicionar_item(db, "Caderno", 25.00, 1)
    adicionar_item(db, "Livro", 100.00, 3)
 
    # Act
    total = calcular_total(db)
 
    # Assert
    assert total == pytest.approx(345.0)
 
 
def test_total_item_preco_zero(db):
    """Boundary value: preco == 0.0 deve ser aceito e nao afetar o total."""
    adicionar_item(db, "Brinde", 0.00, 5)
    assert calcular_total(db) == 0.0
 

def test_limpar_remove_todos_os_itens(db):
    """Apos limpar, o carrinho deve estar vazio e o total zerado."""
    # Arrange
    adicionar_item(db, "Item A", 100.00, 1)
    adicionar_item(db, "Item B", 200.00, 2)
 
    # Act
    linhas_removidas = limpar_carrinho(db)
    itens = listar_itens(db)
    total = calcular_total(db)
 
    # Assert
    assert linhas_removidas == 2
    assert itens == []
    assert total == 0.0
 
 
def test_pode_adicionar_apos_limpar(db):
    """
    Fluxo completo: adiciona -> limpa -> adiciona de novo.
    Somente o ultimo item deve existir no banco.
    """
    # Arrange
    adicionar_item(db, "Produto Antigo", 99.00, 1)
    limpar_carrinho(db)
 
    # Act
    adicionar_item(db, "Produto Novo", 49.90, 2)
    itens = listar_itens(db)
 
    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Produto Novo"
    assert itens[0]["preco"] == 49.90
    assert itens[0]["quantidade"] == 2
 
 
def test_limpar_carrinho_vazio_retorna_zero_linhas(db):
    """Boundary value: limpar banco ja vazio deve retornar 0 linhas removidas."""
    linhas = limpar_carrinho(db)
    assert linhas == 0
 