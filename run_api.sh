#!/bin/bash

# Detecta o sistema operacional
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "macOS";;
        CYGWIN*|MINGW*|MSYS*) echo "Windows";;
        *)          echo "Unknown";;
    esac
}

OS=$(detect_os)

# Configuração padrão
HOST_URL="127.0.0.1"
PORT=8000
MODEL="llama3.2:3b"
OLLAMA_URL="http://127.0.0.1:11434/api/generate"
CORS="*"
NO_INSTALL=false

# Parse de argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST_URL="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --ollama-url)
            OLLAMA_URL="$2"
            shift 2
            ;;
        --cors)
            CORS="$2"
            shift 2
            ;;
        --no-install)
            NO_INSTALL=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [opções]"
            echo "Opções:"
            echo "  --host <url>         URL do host (padrão: 127.0.0.1)"
            echo "  --port <porta>       Porta do servidor (padrão: 8000)"
            echo "  --model <modelo>     Modelo Ollama (padrão: llama3.2:3b)"
            echo "  --ollama-url <url>   URL da API Ollama (padrão: http://127.0.0.1:11434/api/generate)"
            echo "  --cors <origem>      Origens CORS (padrão: *)"
            echo "  --no-install         Pula instalação de dependências"
            echo "  -h, --help           Mostra esta ajuda"
            exit 0
            ;;
        *)
            echo "Opção desconhecida: $1"
            echo "Use --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

set -e  # Para em caso de erro

# Obtém a pasta do script (raiz do projeto)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo -e "\e[36m== GS-JobFitScore API ==\e[0m"
echo "Pasta do projeto: $ROOT"
echo "Sistema Operacional: $OS"

# 1) Verifica Python
PYTHON_CMD="python3"

# No Windows com Git Bash/MSYS, tenta python primeiro
if [ "$OS" = "Windows" ]; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        echo -e "\e[31mErro: Python não encontrado no PATH. Instale o Python 3.10+ e tente novamente.\e[0m"
        exit 1
    fi
else
    if ! command -v python3 &> /dev/null; then
        echo -e "\e[31mErro: Python3 não encontrado no PATH. Instale o Python 3.10+ e tente novamente.\e[0m"
        exit 1
    fi
fi

echo "Usando comando Python: $PYTHON_CMD"

# 2) Cria venv se necessário
VENV_PATH="$ROOT/.venv"

# Define o caminho do Python no venv baseado no OS
if [ "$OS" = "Windows" ]; then
    VENV_PYTHON="$VENV_PATH/Scripts/python.exe"
else
    VENV_PYTHON="$VENV_PATH/bin/python"
fi

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Criando ambiente virtual (.venv)..."
    "$PYTHON_CMD" -m venv ".venv"
fi

# 3) Atualiza pip e instala dependências
echo "Atualizando pip..."
"$VENV_PYTHON" -m pip install --upgrade pip

if [ "$NO_INSTALL" = false ]; then
    REQ_FILE="$ROOT/requirements.txt"
    if [ -f "$REQ_FILE" ]; then
        echo "Instalando dependências de requirements.txt..."
        "$VENV_PYTHON" -m pip install -r "$REQ_FILE"
    else
        echo -e "\e[33mAviso: requirements.txt não encontrado. Pulando instalação.\e[0m"
    fi
else
    echo "--no-install: pulando instalação de dependências."
fi

# 4) Variáveis de ambiente para esta sessão
export OLLAMA_MODEL="$MODEL"
export OLLAMA_URL="$OLLAMA_URL"
export USE_MODEL="true"
export CORS_ORIGINS="$CORS"

echo -e "\e[33mVariáveis de ambiente:\e[0m"
echo "  OLLAMA_MODEL = $OLLAMA_MODEL"
echo "  OLLAMA_URL   = $OLLAMA_URL"
echo "  USE_MODEL    = $USE_MODEL"
echo "  CORS_ORIGINS = $CORS_ORIGINS"

# 5) Inicia o servidor
echo -e "\n\e[32mIniciando API em http://$HOST_URL:$PORT ... (Ctrl + C para parar)\e[0m"

trap 'echo -e "\n\nAPI finalizada."; exit 0' INT TERM

"$VENV_PYTHON" -m uvicorn api.server:app --host "$HOST_URL" --port "$PORT"
