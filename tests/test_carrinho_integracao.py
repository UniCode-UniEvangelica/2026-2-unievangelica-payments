#!/usr/bin/env python3
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
    conn = sqlite3.connect(":memory:")   # banco vive apenas na RAM
    criar_tabela(conn)                   # cria a estrutura da tabela
    yield conn                           # entrega para o teste
    conn.close()                         # teardown: banco destruído aqui


# =====================================================================
# GRUPO 1 — Testes de Inserção e Persistência
# =====================================================================

def test_item_persiste_no_banco(db):
    """
    Verificar que um item inserido realmente fica no banco.
    Arrange: Use adicionar_item(db, ...)
    Act: Use listar_itens(db)
    Assert: Verifique se o item está na lista e se os dados estão corretos.
    """

    # Arrange
    adicionar_item(db, 'Produto teste 01', 10.0)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]['nome'] == 'Produto teste 01'
    assert itens[0]['preco'] == 10.0

def test_multiplos_itens_persistem(db):
    """
    Arrange: insere 3 itens distintos
    Act: lista os itens
    Assert: exatamente 3 itens retornados
    """
    # Arrange
    products = [ 
        { 
            'id': 1,
            'nome': 'Produto 01', 
            'preco': 20.0, 
            'quantidade': 1 
        },
        { 
            'id': 2,
            'nome': 'Produto 02', 
            'preco': 100.0,
            'quantidade': 2
        }, 
        { 
            'id': 3,
            'nome': 'Produto 03', 
            'preco': 200.0, 
            'quantidade': 3 
        }
    ]

    adicionar_item(db, 'Produto 01', 20.0, 1)
    adicionar_item(db, 'Produto 02', 100.0, 2)
    adicionar_item(db, 'Produto 03', 200.0, 3)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens)
    assert itens == products

def test_preco_negativo_lanca_value_error(db):
    """
    Assert: ValueError deve ser lançado
    Dica: use pytest.raises(ValueError)
    """
    with pytest.raises(ValueError):
        adicionar_item(db, "Produto inválido", -10, 1)

# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    """
    Arrange: banco vazio (nenhum insert)
    Act + Assert: calcular_total retorna 0.0
    """
    # Arrange 

    # Act
    total = calcular_total(db)

    # Aseert
    assert total == 0.00

def test_total_considera_quantidade(db):
    """
    Arrange: insere 3 unidades de R$ 50,00
    Assert: total == 150.0  (preco × quantidade)
    """

    # Arrange
    adicionar_item(db, 'Produto teste total', 50.0, 3)

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
    adicionar_item(db, 'Produto teste 01', 50.0, 3)
    adicionar_item(db, 'Produto teste 02', 50.0, 2)
    adicionar_item(db, 'Produto teste 03', 50.0)

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 300.0


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
    adicionar_item(db, 'Produto teste 01', 50.0, 3)
    adicionar_item(db, 'Produto teste 02', 50.0, 2)

    # Act
    limpar_carrinho(db)

    # Assert
    assert len(listar_itens(db)) == 0

def test_pode_adicionar_apos_limpar(db):
    """
    Arrange: adiciona, limpa, adiciona de novo
    Assert: somente o último item existe
    """

    # Arrange
    adicionar_item(db, 'Produto teste 01', 50.0, 3)
    adicionar_item(db, 'Produto teste 02', 50.0, 2)

    limpar_carrinho(db)

    adicionar_item(db, 'Produto novo', 20.00)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]['nome'] == 'Produto novo'