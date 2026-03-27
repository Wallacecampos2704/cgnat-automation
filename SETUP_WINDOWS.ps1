# ============================================================================
# CGNAT Dashboard - Script de Setup para Windows (PowerShell)
# Cria repositório GitHub e publica no Streamlit Cloud automaticamente
# ============================================================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                   CGNAT Dashboard - Setup Automático                         ║" -ForegroundColor Cyan
Write-Host "║                     Criar GitHub + Publicar Streamlit                        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar se Git está instalado
Write-Host "🔍 Verificando Git..." -ForegroundColor Yellow
git --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git não está instalado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Baixe em: https://git-scm.com/download/win" -ForegroundColor Green
    Write-Host "Depois execute este script novamente." -ForegroundColor Green
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "✅ Git detectado" -ForegroundColor Green

# Verificar se Python está instalado
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow
python --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python não está instalado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Baixe em: https://www.python.org/downloads/" -ForegroundColor Green
    Write-Host "IMPORTANTE: Marque 'Add Python to PATH' durante instalação" -ForegroundColor Green
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "✅ Python detectado" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Configuração Inicial" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Cyan

$GITHUB_USER = Read-Host "Digite seu usuário GitHub (ex: Wallacecampos2704)"
$GITHUB_EMAIL = Read-Host "Digite seu email GitHub"
$GITHUB_TOKEN = Read-Host "Digite seu Personal Access Token do GitHub" -AsSecureString

# Converter token para texto
$GITHUB_TOKEN_TEXT = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($GITHUB_TOKEN))

Write-Host ""
Write-Host "Seu usuário: $GITHUB_USER" -ForegroundColor Green
Write-Host "Seu email: $GITHUB_EMAIL" -ForegroundColor Green
Write-Host "Token: ******* (oculto)" -ForegroundColor Green
Write-Host ""

Read-Host "Pressione Enter para continuar"

# Configurar Git globalmente
Write-Host ""
Write-Host "🔧 Configurando Git..." -ForegroundColor Yellow
git config --global user.name "$GITHUB_USER"
git config --global user.email "$GITHUB_EMAIL"
Write-Host "✅ Git configurado" -ForegroundColor Green

# Criar pasta do projeto
Write-Host ""
Write-Host "📁 Criando pasta do projeto..." -ForegroundColor Yellow
$PROJECT_DIR = "$env:USERPROFILE\cgnat-automation"

if (Test-Path $PROJECT_DIR) {
    Write-Host "⚠️  Pasta já existe. Removendo..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $PROJECT_DIR
}

New-Item -ItemType Directory -Path $PROJECT_DIR | Out-Null
Set-Location $PROJECT_DIR
Write-Host "✅ Pasta criada: $PROJECT_DIR" -ForegroundColor Green

# Inicializar repositório Git
Write-Host ""
Write-Host "🔄 Inicializando repositório Git..." -ForegroundColor Yellow
git init
git config user.name "$GITHUB_USER"
git config user.email "$GITHUB_EMAIL"
Write-Host "✅ Repositório inicializado" -ForegroundColor Green

# Criar arquivo .gitignore
Write-Host ""
Write-Host "📝 Criando .gitignore..." -ForegroundColor Yellow
@"
__pycache__/
*.py[cod]
*.so
.Python
venv/
ENV/
.venv
.streamlit/secrets.toml
*.csv
*.json
*.db
*.log
.env
.DS_Store
"@ | Out-File -Encoding UTF8 ".gitignore"
Write-Host "✅ .gitignore criado" -ForegroundColor Green

# Criar README.md
Write-Host ""
Write-Host "📝 Criando README.md..." -ForegroundColor Yellow
@"
# CGNAT Dashboard - Automação Completa

Solução de automação para CGNAT no Brasil com dados vivos, calculadora de ROI e diagnóstico regional.

## 🚀 Início Rápido

``````bash
pip install -r requirements.txt
streamlit run app.py
``````

## 📊 Funcionalidades

- Dashboard com dados vivos
- Calculadora de ROI
- Diagnóstico regional
- Feed de notícias
- Atualização automática

## 📞 Suporte

