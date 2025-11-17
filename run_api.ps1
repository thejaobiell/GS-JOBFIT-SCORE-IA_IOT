param(
    [string]$HostUrl = "127.0.0.1",
    [int]$Port = 8000,
    [string]$Model = "llama3.2:3b",
    [string]$OllamaUrl = "http://127.0.0.1:11434/api/generate",
    [string]$Cors = "*",
    [switch]$NoInstall
)

$ErrorActionPreference = "Stop"

# Navega até a pasta do script (raiz do projeto)
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "== GS-JobFitScore API ==" -ForegroundColor Cyan
Write-Host "Pasta do projeto: $root"

# 1) Verifica Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python não encontrado no PATH. Instale o Python 3.10+ e tente novamente."
    exit 1
}

# 2) Cria venv se necessário
$venvPath = Join-Path $root ".venv"
$venvPython = Join-Path $venvPath "Scripts/python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Criando ambiente virtual (.venv)..."
    python -m venv ".venv"
}

# 3) Atualiza pip e instala dependências
Write-Host "Atualizando pip..."
& $venvPython -m pip install --upgrade pip | Out-Host

if (-not $NoInstall) {
    $reqFile = Join-Path $root "requirements.txt"
    if (Test-Path $reqFile) {
        Write-Host "Instalando dependências de requirements.txt..."
        & $venvPython -m pip install -r $reqFile | Out-Host
    }
    else {
        Write-Warning "requirements.txt não encontrado. Pulando instalação."
    }
}
else {
    Write-Host "--NoInstall: pulando instalação de dependências."
}

# 4) Variáveis de ambiente para esta sessão
$env:OLLAMA_MODEL = $Model
$env:OLLAMA_URL = $OllamaUrl
$env:USE_MODEL = "true"
$env:CORS_ORIGINS = $Cors

Write-Host "Variáveis de ambiente:" -ForegroundColor Yellow
Write-Host "  OLLAMA_MODEL = $($env:OLLAMA_MODEL)"
Write-Host "  OLLAMA_URL   = $($env:OLLAMA_URL)"
Write-Host "  USE_MODEL    = $($env:USE_MODEL)"
Write-Host "  CORS_ORIGINS = $($env:CORS_ORIGINS)"

# 5) Inicia o servidor
Write-Host ("`nIniciando API em http://{0}:{1} ... (Ctrl + C para parar)" -f $HostUrl, $Port) -ForegroundColor Green
try {
    & $venvPython -m uvicorn api.server:app --host $HostUrl --port $Port
}
catch {
    Write-Error "Falha ao iniciar a API: $($_.Exception.Message)"
}
finally {
    Write-Host "\nAPI finalizada."
    Read-Host "Pressione Enter para fechar"
}
