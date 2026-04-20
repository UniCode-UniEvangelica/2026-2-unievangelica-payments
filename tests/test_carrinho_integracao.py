#!/usr/bin/env python3
"""
Testes de Integração — Carrinho de Compras com SQLite

Aula 11 Extra — Teste de Software (2026.1) | UniCode UniEvangelica
Aluno: Vinicius Fernandes de Jesus — 2312975
"""

import sqlite3
import pytest
from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho,
)


# =====================================================================
# Fixture — Banco de dados SQLite em memória (isolamento garantido)
# =====================================================================
@pytest.fixture
def db():
    """Cria um banco SQLite em memória com a tabela 'carrinho' pronta."""
    conn = sqlite3.connect(":memory:")  # banco vive só na RAM
    criar_tabela(conn)                  # cria a estrutura
    yield conn                          # entrega para o teste
    conn.close()                        # destrói o banco ao fim


# =====================================================================
# Missão 1 — Testar inserção e persistência (3 testes)
# =====================================================================
def test_item_persiste_no_banco(db):
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
    # Arrange: insere 3 itens distintos
    adicionar_item(db, "Mouse", 120.00, 2)
    adicionar_item(db, "Teclado", 250.00, 1)
    adicionar_item(db, "Monitor", 1800.00, 1)

    # Act: lista os itens
    itens = listar_itens(db)

    # Assert: exatamente 3 itens retornados
    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    # Assert: ValueError deve ser lançado ao inserir preço negativo
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto Inválido", -50.00, 1)


# =====================================================================
# Missão 2 — Testar cálculo de total (3 testes)
# =====================================================================
def test_carrinho_vazio_retorna_zero(db):
    # Arrange: banco vazio (nenhum insert)

    # Act + Assert: calcular_total retorna 0.0
    assert calcular_total(db) == 0.0


def test_total_considera_quantidade(db):
    # Arrange: insere 3 unidades de R$ 50,00
    adicionar_item(db, "Caderno", 50.00, 3)

    # Act
    total = calcular_total(db)

    # Assert: total == 150.0 (preco × quantidade)
    assert total == 150.0


def test_total_multiplos_itens(db):
    # Arrange: 3 itens com preços e quantidades diferentes
    adicionar_item(db, "Caneta", 5.00, 10)     # 50.00
    adicionar_item(db, "Caderno", 25.00, 2)    # 50.00
    adicionar_item(db, "Mochila", 150.00, 1)   # 150.00

    # Act
    total = calcular_total(db)

    # Assert: total == soma correta (50 + 50 + 150 = 250)
    assert total == 250.0


# =====================================================================
# Missão 3 — Testar limpeza do carrinho (2 testes)
# =====================================================================
def test_limpar_remove_todos_os_itens(db):
    # Arrange: adiciona 2 itens
    adicionar_item(db, "Mouse", 120.00, 1)
    adicionar_item(db, "Teclado", 250.00, 1)

    # Act: limpa o carrinho
    limpar_carrinho(db)

    # Assert: listar_itens retorna [] e total retorna 0.0
    assert listar_itens(db) == []
    assert calcular_total(db) == 0.0


def test_pode_adicionar_apos_limpar(db):
    # Arrange: adiciona, limpa, adiciona de novo
    adicionar_item(db, "Mouse", 120.00, 1)
    limpar_carrinho(db)
    adicionar_item(db, "Teclado", 250.00, 1)

    # Act
    itens = listar_itens(db)

    # Assert: somente o último item existe
    assert len(itens) == 1
    assert itens[0]["nome"] == "Teclado"
