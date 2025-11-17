#!/bin/bash

# Script para encerrar a API GS-JobFitScore
# Modo de uso: ./stop_api.sh

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

echo -e "\e[33m🛑 Encerrando GS-JobFitScore API...\e[0m"

# Função para encontrar processos no Windows
find_processes_windows() {
    local name=$1
    tasklist //FI "IMAGENAME eq $name" 2>/dev/null | grep -i "$name" | awk '{print $2}'
}

# Função para encerrar processo no Windows
kill_process_windows() {
    local pid=$1
    taskkill //PID "$pid" //F 2>/dev/null
}

# Encerra processos do Uvicorn (API FastAPI)
echo -e "\n\e[36m📍 Procurando processos do Uvicorn...\e[0m"

if [ "$OS" = "Windows" ]; then
    # Windows via Git Bash/MSYS
    UVICORN_PIDS=$(ps aux | grep -i "[u]vicorn" | awk '{print $1}')
    
    if [ -n "$UVICORN_PIDS" ]; then
        COUNT=$(echo "$UVICORN_PIDS" | wc -l)
        echo -e "   \e[32mEncontrados $COUNT processo(s) do Uvicorn\e[0m"
        
        for PID in $UVICORN_PIDS; do
            echo -e "   \e[33mEncerrando PID: $PID\e[0m"
            kill -9 "$PID" 2>/dev/null || taskkill //PID "$PID" //F 2>/dev/null
        done
        echo -e "   \e[32m✅ API encerrada com sucesso\e[0m"
    else
        echo -e "   \e[90mℹ️  Nenhum processo da API encontrado\e[0m"
    fi
else
    # Linux e macOS
    UVICORN_PIDS=$(pgrep -f "uvicorn.*api.server:app" 2>/dev/null)
    
    if [ -n "$UVICORN_PIDS" ]; then
        COUNT=$(echo "$UVICORN_PIDS" | wc -l)
        echo -e "   \e[32mEncontrados $COUNT processo(s) do Uvicorn\e[0m"
        
        for PID in $UVICORN_PIDS; do
            echo -e "   \e[33mEncerrando PID: $PID\e[0m"
            kill -9 "$PID" 2>/dev/null
        done
        echo -e "   \e[32m✅ API encerrada com sucesso\e[0m"
    else
        echo -e "   \e[90mℹ️  Nenhum processo da API encontrado\e[0m"
    fi
fi

# Encerra processos do Ollama (opcional)
echo -e "\n\e[36m📍 Procurando processos do Ollama...\e[0m"

if [ "$OS" = "Windows" ]; then
    OLLAMA_PIDS=$(ps aux | grep -i "[o]llama" | awk '{print $1}')
else
    OLLAMA_PIDS=$(pgrep -f "ollama" 2>/dev/null)
fi

if [ -n "$OLLAMA_PIDS" ]; then
    COUNT=$(echo "$OLLAMA_PIDS" | wc -l)
    echo -e "   \e[32mEncontrados $COUNT processo(s) do Ollama\e[0m"
    
    read -p "   Deseja encerrar o Ollama também? (s/N): " -n 1 -r RESPONSE
    echo
    
    if [[ $RESPONSE =~ ^[SsYy]$ ]]; then
        for PID in $OLLAMA_PIDS; do
            echo -e "   \e[33mEncerrando PID: $PID\e[0m"
            if [ "$OS" = "Windows" ]; then
                kill -9 "$PID" 2>/dev/null || taskkill //PID "$PID" //F 2>/dev/null
            else
                kill -9 "$PID" 2>/dev/null
            fi
        done
        echo -e "   \e[32m✅ Ollama encerrado com sucesso\e[0m"
    else
        echo -e "   \e[90m⏭️  Ollama mantido em execução\e[0m"
    fi
else
    echo -e "   \e[90mℹ️  Nenhum processo do Ollama encontrado\e[0m"
fi

# Libera porta 8000 (caso algum processo esteja usando)
echo -e "\n\e[36m📍 Verificando porta 8000...\e[0m"

if [ "$OS" = "Windows" ]; then
    # Windows
    PORT_PID=$(netstat -ano | grep ":8000.*LISTENING" | awk '{print $5}' | head -1)
    
    if [ -n "$PORT_PID" ]; then
        echo -e "   \e[33mProcesso usando porta 8000 (PID: $PORT_PID)\e[0m"
        taskkill //PID "$PORT_PID" //F 2>/dev/null
        echo -e "   \e[32m✅ Porta 8000 liberada\e[0m"
    else
        echo -e "   \e[90mℹ️  Porta 8000 já está livre\e[0m"
    fi
elif [ "$OS" = "macOS" ]; then
    # macOS
    PORT_PID=$(lsof -ti:8000 2>/dev/null)
    
    if [ -n "$PORT_PID" ]; then
        echo -e "   \e[33mProcesso usando porta 8000 (PID: $PORT_PID)\e[0m"
        kill -9 "$PORT_PID" 2>/dev/null
        echo -e "   \e[32m✅ Porta 8000 liberada\e[0m"
    else
        echo -e "   \e[90mℹ️  Porta 8000 já está livre\e[0m"
    fi
else
    # Linux
    PORT_PID=$(ss -lptn 'sport = :8000' 2>/dev/null | grep -oP 'pid=\K[0-9]+' | head -1)
    
    if [ -z "$PORT_PID" ]; then
        # Fallback para lsof se ss não funcionar
        PORT_PID=$(lsof -ti:8000 2>/dev/null)
    fi
    
    if [ -n "$PORT_PID" ]; then
        echo -e "   \e[33mProcesso usando porta 8000 (PID: $PORT_PID)\e[0m"
        kill -9 "$PORT_PID" 2>/dev/null
        echo -e "   \e[32m✅ Porta 8000 liberada\e[0m"
    else
        echo -e "   \e[90mℹ️  Porta 8000 já está livre\e[0m"
    fi
fi

echo -e "\n\e[32m✅ Encerramento concluído!\e[0m"
echo -e "   \e[36mPara reiniciar, execute: ./start_api.sh\e[0m"

# Aguarda 3 segundos antes de fechar
sleep 3
