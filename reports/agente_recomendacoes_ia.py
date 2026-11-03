import os
import json
from google import genai

class APSRiskAdvisorAgentGoogle:
    def __init__(self, google_client):
        self.client = google_client

    def generate_action_plan(self, summary_metrics: dict) -> str:
        system_prompt = (
            "Você é um Agente de IA sênior em saúde populacional e eficiência operacional. "
            "Sua função é analisar os indicadores de risco de abandono em serviços de saúde "
            "e gerar recomendações práticas, objetivas e acionáveis para gestores e profissionais de saúde."
        )

        user_content = (
            f"Com base nos seguintes indicadores consolidados do projeto APS: "
            f"{json.dumps(summary_metrics, ensure_ascii=False)}, "
            f"elabore um plano de ação estruturado com 3 prioridades estratégicas."
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{system_prompt}\n\nSolicitação: {user_content}"
            )
            return response.text

        except Exception as e:
            return f"Erro ao comunicar com a API do Google: {str(e)}"


if __name__ == "__main__":
    # Obtém a chave de API via variável de ambiente ou configuração local
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        try:
            from google.colab import userdata
            api_key = userdata.get("GEMINI_API_KEY")
        except ImportError:
            pass

    if not api_key:
        raise ValueError("A chave GEMINI_API_KEY precisa estar definida no ambiente.")

    client = genai.Client(api_key=api_key)

    mock_metrics = {
        "unidade_foco": "Unidade Piloto APS",
        "taxa_abandono_recente_pct": 18.5,
        "principal_fator_correlacionado": "Tempo de espera superior a 30 dias para retorno",
        "perfil_mais_atingido": "Adultos jovens (20-35 anos)"
    }

    print("--- Executando Agente de IA sobre os Dados do Projeto APS ---")
    advisor = APSRiskAdvisorAgentGoogle(client)
    action_plan = advisor.generate_action_plan(mock_metrics)

    print("\nPlano de Ação Gerado pela IA:")
    print(action_plan)

    output_filename = "relatorio_recomendacoes_ia.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("# Relatório de Recomendações Estratégicas (Gerado por Agente de IA)\n\n")
        f.write("Este documento apresenta os insights gerados automaticamente pelo agente de IA integrado ao pipeline de mitigação de falsos abandonos na APS.\n\n")
        f.write("---\n\n")
        f.write(action_plan)

    print(f"\n[Sucesso] Arquivo '{output_filename}' gerado com sucesso!")
