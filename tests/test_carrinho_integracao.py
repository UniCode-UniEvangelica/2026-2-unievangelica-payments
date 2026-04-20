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
    """
    conn = sqlite3.connect(":memory:")   # banco vive apenas na RAM
    criar_tabela(conn)                   # cria a estrutura da tabela
    yield conn                           # entrega para o teste
    conn.close()                         # teardown: banco destruído aqui

# =====================================================================
# GRUPO 1 — Testes de Inserção e Persistência
# =====================================================================

def test_item_persiste_no_banco(db):
    """
    MISSÃO: Verificar que um item inserido realmente fica no banco.
    """
    # Arrange
    adicionar_item(db, "Notebook", 3500.00, 1)
    
    # Act
    itens = listar_itens(db)
    
    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Notebook"
    assert itens[0]["preco"] == 3500.00
    assert itens[0]["quantidade"] == 1

def test_multiplos_itens_persistem(db):
    """
    Arrange: insere 3 itens distintos
    Act: lista os itens
    Assert: exatamente 3 itens retornados
    """
    # Arrange
    adicionar_item(db, "Mouse", 150.00, 2)
    adicionar_item(db, "Teclado", 250.00, 1)
    adicionar_item(db, "Monitor", 1200.00, 1)
    
    # Act
    itens = listar_itens(db)
    
    # Assert
    assert len(itens) == 3

def test_preco_negativo_lanca_value_error(db):
    """
    Assert: ValueError deve ser lançado
    Dica: use pytest.raises(ValueError)
    """
    # Act & Assert
    with pytest.raises(ValueError, match="Preço não pode ser negativo"):
        adicionar_item(db, "Item Inválido", -10.50, 1)

# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    """
    Arrange: banco vazio (nenhum insert)
    Act + Assert: calcular_total retorna 0.0
    """
    # Act
    total = calcular_total(db)
    
    # Assert
    assert total == 0.0

def test_total_considera_quantidade(db):
    """
    Arrange: insere 3 unidades de R$ 50,00
    Assert: total == 150.0  (preco × quantidade)
    """
    # Arrange
    adicionar_item(db, "Cabo USB", 50.00, 3)
    
    # Act
    total = calcular_total(db)
    
    # Assert
    assert total == 150.0

def test_total_multiplos_itens(db):
    """
    Arrange: 3 itens com preços e quantidades diferentes
    Assert: total == soma correta
    """
    # Arrange
    adicionar_item(db, "Item A", 10.00, 2)  # Subtotal: 20.00
    adicionar_item(db, "Item B", 50.00, 1)  # Subtotal: 50.00
    adicionar_item(db, "Item C", 5.00, 4)   # Subtotal: 20.00
    
    # Act
    total = calcular_total(db)
    
    # Assert
    assert total == 90.00

# =====================================================================
# GRUPO 3 — Testes de Limpeza do Carrinho
# =====================================================================

def test_limpar_remove_todos_os_itens(db):
    """
    Arrange: adiciona 2 itens
    Act: limpa o carrinho
    Assert: listar_itens retorna [] e total retorna 0.0
    """
    # Arrange
    adicionar_item(db, "Item 1", 100.00, 1)
    adicionar_item(db, "Item 2", 200.00, 1)
    
    # Act
    linhas_removidas = limpar_carrinho(db)
    
    # Assert
    assert linhas_removidas == 2
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0

def test_pode_adicionar_apos_limpar(db):
    """
    Arrange: adiciona, limpa, adiciona de novo
    Assert: somente o último item existe
    """
    # Arrange
    adicionar_item(db, "Item Antigo", 100.00, 1)
    limpar_carrinho(db)
    
    # Act
    adicionar_item(db, "Item Novo", 500.00, 1)
    itens = listar_itens(db)
    
    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Item Novo"
    assert calcular_total(db) == 500.00