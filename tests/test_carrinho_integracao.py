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
    """
    MISSÃO: Verificar que um item inserido realmente fica no banco.
    Arrange: Use adicionar_item(db, ...)
    Act: Use listar_itens(db)
    Assert: Verifique se o item está na lista e se os dados estão corretos.
    """
    # Arrange: insere um item
    adicionar_item(db, "Notebook", 3500.00, 1)
    
    # Act: recupera os itens
    itens = listar_itens(db)
    
    # Assert: o item está lá com nome, preco e quantidade corretos
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
    # Arrange: insere 3 itens distintos
    adicionar_item(db, "Notebook", 3500.00, 1)
    adicionar_item(db, "Mouse", 250.00, 2)
    adicionar_item(db, "Teclado", 450.00, 1)
    
    # Act: lista os itens
    itens = listar_itens(db)
    
    # Assert: exatamente 3 itens retornados
    assert len(itens) == 3

def test_preco_negativo_lanca_value_error(db):
    """
    Assert: ValueError deve ser lançado
    Dica: use pytest.raises(ValueError)
    """
    # Arrange + Act + Assert: tenta adicionar item com preço negativo
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto Inválido", -50.00, 1)


# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    """
    Arrange: banco vazio (nenhum insert)
    Act + Assert: calcular_total retorna 0.0
    """
    # Arrange: banco vazio (nenhum insert)
    # Act: calcula o total
    total = calcular_total(db)
    
    # Assert: retorna 0.0
    assert total == 0.0

def test_total_considera_quantidade(db):
    """
    Arrange: insere 3 unidades de R$ 50,00
    Assert: total == 150.0  (preco × quantidade)
    """
    # Arrange: insere 3 unidades de R$ 50,00
    adicionar_item(db, "Produto", 50.00, 3)
    
    # Act: calcula o total
    total = calcular_total(db)
    
    # Assert: total == 150.0 (preco × quantidade)
    assert total == 150.0

def test_total_multiplos_itens(db):
    """
    Arrange: 3 itens com preços e quantidades diferentes
    Assert: total == soma correta
    """
    # Arrange: 3 itens com preços e quantidades diferentes
    adicionar_item(db, "Notebook", 3500.00, 1)    # 3500.00 × 1 = 3500.00
    adicionar_item(db, "Mouse", 250.00, 2)         # 250.00 × 2 = 500.00
    adicionar_item(db, "Teclado", 450.00, 1)      # 450.00 × 1 = 450.00
    
    # Act: calcula o total
    total = calcular_total(db)
    
    # Assert: total == soma correta (3500 + 500 + 450 = 4450)
    assert total == 4450.0


# =====================================================================
# GRUPO 3 — Testes de Limpeza do Carrinho
# =====================================================================

def test_limpar_remove_todos_os_itens(db):
    """
    Arrange: adiciona 2 itens
    Act: limpa o carrinho
    Assert: listar_itens retorna [] e total retorna 0.0
    """
    # Arrange: adiciona 2 itens
    adicionar_item(db, "Notebook", 3500.00, 1)
    adicionar_item(db, "Mouse", 250.00, 2)
    
    # Act: limpa o carrinho
    limpar_carrinho(db)
    
    # Assert: listar_itens retorna [] e total retorna 0.0
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0

def test_pode_adicionar_apos_limpar(db):
    """
    Arrange: adiciona, limpa, adiciona de novo
    Assert: somente o último item existe
    """
    # Arrange: adiciona primeiro item
    adicionar_item(db, "Notebook", 3500.00, 1)
    
    # Act: limpa o carrinho
    limpar_carrinho(db)
    
    # Adiciona novo item após limpeza
    adicionar_item(db, "Mouse", 250.00, 2)
    
    # Assert: somente o último item existe
    itens = listar_itens(db)
    assert len(itens) == 1
    assert itens[0]["nome"] == "Mouse"
    assert itens[0]["quantidade"] == 2
