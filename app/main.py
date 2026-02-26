def calcular_multa(valor_original, dias_atraso, taxa_multa_diaria):
    # Defeito 1 corrigido: Percentual negativo validado
    if taxa_multa_diaria < 0:
        raise ValueError("Taxa de multa não pode ser negativa")

    # Defeito 2 corrigido: Multa calculada com taxa correta (1% ao dia)
    multa = valor_original * dias_atraso * (taxa_multa_diaria / 100) # Correção: / 100
    return multa

def calcular_total_com_multa(valor_original, multa):
    total = valor_original + multa
    # Defeito 3 corrigido: Total arredondado para duas casas decimais
    return round(total, 2)
