# PowerShell script to start the AI-Powered CSV Analysis App

Write-Host "🚀 Starting AI-Powered CSV Analysis App..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ and add it to PATH." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if requirements are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask, pandas, plotly, openai" 2>$null
    Write-Host "✅ All dependencies are installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Some dependencies missing. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check OpenAI API key
$apiKey = $env:OPENAI_API_KEY
if ($apiKey) {
    Write-Host "✅ OpenAI API key found" -ForegroundColor Green
} else {
    Write-Host "⚠️  OpenAI API key not set. AI insights will not work." -ForegroundColor Yellow
    Write-Host "Set it with: `$env:OPENAI_API_KEY='your_key_here'" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🌐 Starting Flask application..." -ForegroundColor Green
Write-Host "📱 Open your browser and go to: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the Flask app
try {
    python app.py
} catch {
    Write-Host "❌ Error starting Flask application: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
} 