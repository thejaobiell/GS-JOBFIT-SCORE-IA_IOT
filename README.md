<div align="center">
  <img src="https://raw.githubusercontent.com/thejaobiell/GS-JOBFIT-SCORE-Java/refs/heads/main/src/main/resources/static/logo.jpeg" alt="MottuFlow" width="200"/>
  <h1>JobFit-Score - Sistema de Avaliação de Candidatos com IA</h1>
</div>

## Descrição

Sistema que avalia compatibilidade entre candidatos e vagas usando IA local via Ollama ou fallback determinístico.

---

## Requisitos

### Obrigatórios

* [Python 3.10+](https://www.python.org/downloads/)
* [Terminal Bash( ex: Git Bash )](https://git-scm.com/install/)
* [Ollama](https://ollama.com/)
* Modelo Ollama ( ex: [llama3.2:3b(modelo leve)](https://ollama.com/library/llama3.2) ou [gemma3:27b(modelo pesado)](https://ollama.com/library/gemma3:27b) )
> O sistema funciona sem IA usando fallback interno.

---

## Como utilizar

```bash
# Clone do Repositório
git clone https://github.com/thejaobiell/GS-JOBFIT-SCORE-IA_IOT.git

# Entre na pasta da aplicação
cd "GS-JOBFIT-SCORE-IA_IOT"

# Garanta a permissão para executar os scripts
chmod +x run_api.sh
chmod +x stop_api.sh

# Rode a aplicação
./run_api.sh
```

### API estará disponível em:

```
http://localhost:8000
```

### Documentação Swagger:

```
http://localhost:8000/docs
```

---

## Como Usar

### Modo sem IA

```bash
./run_api.sh
```

Usa fallback determinístico.

### Modo com IA (Ollama)

Instale o Ollama, baixe modelo e execute:

```bash
ollama pull llama3.2:3b
ollama serve
./run_api.sh
```

---

# Endpoints da API

Base URL:

```
http://127.0.0.1:8000
```

---

## GET /

Informações básicas da API.

Resposta:

```json
{
  "name": "GS-JobFitScore API",
  "version": "1.0.0",
  "status": "online",
  "docs": "/docs",
  "health": "/health",
  "endpoints": {
    "evaluate": "POST /evaluate - Avalia candidatos vs vaga",
    "extract_resume": "POST /extract-resume - Extrai currículo PDF",
    "extract_self": "POST /extract-self - Extrai candidato de texto",
    "extract_job": "POST /extract-job - Extrai vaga de texto",
    "evaluate_self": "POST /evaluate-self - Avalia auto-descrição vs vaga",
    "evaluate_texts": "POST /evaluate-texts - Avalia textos livres"
  }
}
```

---

## GET /health

Status e configurações atuais.

```bash
curl http://127.0.0.1:8000/health
```

Resposta 
```json
{
  "status": "ok",
  "version": "1.0.0",
  "use_model_default": true,
  "ollama_model": "llama3.2:3b",
  "ollama_url": "http://127.0.0.1:11434/api/generate",
  "cors_enabled": true
}
```

---

## POST /evaluate

Avalia um ou mais candidatos contra uma vaga estruturada.

Entrada:

```json
{
  "vaga": {
    "titulo": "Dev Mobile",
    "empresa": "TechX",
    "requisitos": ["react native", "typescript" ,"api", "git"]
  },
  "candidatos": [
    {
      "nome": "João",
      "habilidades": ["react native", "git"],
      "experiencia": "2 anos",
      "cursos": ["mobile"]
    }
  ]
}
```

---

## POST /extract-resume

Extrai informações estruturadas de um currículo PDF.

multipart/form-data:

```
file: candidato.pdf
```

Retorno:

```json
{
  "nome": "Fulano",
  "habilidades": [],
  "experiencia": "",
  "cursos": []
}
```

---

## POST /extract-self

Extrai um candidato a partir de texto livre.

Entrada:

```json
{
  "text": "Meu nome é João, tenho experiência com React Native e APIs."
}
```

Retorno:

```json
{
  "nome": "João",
  "habilidades": ["react native", "apis"],
  "experiencia": "...",
  "cursos": []
}
```

---

## POST /extract-job

Extrai vaga estruturada a partir de texto livre.

Entrada:

```json
{
  "text": "Empresa X procura Dev Backend com experiência em Java, Spring e Docker."
}
```

Retorno:

```json
{
  "titulo": "Dev Backend",
  "empresa": "Empresa X",
  "requisitos": ["java", "spring", "docker"],
  "descricao": "..."
}
```

---

## POST /evaluate-self

Extrai informações do candidato a partir de texto e avalia contra vaga.

Entrada:

```json
{
  "vaga": {
    "titulo": "Dev Java",
    "requisitos": ["java", "spring", "docker"]
  },
  "self_text": "Sou desenvolvedor Java com experiência em Spring."
}
```

---

## POST /evaluate-texts

Extrai vaga e candidato automaticamente e gera a avaliação final.

Entrada:

```json
{
  "job_text": "Buscamos Dev Android com Kotlin e APIs",
  "self_text": "Trabalho com Kotlin há 2 anos"
}
```

Saída:

```json
{
  "avaliacoes": [
    {
      "nome": "Candidato",
      "score": 85,
      "feedback": "Habilidades presentes: kotlin."
    }
  ]
}
```

---

## Estrutura

```
.
├── api
│   ├── __init__.py
│   ├── models.py
│   ├── server.py
│   └── services
│       ├── __init__.py
│       ├── ollama_client.py
│       └── pdf_reader.py
│
├── API_INTEGRATION.md
├── JAVA_INTEGRATION_EXAMPLES.md
├── job_fit_score_ollama.ipynb
├── job_fit_score_ollama.py
├── README.md
├── requirements.txt
├── resultado_avaliacao_ollama.json
├── run_api.sh
└── stop_api.sh
```
