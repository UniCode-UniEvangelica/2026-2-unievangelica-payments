import pytest
from app.main import calcular_multa, calcular_total_com_multa

def test_calcular_multa_taxa_incorreta():
    # Teste para o Defeito 2: Multa calculada com taxa incorreta
    # Esperado: 100 * 10 * (1/100) = 10
    # Atual com defeito: 100 * 10 * (1/1000) = 1
    assert calcular_multa(100, 10, 1) == 10.0

def test_calcular_multa_percentual_negativo():
    # Teste para o Defeito 1: Percentual negativo não validado
    # Esperado: Erro ou validação
    # Atual com defeito: Retorna um valor negativo sem tratamento
    assert calcular_multa(100, 10, -1) == "Erro: Taxa de multa não pode ser negativa"

def test_calcular_total_com_multa_nao_arredondado():
    # Teste para o Defeito 3: Total não arredondado
    # Esperado: 100 + 1.23 = 101.23 (arredondado para 2 casas, se fosse o caso)
    # Atual com defeito: 101.2345
    multa_calculada = 1.2345
    assert calcular_total_com_multa(100, multa_calculada) == 101.23
