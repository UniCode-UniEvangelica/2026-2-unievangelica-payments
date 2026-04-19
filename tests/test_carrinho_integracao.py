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
     # Arrange
    nome_esperado = "Notebook"
    preco_esperado = 3499.90
    quantidade_esperada = 2
 
    # Act
    adicionar_item(db, nome=nome_esperado, preco=preco_esperado, quantidade=quantidade_esperada)
    itens = listar_itens(db)
 
    # Assert
    assert len(itens) == 1
    item_salvo = itens[0]
    assert item_salvo.nome == nome_esperado
    assert item_salvo.preco == pytest.approx(preco_esperado)
    assert item_salvo.quantidade == quantidade_esperada

def test_multiplos_itens_persistem(db):
    """
    Arrange: insere 3 itens distintos
    Act: lista os itens
    Assert: exatamente 3 itens retornados
    """
    # Arrange
    produtos = [
        ("Mouse", 150.0, 1),
        ("Teclado", 300.0, 1),
        ("Monitor", 1200.0, 1),
    ]
 
    # Act
    for nome, preco, qtd in produtos:
        adicionar_item(db, nome=nome, preco=preco, quantidade=qtd)
    itens = listar_itens(db)
 
    # Assert
    assert len(itens) == 3
    nomes_salvos = {item.nome for item in itens}
    assert nomes_salvos == {"Mouse", "Teclado", "Monitor"}
    
def test_preco_negativo_lanca_value_error(db):
    """
    Assert: ValueError deve ser lançado
    Dica: use pytest.raises(ValueError)
    """
    # Arrange
    nome = "Produto Inválido"
    preco_invalido = -10.0
 
    # Act / Assert
    with pytest.raises(ValueError, match="Preço não pode ser negativo"):
        adicionar_item(db, nome=nome, preco=preco_invalido)
 
    # Assert — nenhum item deve ter sido persistido
    assert listar_itens(db) == []

# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    """
    Arrange: banco vazio (nenhum insert)
    Act + Assert: calcular_total retorna 0.0
    """
    # Arrange
    # (nenhuma inserção — carrinho parte vazio graças ao :memory:)
 
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
    preco_unitario = 50.0
    quantidade = 3
 
    # Act
    adicionar_item(db, nome="Caneta", preco=preco_unitario, quantidade=quantidade)
    total = calcular_total(db)
 
    # Assert
    assert total == pytest.approx(150.0)
    

def test_total_multiplos_itens(db):
    """
    Arrange: 3 itens com preços e quantidades diferentes
    Assert: total == soma correta
    """
     # Arrange
     # Camiseta: 2 × 79.90  = 159.80
    # Calça:    1 × 199.90 = 199.90
    # Meia:     5 × 19.90  =  99.50
    # Total esperado        = 459.20
    itens = [
        ("Camiseta", 79.90, 2),
        ("Calça", 199.90, 1),
        ("Meia", 19.90, 5),
    ]
    total_esperado = (79.90 * 2) + (199.90 * 1) + (19.90 * 5)
 
    # Act
    for nome, preco, qtd in itens:
        adicionar_item(db, nome=nome, preco=preco, quantidade=qtd)
    total = calcular_total(db)
 
    # Assert
    assert total == pytest.approx(total_esperado, rel=1e-2)
    


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
    adicionar_item(db, nome="Produto A", preco=100.0, quantidade=1)
    adicionar_item(db, nome="Produto B", preco=200.0, quantidade=3)
    assert len(listar_itens(db)) == 2  # pré-condição
 
    # Act
    limpar_carrinho(db)
 
    # Assert
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.
   

def test_pode_adicionar_apos_limpar(db):
    """
    Arrange: adiciona, limpa, adiciona de novo
    Assert: somente o último item existe
    """
    # Arrange
    adicionar_item(db, nome="Item Antigo", preco=500.0, quantidade=2)
    limpar_carrinho(db)
 
    # Act
    adicionar_item(db, nome="Item Novo", preco=75.0, quantidade=1)
    itens = listar_itens(db)
    total = calcular_total(db)
 
    # Assert
    assert len(itens) == 1
    assert itens[0].nome == "Item Novo"
    assert total == pytest.approx(75.0)
 

