def calcular_multa(valor_original, dias_atraso, taxa_multa_diaria):
    # Defeito 1: Percentual negativo não validado (a validação foi removida propositalmente)
    # if taxa_multa_diaria < 0:
    #     return "Erro: Taxa de multa não pode ser negativa"

    # Defeito 2: Multa calculada com taxa incorreta (0.1% ao dia, deveria ser 1%)
    multa = valor_original * dias_atraso * (taxa_multa_diaria / 1000) # Deveria ser / 100
    return multa

def calcular_total_com_multa(valor_original, multa):
    total = valor_original + multa
    # Defeito 3: Total não arredondado
    return total
