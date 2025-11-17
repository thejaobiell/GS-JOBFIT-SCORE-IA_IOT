import json
import sys
import io
import requests

# Corrige encoding no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Configuração do Ollama (local)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"  # ou "gemma3:27b" para modelo maior

dados = {
    "vaga": {
        "titulo": "Desenvolvedor Front-End React Native",
        "empresa": "TechFlow Solutions",
        "requisitos": [
            "React Native",
            "JavaScript",
            "TypeScript",
            "APIs REST",
            "Git",
            "UI/UX básico",
        ],
        "descricao": "Responsável por desenvolver e manter aplicativos móveis usando React Native, garantindo performance e boa experiência do usuário.",
    },
    "candidatos": [
        {
            "nome": "Ana Souza",
            "habilidades": ["React Native", "JavaScript", "Figma", "UX Design", "Git"],
            "experiencia": "2 anos como desenvolvedora mobile em React Native",
            "cursos": ["React Native Avançado", "Design de Interfaces"],
        },
        {
            "nome": "Lucas Pereira",
            "habilidades": ["JavaScript", "TypeScript", "Node.js", "ReactJS"],
            "experiencia": "3 anos como desenvolvedor full-stack, iniciando com React Native",
            "cursos": ["ReactJS Completo", "APIs REST com Node.js"],
        },
        {
            "nome": "Mariana Lima",
            "habilidades": [
                "HTML",
                "CSS",
                "React Native",
                "APIs REST",
                "Git",
                "TypeScript",
            ],
            "experiencia": "1 ano como estagiária em desenvolvimento mobile",
            "cursos": ["Introdução ao React Native", "Versionamento com Git"],
        },
    ],
}

prompt = f"""
Você é um avaliador técnico de compatibilidade entre candidatos e vagas de emprego.

Analise os dados abaixo em formato JSON. Compare as habilidades, experiências e cursos dos candidatos com os requisitos da vaga.

Para cada candidato, calcule um score de compatibilidade de 0 a 100 e retorne em formato JSON no seguinte modelo:

{{
  "avaliacoes": [
    {{
      "nome": "Nome do candidato",
      "score": número,
      "feedback": "breve explicação sobre a pontuação"
    }}
  ]
}}

Use os seguintes critérios:
- + pontos para cada habilidade que coincidir com os requisitos da vaga.
- Considere experiência e cursos relacionados como fator positivo.
- Diminua pontos se o candidato não tiver tecnologias essenciais da vaga.
- O score deve refletir a chance real de sucesso na vaga (0 a 100).

IMPORTANTE: Retorne APENAS o JSON, sem markdown ou explicações adicionais.

Dados:
{json.dumps(dados, ensure_ascii=False, indent=2)}
"""


def gerar_com_ollama(prompt, model=MODEL_NAME):
    """Faz requisição para o Ollama local"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # Força resposta em JSON
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        raise Exception(
            "❌ Não foi possível conectar ao Ollama. Certifique-se de que está rodando (ollama serve)"
        )
    except requests.exceptions.Timeout:
        raise Exception("⏱️ Timeout: O modelo demorou muito para responder")
    except Exception as e:
        raise Exception(f"Erro na requisição: {e}")


try:
    print("🔄 Gerando avaliação dos candidatos com Ollama...\n")
    print(f"📦 Modelo: {MODEL_NAME}")
    print("⏳ Aguarde, isso pode levar alguns segundos...\n")

    # Gera resposta com Ollama
    resposta_texto = gerar_com_ollama(prompt)

    # Parse do JSON
    try:
        resultado = json.loads(resposta_texto)

        # Exibe os resultados de forma formatada
        print("=" * 60)
        print(f"📋 VAGA: {dados['vaga']['titulo']}")
        print(f"🏢 EMPRESA: {dados['vaga']['empresa']}")
        print("=" * 60)
        print()

        for avaliacao in resultado["avaliacoes"]:
            print(f"👤 {avaliacao['nome']}")
            print(f"   Score: {avaliacao['score']}/100")
            print(f"   📝 {avaliacao['feedback']}")
            print("-" * 60)

        # Salva o resultado em arquivo JSON
        with open("resultado_avaliacao_ollama.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print("\n✅ Resultado salvo em 'resultado_avaliacao_ollama.json'")

    except json.JSONDecodeError as e:
        print("⚠️  Não foi possível interpretar como JSON. Resposta bruta:")
        print(resposta_texto)
        print(f"\nErro: {e}")

except Exception as e:
    print(f"❌ Erro: {e}")
    print("\n💡 Dicas:")
    print("   1. Verifique se o Ollama está rodando: ollama serve")
    print("   2. Verifique se o modelo está instalado: ollama list")
    print(f"   3. Se necessário, instale o modelo: ollama pull {MODEL_NAME}")
