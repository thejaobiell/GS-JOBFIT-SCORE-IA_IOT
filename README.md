# 🎯 JobFitScore - Sistema de Avaliação de Candidatos com IA

Sistema inteligente que avalia a compatibilidade entre candidatos e vagas de emprego usando IA local (Ollama) ou fallback determinístico.

## 📋 Índice

- [Requisitos](#-requisitos)
- [Instalação Rápida](#-instalação-rápida)
- [Como Usar](#-como-usar)
- [Endpoints da API](#-endpoints-da-api)
- [Exemplos Práticos](#-exemplos-práticos)
- [Troubleshooting](#-troubleshooting)

---

## 🔧 Requisitos

### Obrigatórios

- **Python 3.10 ou superior** ([Download](https://www.python.org/downloads/))
- **Windows 10/11** (PowerShell)

### Opcionais (para usar IA)

- **Ollama** ([Download](https://ollama.com/download))
- **Modelo Ollama** (ex: `llama3.2:3b`)

> **Nota**: O sistema funciona SEM Ollama usando fallback determinístico!

---

## 🚀 Instalação Rápida

### Passo 1: Baixar o Projeto

```powershell
cd C:\Users\SEU_USUARIO\Documents
git clone [URL_DO_REPOSITORIO]
cd "GS-JobFitScore\Disruptive Architectures IOT & IA"
```

### Passo 2: Instalar Python

1. Baixe Python 3.10+ em https://www.python.org/downloads/
2. Durante instalação, **marque**: ✅ "Add Python to PATH"
3. Verifique instalação:
   ```powershell
   python --version
   # Deve mostrar: Python 3.10.x ou superior
   ```

### Passo 3: Configurar Permissão de Scripts (uma vez)

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

### Passo 4: Rodar a API

**Opção A - Duplo clique:**

1. Navegue até a pasta do projeto
2. Clique duas vezes em `run_api.ps1`
3. Aguarde a mensagem: `Uvicorn running on http://127.0.0.1:8000`

**Opção B - Terminal:**

```powershell
.\run_api.ps1
```

### Passo 5: Testar

Abra o navegador em: http://127.0.0.1:8000/docs

✅ Se aparecer a documentação interativa (Swagger), está funcionando!

---

## 📖 Como Usar

### Modo 1: Sem IA (Funciona Sempre)

O sistema funciona imediatamente sem instalar nada além do Python:

```powershell
.\run_api.ps1
```

- ✅ Extrai candidatos de PDFs (sem estruturação inteligente)
- ✅ Avalia candidatos usando lógica determinística
- ✅ Score de 0-100 baseado em match de palavras-chave

### Modo 2: Com IA (Ollama)

Para ter análise inteligente com IA local:

#### 1. Instalar Ollama

- Windows: https://ollama.com/download
- Baixe e instale (Next → Next → Finish)

#### 2. Baixar um Modelo

Abra um **novo terminal** e execute:

```powershell
# Modelo pequeno e rápido (2GB)
ollama pull llama3.2:3b

# OU modelo maior e mais preciso (16GB)
ollama pull gemma3:27b
```

#### 3. Iniciar Ollama

```powershell
ollama serve
```

Deixe esse terminal aberto (Ollama rodando em background).

#### 4. Rodar a API (em outro terminal)

```powershell
.\run_api.ps1
```

Pronto! Agora a API usa IA para análises inteligentes.

---

## 🌐 Endpoints da API

### Base URL

```
http://127.0.0.1:8000
```

### 1. Avaliar Candidato com Texto Simples ⭐ **RECOMENDADO**

**Endpoint**: `POST /evaluate-texts`

**Use quando**: Empresa e candidato digitam descrições em texto livre.

**Exemplo**:

```bash
curl -X POST http://127.0.0.1:8000/evaluate-texts \
  -H "Content-Type: application/json" \
  -d '{
    "job_text": "Procuramos desenvolvedor React Native com TypeScript e Git",
    "self_text": "Sou Ana, 2 anos com React Native e TypeScript"
  }'
```

**Resposta**:

```json
{
  "avaliacoes": [
    {
      "nome": "Ana",
      "score": 85,
      "feedback": "Habilidades presentes: react native, typescript. Faltando: git."
    }
  ]
}
```

### 2. Upload de Currículo PDF

**Endpoint**: `POST /extract-resume`

**Use quando**: Candidato tem currículo em PDF.

**Exemplo (via navegador)**:

1. Acesse: http://127.0.0.1:8000/docs
2. Expanda `POST /extract-resume`
3. Clique em "Try it out"
4. Faça upload do PDF
5. Clique em "Execute"

### 3. Outros Endpoints

Veja documentação completa: [API_DOCS.md](./API_DOCS.md)

---

## 💡 Exemplos Práticos

### Exemplo 1: Front-end JavaScript

```javascript
// Avaliar candidato vs vaga
async function avaliarCandidato() {
  const response = await fetch("http://127.0.0.1:8000/evaluate-texts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      job_text: document.getElementById("vaga").value,
      self_text: document.getElementById("candidato").value,
      use_model: true, // true = usa IA, false = usa fallback
    }),
  });

  const data = await response.json();
  const resultado = data.avaliacoes[0];

  console.log(`Score: ${resultado.score}/100`);
  console.log(`Feedback: ${resultado.feedback}`);
}
```

### Exemplo 2: Python

```python
import requests

response = requests.post('http://127.0.0.1:8000/evaluate-texts', json={
    'job_text': 'Desenvolvedor Python com Django e PostgreSQL',
    'self_text': 'Tenho 3 anos com Python e Django',
    'use_model': True
})

resultado = response.json()['avaliacoes'][0]
print(f"Score: {resultado['score']}/100")
print(f"Feedback: {resultado['feedback']}")
```

### Exemplo 3: PowerShell

```powershell
$body = @{
    job_text = "Desenvolvedor React Native"
    self_text = "2 anos com React Native"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/evaluate-texts `
                  -Method POST `
                  -ContentType "application/json" `
                  -Body $body
```

---

## 🔍 Testando a API

### Teste 1: Health Check

```powershell
# PowerShell
Invoke-WebRequest http://127.0.0.1:8000/health

# Ou navegador
# http://127.0.0.1:8000/health
```

**Resultado esperado**:

```json
{
  "status": "ok",
  "use_model_default": true,
  "ollama_model": "llama3.2:3b",
  "ollama_url": "http://127.0.0.1:11434/api/generate"
}
```

### Teste 2: Documentação Interativa

Acesse: http://127.0.0.1:8000/docs

- ✅ Teste todos os endpoints visualmente
- ✅ Veja exemplos de requisição/resposta
- ✅ Execute testes direto do navegador

---

## ⚙️ Configuração Avançada

### Mudar Modelo Ollama

```powershell
.\run_api.ps1 -Model "gemma3:27b"
```

### Mudar Porta

```powershell
.\run_api.ps1 -Port 8080
```

### Configurar CORS (para front em outra porta)

```powershell
.\run_api.ps1 -Cors "http://localhost:3000,http://localhost:5173"
```

### Desabilitar IA (usar apenas fallback)

No arquivo `api/server.py`, linha 14:

```python
USE_MODEL_DEFAULT = False  # Mude de True para False
```

---

## 🐛 Troubleshooting

### Problema: "python não é reconhecido"

**Solução**:

1. Reinstale Python marcando "Add Python to PATH"
2. OU adicione manualmente:
   - Painel de Controle → Sistema → Variáveis de Ambiente
   - Adicione `C:\Python310` e `C:\Python310\Scripts` ao PATH

### Problema: "uvicorn não é reconhecido"

**Solução**: Use o script fornecido:

```powershell
.\run_api.ps1
```

O script cria ambiente virtual e instala tudo automaticamente.

### Problema: "Ollama não conecta"

**Sintomas**: API funciona mas score sempre 0 ou genérico.

**Solução**:

1. Verifique se Ollama está rodando:
   ```powershell
   ollama list
   ```
2. Se não estiver, inicie:
   ```powershell
   ollama serve
   ```
3. Baixe um modelo:
   ```powershell
   ollama pull llama3.2:3b
   ```

### Problema: "Porta 8000 já está em uso"

**Solução**: Use outra porta:

```powershell
.\run_api.ps1 -Port 8080
```

### Problema: Erro 403 CORS no front

**Solução**: Configure CORS:

```powershell
.\run_api.ps1 -Cors "http://localhost:3000"
```

### Problema: API lenta

**Causas possíveis**:

1. Modelo Ollama muito grande → Use `llama3.2:3b` (2GB)
2. CPU lento → Considere usar fallback (`use_model: false`)
3. Primeira requisição sempre demora (carrega o modelo)

**Solução**:

```powershell
# Use modelo menor
.\run_api.ps1 -Model "llama3.2:3b"

# OU desabilite IA para testes rápidos
# (edite api/server.py, linha 14: USE_MODEL_DEFAULT = False)
```

---

## 📁 Estrutura do Projeto

```
Disruptive Architectures IOT & IA/
├── api/
│   ├── __init__.py
│   ├── server.py                    # FastAPI app principal
│   ├── models.py                    # Modelos Pydantic
│   └── services/
│       ├── ollama_client.py         # Cliente HTTP do Ollama
│       └── pdf_reader.py            # Extrator de PDF
├── run_api.ps1                      # Script de inicialização
├── stop_api.ps1                     # Script para parar API
├── requirements.txt                 # Dependências Python
├── job_fit_score_ollama.py          # Script standalone
├── job_fit_score_ollama.ipynb       # Jupyter Notebook
├── README.md                        # Este arquivo
├── API_INTEGRATION.md               # 📘 Documentação completa da API
└── JAVA_INTEGRATION_EXAMPLES.md    # ☕ Exemplos práticos Java
```

## 📚 Documentação

- **[README.md](./README.md)** - Guia de início rápido (você está aqui!)
- **[API_INTEGRATION.md](./API_INTEGRATION.md)** - Documentação completa da API
  - Todos os endpoints detalhados
  - DTOs e modelos Java completos
  - Cliente WebClient configurado
  - Exemplos de integração
- **[JAVA_INTEGRATION_EXAMPLES.md](./JAVA_INTEGRATION_EXAMPLES.md)** - Exemplos práticos Java
  - Setup completo passo a passo
  - Integração com Candidaturas
  - Upload de currículo
  - Tratamento de erros
  - Testes unitários

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

---

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos (Global Solution - FIAP).

---

## 🆘 Suporte

**Problemas comuns**: Veja [Troubleshooting](#-troubleshooting)

**Documentação técnica**: [API_DOCS.md](./API_DOCS.md)

**Issues**: Abra uma issue no repositório

---

## ✨ Features

- ✅ 7 endpoints REST diferentes
- ✅ Suporte a texto livre (empresa + candidato)
- ✅ Upload de currículo em PDF
- ✅ IA local com Ollama (opcional)
- ✅ Fallback determinístico (sempre funciona)
- ✅ CORS configurável
- ✅ Documentação interativa (Swagger)
- ✅ Script de instalação automática
- ✅ Score de 0-100 + feedback detalhado

---

## 🚦 Quick Start (1 minuto)

```powershell
# 1. Clone o projeto
git clone [URL]
cd "GS-JobFitScore\Disruptive Architectures IOT & IA"

# 2. Configure permissões (só uma vez)
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force

# 3. Rode a API
.\run_api.ps1

# 4. Teste no navegador
# http://127.0.0.1:8000/docs
```

**Pronto!** 🎉 A API está rodando e pronta para usar.

---

## 📊 Exemplo de Resposta

```json
{
  "avaliacoes": [
    {
      "nome": "João Silva",
      "score": 78,
      "feedback": "Habilidades presentes: react native, javascript, git. Faltando: typescript, ui/ux básico. Cursos relacionados: 1."
    }
  ]
}
```

**Score**:

- 0-40: Baixa compatibilidade
- 41-70: Compatibilidade moderada
- 71-100: Alta compatibilidade

---

**Desenvolvido com ❤️ para Global Solution - FIAP 2025**
