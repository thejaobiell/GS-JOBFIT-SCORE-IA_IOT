<div align="center">
  <img src="https://raw.githubusercontent.com/thejaobiell/GS-JOBFIT-SCORE-Java/refs/heads/main/src/main/resources/static/logo.jpeg" alt="MottuFlow" width="200"/>
  <h1>JobFit-Score</h1>
</div>

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)

> 📦 **Repositório IA/IOT**: [github.com/thejaobiell/GS-JOBFIT-SCORE-IA_IOT](https://github.com/thejaobiell/GS-JOBFIT-SCORE-IA_IOT)

---

## 🎥 Vídeo Demonstrativo

Assista ao vídeo completo demonstrando o funcionamento do sistema:

[![Vídeo Demonstrativo](https://img.youtube.com/vi/WjyWRQT2fok/sddefault.jpg)](https://www.youtube.com/watch?v=WjyWRQT2fok)

🔗 **Link direto**: https://www.youtube.com/watch?v=WjyWRQT2fok

---

## 🎯 Sobre o Projeto

O **JobFit-Score** é um sistema que avalia automaticamente a compatibilidade entre candidatos e vagas de emprego. Utiliza IA local via Ollama para análise inteligente, com fallback determinístico para funcionar mesmo sem modelos de linguagem.

### Principais funcionalidades

- ✅ Avaliação automática de candidatos vs vagas
- 📄 Extração de dados de currículos em PDF
- 🤖 Análise com IA local (Ollama) ou fallback determinístico
- 🔄 API REST completa com documentação Swagger
- 🎨 Scripts automatizados para deploy simplificado

---

## 🌟 Características

- **IA Local**: Usa modelos Ollama sem enviar dados para serviços externos
- **Fallback Inteligente**: Funciona mesmo sem IA disponível
- **API RESTful**: Interface padronizada e documentada
- **Extração de PDF**: Processa currículos automaticamente
- **Análise de Texto Livre**: Avalia descrições não estruturadas
- **Configurável**: Múltiplas opções de configuração via CLI

---

## 📦 Requisitos

### Obrigatórios

| Requisito                               | Versão Mínima | Link                                          |
| --------------------------------------- | ------------- | --------------------------------------------- |
| Python                                  | 3.10+         | [Download](https://www.python.org/downloads/) |
| Terminal que consiga rodar arquivos .sh | Qualquer      | [Git Bash](https://git-scm.com/install/)      |

### Para IA

| Requisito  | Descrição                | Link                                  |
| ---------- | ------------------------ | ------------------------------------- |
| Ollama     | Runtime para modelos LLM | [ollama.com](https://ollama.com/)     |
| Modelo LLM | Ex: llama3.2:3b          | [Modelos](https://ollama.com/library) |

> **Nota**: O sistema funciona sem IA usando análise determinística baseada em regras.

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/thejaobiell/GS-JOBFIT-SCORE-IA_IOT.git
cd GS-JOBFIT-SCORE-IA_IOT
```

### 2. Configure permissões

```bash
chmod +x run_api.sh stop_api.sh
```

### 3. Execute a aplicação

```bash
./run_api.sh
```

A API estará disponível em:

- **Servidor**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 💻 Uso

### Modo Básico (sem IA)

```bash
./run_api.sh
```

O sistema usará o fallback determinístico automaticamente.

### Modo Avançado (com Ollama)

#### Passo 1: Instale e inicie o Ollama

```bash
# Baixe um modelo (exemplo: llama3.2:3b)
ollama pull llama3.2:3b

# Inicie o servidor Ollama
ollama serve
```

#### Passo 2: Execute com IA habilitada

```bash
./run_api.sh --model llama3.2:3b
```

### Opções de Configuração

O script `run_api.sh` aceita os seguintes parâmetros:

| Parâmetro      | Descrição                       | Exemplo                                            |
| -------------- | ------------------------------- | -------------------------------------------------- |
| `--host`       | Define o host do servidor       | `--host 0.0.0.0`                                   |
| `--port`       | Define a porta do servidor      | `--port 9000`                                      |
| `--model`      | Modelo Ollama a usar            | `--model llama3.2:1b`                              |
| `--ollama-url` | URL da API do Ollama            | `--ollama-url http://localhost:11434/api/generate` |
| `--cors`       | Origens CORS permitidas         | `--cors "*"`                                       |
| `--no-install` | Pula instalação de dependências | `--no-install`                                     |
| `--help`       | Exibe ajuda                     | `--help`                                           |

### Exemplos de Uso

```bash
# Servidor público na porta 9001 com modelo específico
./run_api.sh --host 0.0.0.0 --port 9001 --model llama3.2:3b

# Apenas mudar o modelo
./run_api.sh --model gemma2:27b

# Configuração completa
./run_api.sh --host 0.0.0.0 --port 9000 --model llama3.2:3b --cors "*" --no-install
```

### Parando o Servidor

```bash
./stop_api.sh
```

---

# Integração com as outras matérias

### Leia o arquivo [`INTEGRACAO.md`](https://github.com/thejaobiell/GS-JOBFIT-SCORE-IA_IOT/blob/main/INTEGRACAO.md)
#### - Contem a explicação detalhada da integração da API IA/IOT com o APP Mobile

---

## 📚 Documentação da API

### Base URL

```
http://127.0.0.1:8000
```

### Endpoints Principais

#### 1. **GET /** - Informações da API

Retorna informações gerais sobre a API.

**Resposta:**

```json
{
  "name": "GS-JobFitScore API",
  "version": "1.0.0",
  "status": "online",
  "docs": "/docs",
  "health": "/health"
}
```

---

#### 2. **GET /health** - Health Check

Verifica o status do sistema.

**Exemplo:**

```bash
curl http://127.0.0.1:8000/health
```

**Resposta:**

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

#### 3. **POST /evaluate** - Avaliar Candidatos

Avalia a compatibilidade entre candidatos e uma vaga.

**Request Body:**

```json
{
  "vaga": {
    "titulo": "Desenvolvedor Mobile",
    "empresa": "TechX",
    "requisitos": ["react native", "typescript", "api rest", "git"]
  },
  "candidatos": [
    {
      "nome": "João Silva",
      "habilidades": ["react native", "javascript", "git"],
      "experiencia": "2 anos em desenvolvimento mobile",
      "cursos": ["Bootcamp React Native", "Curso TypeScript"]
    }
  ]
}
```

**Resposta:**

```json
{
  "vaga": "Desenvolvedor Mobile",
  "candidatos_avaliados": [
    {
      "nome": "João Silva",
      "score": 85,
      "justificativa": "Forte compatibilidade com React Native e Git...",
      "recomendacao": "Recomendado"
    }
  ]
}
```

---

#### 4. **POST /extract-resume** - Extrair Currículo PDF

Extrai informações estruturadas de um currículo em PDF.

**Request:** multipart/form-data

```
file: curriculo.pdf
```

**Resposta:**

```json
{
  "nome": "Maria Santos",
  "habilidades": ["python", "django", "postgresql"],
  "experiencia": "5 anos como desenvolvedora backend",
  "cursos": ["Engenharia de Software", "Certificação AWS"]
}
```

---

#### 5. **POST /extract-self** - Extrair Auto-Descrição

Extrai informações estruturadas de texto livre sobre o candidato.

**Request Body:**

```json
{
  "text": "Meu nome é João, tenho 3 anos de experiência com React Native, TypeScript e integração de APIs. Completei bootcamp de desenvolvimento mobile."
}
```

**Resposta:**

```json
{
  "nome": "João",
  "habilidades": ["react native", "typescript", "apis"],
  "experiencia": "3 anos",
  "cursos": ["bootcamp mobile"]
}
```

---

#### 6. **POST /extract-job** - Extrair Vaga

Extrai informações estruturadas de uma descrição de vaga.

**Request Body:**

```json
{
  "text": "A empresa X busca Desenvolvedor Backend com experiência em Java, Spring Boot, Docker e microserviços."
}
```

**Resposta:**

```json
{
  "titulo": "Desenvolvedor Backend",
  "empresa": "empresa X",
  "requisitos": ["java", "spring boot", "docker", "microserviços"]
}
```

---

#### 7. **POST /evaluate-self** - Avaliar Auto-Descrição

Avalia um candidato através de sua auto-descrição em texto livre.

**Request Body:**

```json
{
  "vaga": {
    "titulo": "Desenvolvedor Java",
    "empresa": "TechCorp",
    "requisitos": ["java", "spring", "docker", "kubernetes"]
  },
  "self_text": "Sou desenvolvedor Java com 4 anos de experiência. Trabalho com Spring Framework e Docker no dia a dia."
}
```

---

#### 8. **POST /evaluate-texts** - Avaliar Textos Livres

Avalia compatibilidade entre descrição de vaga e auto-descrição do candidato.

**Request Body:**

```json
{
  "job_text": "Buscamos Desenvolvedor Android com experiência em Kotlin, Jetpack Compose e APIs REST.",
  "self_text": "Trabalho com Kotlin há 2 anos, desenvolvo apps Android nativos e integro APIs."
}
```

---

### Documentação Interativa

Acesse a documentação Swagger completa em:

```
http://localhost:8000/docs
```

Lá você pode testar todos os endpoints diretamente no navegador.

---

## 📁 Estrutura do Projeto

```
GS-JOBFIT-SCORE-IA_IOT/
├── api/
│   ├── __init__.py
│   ├── models.py              # Modelos Pydantic
│   ├── server.py              # Servidor FastAPI
│   └── services/
│       ├── __init__.py
│       ├── ollama_client.py   # Cliente Ollama
│       └── pdf_reader.py      # Leitor de PDF
│
│
├── examples/
│   ├── job_fit_score_ollama.ipynb
│   └── resultado_avaliacao_ollama.json
├── scripts/
│   ├── run_api.sh             # Script de inicialização
│   └── stop_api.sh            # Script de parada
├── job_fit_score_ollama.py    # Script principal
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente

O sistema utiliza as seguintes variáveis de ambiente (configuradas automaticamente pelo script):

```bash
OLLAMA_MODEL=llama3.2:3b
OLLAMA_URL=http://127.0.0.1:11434/api/generate
API_HOST=127.0.0.1
API_PORT=8000
CORS_ORIGINS=*
```

### Modelos Ollama Recomendados

| Modelo      | Tamanho | Uso Recomendado  |
| ----------- | ------- | ---------------- |
| llama3.2:1b | ~1GB    | Testes rápidos   |
| llama3.2:3b | ~3GB    | Uso geral        |
| gemma2:9b   | ~9GB    | Alta precisão    |
| gemma2:27b  | ~27GB   | Máxima qualidade |

---

## 👥 Equipe de Desenvolvimento

<table>
<tr>
<td align="center">
<a href="https://github.com/thejaobiell">
<img src="https://github.com/thejaobiell.png" width="100px;" alt="João Gabriel"/><br>
<sub><b>João Gabriel Boaventura</b></sub><br>
<sub>RM554874 • 2TDSB2025</sub><br>
</a>
</td>
<td align="center">
<a href="https://github.com/leomotalima">
<img src="https://github.com/leomotalima.png" width="100px;" alt="Léo Mota"/><br>
<sub><b>Léo Mota Lima</b></sub><br>
<sub>RM557851 • 2TDSB2025</sub><br>
</a>
</td>
<td align="center">
<a href="https://github.com/LucasLDC">
<img src="https://github.com/LucasLDC.png" width="100px;" alt="Lucas Leal"/><br>
<sub><b>Lucas Leal das Chagas</b></sub><br>
<sub>RM551124 • 2TDSB2025</sub><br>
</a>
</td>
</tr>
</table>
