@echo off
REM ============================================================================
REM CGNAT Dashboard - Script de Setup para Windows
REM Cria repositório GitHub e publica no Streamlit Cloud automaticamente
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════════╗
echo ║                   CGNAT Dashboard - Setup Automático                         ║
echo ║                     Criar GitHub + Publicar Streamlit                        ║
echo ╚═══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git não está instalado!
    echo.
    echo Baixe em: https://git-scm.com/download/win
    echo Depois execute este script novamente.
    pause
    exit /b 1
)

echo ✅ Git detectado

REM Pedir informações do usuário
echo.
echo 📝 Configuração Inicial
echo ─────────────────────────────────────────────────────────────────

set /p GITHUB_USER="Digite seu usuário GitHub (ex: Wallacecampos2704): "
set /p GITHUB_EMAIL="Digite seu email GitHub: "
set /p GITHUB_TOKEN="Digite seu Personal Access Token do GitHub: "

echo.
echo Seu usuário: %GITHUB_USER%
echo Seu email: %GITHUB_EMAIL%
echo Token: ******* (oculto)
echo.

pause /b

REM Configurar Git globalmente
echo.
echo 🔧 Configurando Git...
git config --global user.name "%GITHUB_USER%"
git config --global user.email "%GITHUB_EMAIL%"
echo ✅ Git configurado

REM Criar pasta do projeto
echo.
echo 📁 Criando pasta do projeto...
set PROJECT_DIR=%USERPROFILE%\cgnat-automation
if exist "%PROJECT_DIR%" (
    echo ⚠️  Pasta já existe. Removendo...
    rmdir /s /q "%PROJECT_DIR%"
)
mkdir "%PROJECT_DIR%"
cd /d "%PROJECT_DIR%"
echo ✅ Pasta criada: %PROJECT_DIR%

REM Inicializar repositório Git
echo.
echo 🔄 Inicializando repositório Git...
git init
git config user.name "%GITHUB_USER%"
git config user.email "%GITHUB_EMAIL%"
echo ✅ Repositório inicializado

REM Criar arquivo .gitignore
echo.
echo 📝 Criando .gitignore...
(
    echo __pycache__/
    echo *.py[cod]
    echo *.so
    echo .Python
    echo venv/
    echo ENV/
    echo .venv
    echo .streamlit/secrets.toml
    echo *.csv
    echo *.json
    echo *.db
    echo *.log
    echo .env
    echo .DS_Store
) > .gitignore
echo ✅ .gitignore criado

REM Criar README.md
echo.
echo 📝 Criando README.md...
(
    echo # CGNAT Dashboard - Automação Completa
    echo.
    echo Solução de automação para CGNAT no Brasil com dados vivos, calculadora de ROI e diagnóstico regional.
    echo.
    echo ## 🚀 Início Rápido
    echo.
    echo ```bash
    echo pip install -r requirements.txt
    echo streamlit run app.py
    echo ```
    echo.
    echo ## 📊 Funcionalidades
    echo.
    echo - Dashboard com dados vivos
    echo - Calculadora de ROI
    echo - Diagnóstico regional
    echo - Feed de notícias
    echo - Atualização automática
    echo.
    echo ## 📞 Suporte
    echo.
    echo Veja GUIA_PUBLICACAO.md para instruções completas.
) > README.md
echo ✅ README.md criado

REM Criar requirements.txt
echo.
echo 📝 Criando requirements.txt...
(
    echo streamlit==1.28.1
    echo pandas==2.1.3
    echo requests==2.31.0
    echo python-dateutil==2.8.2
    echo beautifulsoup4==4.12.2
) > requirements.txt
echo ✅ requirements.txt criado

REM Fazer primeiro commit
echo.
echo 📤 Fazendo primeiro commit...
git add .
git commit -m "Inicializar repositório CGNAT Dashboard"
echo ✅ Commit realizado

REM Criar repositório no GitHub via API
echo.
echo 🌐 Criando repositório no GitHub...
echo.

REM Usar curl para criar repositório
curl -X POST https://api.github.com/user/repos ^
  -H "Authorization: token %GITHUB_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"cgnat-automation\",\"description\":\"Dashboard CGNAT com dados vivos, ROI e diagnóstico regional\",\"private\":false,\"auto_init\":false}" ^
  > nul 2>&1

if errorlevel 1 (
    echo ❌ Erro ao criar repositório no GitHub
    echo.
    echo Verifique:
    echo 1. Seu token do GitHub está correto?
    echo 2. Você tem permissão para criar repositórios?
    echo.
    pause
    exit /b 1
)

echo ✅ Repositório criado no GitHub

REM Adicionar remote e fazer push
echo.
echo 📤 Fazendo upload para GitHub...
git remote add origin https://%GITHUB_USER%:%GITHUB_TOKEN%@github.com/%GITHUB_USER%/cgnat-automation.git
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo ❌ Erro ao fazer push
    echo.
    echo Tente manualmente:
    echo git push -u origin main
    echo.
    pause
    exit /b 1
)

echo ✅ Upload concluído!

REM Exibir resumo
echo.
echo ╔═══════════════════════════════════════════════════════════════════════════════╗
echo ║                           ✅ SUCESSO!                                        ║
echo ╚═══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 📍 Seu repositório está em:
echo    https://github.com/%GITHUB_USER%/cgnat-automation
echo.
echo 🚀 Próximos Passos:
echo.
echo 1. Copie os arquivos do projeto para: %PROJECT_DIR%
echo    - app.py
echo    - dados_vivos.py
echo    - calculadora_roi.py
echo    - diagnostico_regional.py
echo    - noticias.py
echo    - GUIA_PUBLICACAO.md
echo.
echo 2. Faça commit e push:
echo    cd %PROJECT_DIR%
echo    git add .
echo    git commit -m "Adicionar arquivos do CGNAT Dashboard"
echo    git push origin main
echo.
echo 3. Publicar no Streamlit Cloud:
echo    - Acesse https://share.streamlit.io
echo    - Clique "New app"
echo    - Selecione seu repositório
echo    - Escolha app.py
echo    - Clique "Deploy!"
echo.
echo 4. Seu dashboard estará em:
echo    https://%GITHUB_USER%-cgnat-automation.streamlit.app
echo.
echo ═════════════════════════════════════════════════════════════════════════════════
echo.

pause
