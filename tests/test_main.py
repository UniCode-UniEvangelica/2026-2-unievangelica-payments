import pytest
from app.main import calcular_multa, calcular_total_com_multa

def test_calcular_multa_taxa_correta():
    # Teste para a correção do Defeito 2: Multa calculada com taxa correta
    # Esperado: 100 * 10 * (1/100) = 10
    assert calcular_multa(100, 10, 1) == 10.0

def test_calcular_multa_percentual_negativo_valido():
    # Teste para a correção do Defeito 1: Percentual negativo validado
    with pytest.raises(ValueError, match="Taxa de multa não pode ser negativa"):
        calcular_multa(100, 10, -1)

def test_calcular_total_com_multa_arredondado():
    # Teste para a correção do Defeito 3: Total arredondado
    multa_calculada = 1.2345
    assert calcular_total_com_multa(100, multa_calculada) == 101.23
