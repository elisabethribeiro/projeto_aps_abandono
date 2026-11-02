import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

SEMENTE = 42
random.seed(SEMENTE)
np.random.seed(SEMENTE)

total_vidas = 1000
linhas_cuidado = ["HAS", "DM", "DLP", "Sobrepeso e Obesidade", "Gestantes", "Saúde Mental"]
status_opcoes = ["Em dia", "Pendente", "Abandono"]
pesos_status = [0.55, 0.25, 0.20]

hoje = pd.to_datetime("2026-11-01")
lista_vidas = []

for i in range(1, total_vidas + 1):
    id_paciente = f"PAC_{i:04d}"
    nome = f"Paciente {i}"
    idade = random.randint(18, 80)
    data_nascimento = (hoje - timedelta(days=idade * 365 + random.randint(0, 364))).strftime("%d/%m/%Y")
    telefone = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    linha_cuidado = random.choice(linhas_cuidado)
    status_lc = random.choices(status_opcoes, weights=pesos_status)[0]
    
    if status_lc == "Pendente":
        pendencias = random.choice(["Exames laboratoriais atrasados", "Consulta médica semestral pendente", "Avaliação nutricional pendente"])
    elif status_lc == "Abandono":
        pendencias = "Sem contato ha mais de 180 dias na linha"
    else:
        pendencias = "Nenhuma pendencia ativa"
        
    dias_mfc = random.randint(5, 200) if random.random() > 0.15 else None
    ultimo_mfc = (hoje - timedelta(days=dias_mfc)).strftime("%d/%m/%Y") if dias_mfc else "Sem registro"

    lista_vidas.append({
        "id_paciente": id_paciente,
        "nome_completo": nome,
        "data_nascimento": data_nascimento,
        "idade": idade,
        "telefone": telefone,
        "linha_de_cuidado_final": linha_cuidado,
        "status_LC": status_lc,
        "pendencias": pendencias,
        "ultimo_atendimento_mfc": ultimo_mfc,
        "dias_ultimo_atendimento_mfc": dias_mfc
    })

df = pd.DataFrame(lista_vidas)

# Identificacao de Falso Abandono (Regra 90 dias)
cond_falso_abandono = (df["status_LC"] == "Abandono") & (df["dias_ultimo_atendimento_mfc"] <= 90)
df_falso_abandono = df[cond_falso_abandono]

print(f"Total de pacientes analisados: {len(df)}")
print(f"Total de casos em falso abandono identificados: {len(df_falso_abandono)}")