Veja GUIA_PUBLICACAO.md para instruções completas.
"@ | Out-File -Encoding UTF8 "README.md"
Write-Host "✅ README.md criado" -ForegroundColor Green

# Criar requirements.txt
Write-Host ""
Write-Host "📝 Criando requirements.txt..." -ForegroundColor Yellow
@"
streamlit==1.28.1
pandas==2.1.3
requests==2.31.0
python-dateutil==2.8.2
beautifulsoup4==4.12.2
"@ | Out-File -Encoding UTF8 "requirements.txt"
Write-Host "✅ requirements.txt criado" -ForegroundColor Green

# Fazer primeiro commit
Write-Host ""
Write-Host "📤 Fazendo primeiro commit..." -ForegroundColor Yellow
git add .
git commit -m "Inicializar repositório CGNAT Dashboard"
Write-Host "✅ Commit realizado" -ForegroundColor Green

# Criar repositório no GitHub via API
Write-Host ""
Write-Host "🌐 Criando repositório no GitHub..." -ForegroundColor Yellow
Write-Host ""

$headers = @{
    "Authorization" = "token $GITHUB_TOKEN_TEXT"
    "Content-Type" = "application/json"
}

$body = @{
    name = "cgnat-automation"
    description = "Dashboard CGNAT com dados vivos, ROI e diagnóstico regional"
    private = $false
    auto_init = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method POST `
        -Headers $headers `
        -Body $body `
        -ErrorAction Stop
    
    Write-Host "✅ Repositório criado no GitHub" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao criar repositório no GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifique:" -ForegroundColor Yellow
    Write-Host "1. Seu token do GitHub está correto?" -ForegroundColor Yellow
    Write-Host "2. Você tem permissão para criar repositórios?" -ForegroundColor Yellow
    Write-Host ""
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Adicionar remote e fazer push
Write-Host ""
Write-Host "📤 Fazendo upload para GitHub..." -ForegroundColor Yellow

git remote add origin "https://${GITHUB_USER}:${GITHUB_TOKEN_TEXT}@github.com/${GITHUB_USER}/cgnat-automation.git"
git branch -M main
git push -u origin main 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao fazer push" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente manualmente:" -ForegroundColor Yellow
    Write-Host "git push -u origin main" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "✅ Upload concluído!" -ForegroundColor Green

# Exibir resumo
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                           ✅ SUCESSO!                                        ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Seu repositório está em:" -ForegroundColor Cyan
Write-Host "   https://github.com/$GITHUB_USER/cgnat-automation" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Próximos Passos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Copie os arquivos do projeto para: $PROJECT_DIR" -ForegroundColor Yellow
Write-Host "   - app.py" -ForegroundColor Yellow
Write-Host "   - dados_vivos.py" -ForegroundColor Yellow
Write-Host "   - calculadora_roi.py" -ForegroundColor Yellow
Write-Host "   - diagnostico_regional.py" -ForegroundColor Yellow
Write-Host "   - noticias.py" -ForegroundColor Yellow
Write-Host "   - GUIA_PUBLICACAO.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Faça commit e push:" -ForegroundColor Yellow
Write-Host "   cd $PROJECT_DIR" -ForegroundColor Yellow
Write-Host "   git add ." -ForegroundColor Yellow
Write-Host "   git commit -m 'Adicionar arquivos do CGNAT Dashboard'" -ForegroundColor Yellow
Write-Host "   git push origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Publicar no Streamlit Cloud:" -ForegroundColor Yellow
Write-Host "   - Acesse https://share.streamlit.io" -ForegroundColor Yellow
Write-Host "   - Clique 'New app'" -ForegroundColor Yellow
Write-Host "   - Selecione seu repositório" -ForegroundColor Yellow
Write-Host "   - Escolha app.py" -ForegroundColor Yellow
Write-Host "   - Clique 'Deploy!'" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Seu dashboard estará em:" -ForegroundColor Yellow
Write-Host "   https://$GITHUB_USER-cgnat-automation.streamlit.app" -ForegroundColor Green
Write-Host ""
Write-Host "═════════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Read-Host "Pressione Enter para sair"
