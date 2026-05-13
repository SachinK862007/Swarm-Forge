Write-Host "Starting SwarmForge services..."
# Start Ollama (if not running)
$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue
if (-not $ollamaProcess) {
    Write-Host "Starting Ollama..."
    Start-Process ollama -ArgumentList "serve" -WindowStyle Minimized
    Start-Sleep 3
} else {
    Write-Host "Ollama is already running."
}
# Start FastAPI backend
Write-Host "Starting FastAPI backend..."
$backendDir = Join-Path $PSScriptRoot "..\backend"
$venvActivate = Join-Path $PSScriptRoot "..\venv_swarm\Scripts\Activate.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; . '$venvActivate'; uvicorn main:app --reload --port 8000"
Write-Host "Backend launched in new window."
# Start Streamlit frontend (if frontend/app.py exists)
$frontendDir = Join-Path $PSScriptRoot "..\frontend"
if (Test-Path (Join-Path $frontendDir "app.py")) {
    Write-Host "Starting Streamlit dashboard..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; . '$venvActivate'; streamlit run app.py"
} else {
    Write-Host "Frontend not yet created; skipping Streamlit."
}
Write-Host "All services launched."
