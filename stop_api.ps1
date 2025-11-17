# Script para encerrar a API GS-JobFitScore
# Modo de uso: .\stop_api.ps1

Write-Host "🛑 Encerrando GS-JobFitScore API..." -ForegroundColor Yellow

# Encerra processos do Uvicorn (API FastAPI)
Write-Host "`n📍 Procurando processos do Uvicorn..." -ForegroundColor Cyan
$uvicornProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*" -or $_.MainWindowTitle -like "*uvicorn*"
}

if ($uvicornProcesses) {
    Write-Host "   Encontrados $($uvicornProcesses.Count) processo(s) do Uvicorn" -ForegroundColor Green
    foreach ($proc in $uvicornProcesses) {
        Write-Host "   Encerrando PID: $($proc.Id)" -ForegroundColor Yellow
        Stop-Process -Id $proc.Id -Force
    }
    Write-Host "   ✅ API encerrada com sucesso" -ForegroundColor Green
}
else {
    Write-Host "   ℹ️  Nenhum processo da API encontrado" -ForegroundColor Gray
}

# Encerra processos do Ollama (opcional)
Write-Host "`n📍 Procurando processos do Ollama..." -ForegroundColor Cyan
$ollamaProcesses = Get-Process -Name "ollama*" -ErrorAction SilentlyContinue

if ($ollamaProcesses) {
    Write-Host "   Encontrados $($ollamaProcesses.Count) processo(s) do Ollama" -ForegroundColor Green
    
    $response = Read-Host "   Deseja encerrar o Ollama também? (s/N)"
    if ($response -eq "s" -or $response -eq "S") {
        foreach ($proc in $ollamaProcesses) {
            Write-Host "   Encerrando PID: $($proc.Id)" -ForegroundColor Yellow
            Stop-Process -Id $proc.Id -Force
        }
        Write-Host "   ✅ Ollama encerrado com sucesso" -ForegroundColor Green
    }
    else {
        Write-Host "   ⏭️  Ollama mantido em execução" -ForegroundColor Gray
    }
}
else {
    Write-Host "   ℹ️  Nenhum processo do Ollama encontrado" -ForegroundColor Gray
}

# Libera porta 8000 (caso algum processo esteja usando)
Write-Host "`n📍 Verificando porta 8000..." -ForegroundColor Cyan
$portProcess = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue

if ($portProcess) {
    $processId = $portProcess.OwningProcess
    Write-Host "   Processo usando porta 8000 (PID: $processId)" -ForegroundColor Yellow
    Stop-Process -Id $processId -Force
    Write-Host "   ✅ Porta 8000 liberada" -ForegroundColor Green
}
else {
    Write-Host "   ℹ️  Porta 8000 já está livre" -ForegroundColor Gray
}

Write-Host "`n✅ Encerramento concluído!" -ForegroundColor Green
Write-Host "   Para reiniciar, execute: .\run_api.ps1" -ForegroundColor Cyan

# Aguarda 3 segundos antes de fechar
Start-Sleep -Seconds 3
