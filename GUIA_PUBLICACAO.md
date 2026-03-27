# 📱 Guia Completo: Como Publicar e Manter o Dashboard

## 🎯 Visão Geral

Este guia mostra como publicar seu dashboard **gratuitamente** no Streamlit Cloud e mantê-lo atualizado automaticamente.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Passo 1: Preparar o Repositório GitHub](#passo-1-preparar-o-repositório-github)
3. [Passo 2: Deploy no Streamlit Cloud](#passo-2-deploy-no-streamlit-cloud)
4. [Passo 3: Atualização Automática](#passo-3-atualização-automática)
5. [Passo 4: Melhorias de UI (Cores e Seleção)](#passo-4-melhorias-de-ui-cores-e-seleção)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

Você precisa ter:
- ✅ Conta no GitHub (gratuita)
- ✅ Conta no Streamlit Cloud (gratuita)
- ✅ Git instalado no seu computador
- ✅ Python 3.8+ instalado

### Instalar Git (se não tiver)

**Windows:**
```bash
# Baixar de: https://git-scm.com/download/win
# Ou usar Chocolatey:
choco install git
```

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt-get install git
```

---

## 📍 Passo 1: Preparar o Repositório GitHub

### 1.1 Criar Conta no GitHub

1. Acesse [github.com](https://github.com)
2. Clique em "Sign up"
3. Preencha email, senha e nome de usuário
4. Confirme seu email

### 1.2 Criar Novo Repositório

1. Clique no ➕ (canto superior direito)
2. Selecione "New repository"
3. Preencha:
   - **Repository name**: `cgnat-automation` (ou outro nome)
   - **Description**: "Dashboard CGNAT com dados vivos, ROI e diagnóstico regional"
   - **Public**: ✅ (deve ser público para Streamlit Cloud)
   - **Add a README file**: ✅
   - **Add .gitignore**: Selecione "Python"
4. Clique "Create repository"

### 1.3 Clonar o Repositório Localmente

```bash
# Abra o terminal/PowerShell

# Clone o repositório
git clone https://github.com/seu-usuario/cgnat-automation.git

# Entre na pasta
cd cgnat-automation
```

### 1.4 Adicionar os Arquivos

```bash
# Copie todos os arquivos do projeto para esta pasta:
# - app.py
# - dados_vivos.py
# - calculadora_roi.py
# - diagnostico_regional.py
# - noticias.py
# - requirements.txt
# - README.md
# - .gitignore

# Verificar arquivos
ls -la

# Adicionar todos os arquivos ao Git
git add .

# Fazer commit
git commit -m "Adicionar CGNAT Dashboard com dados vivos, ROI e notícias"

# Enviar para GitHub
git push origin main
```

**Resultado esperado:**
```
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 8 threads
To https://github.com/seu-usuario/cgnat-automation.git
   abc1234..def5678  main -> main
```

---

## 🚀 Passo 2: Deploy no Streamlit Cloud

### 2.1 Criar Conta no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em "Sign up"
3. Selecione "Sign up with GitHub"
4. Autorize o Streamlit a acessar seus repositórios

### 2.2 Deploy da Aplicação

1. Clique em "New app"
2. Preencha:
   - **Repository**: `seu-usuario/cgnat-automation`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Clique "Deploy!"

**Aguarde 2-3 minutos...**

Seu app estará disponível em:
```
https://seu-usuario-cgnat-automation.streamlit.app
```

### 2.3 Compartilhar o Link

Copie a URL e compartilhe com seus clientes/colegas:
```
https://seu-usuario-cgnat-automation.streamlit.app
```

---

## 🔄 Passo 3: Atualização Automática

### 3.1 Como Funciona

O dashboard atualiza em **3 níveis**:

| Nível | O que atualiza | Frequência | Como funciona |
|-------|---|---|---|
| **Cache Local** | Dados Vivos (IBC, IPv6) | 1 hora | Streamlit cache automático |
| **Notícias** | Feed de notícias | 6 horas | Cache local do módulo |
| **Cálculos** | ROI e Diagnóstico | Instantâneo | Cálculo em tempo real |

### 3.2 Reduzir Tempo de Cache

Se quiser atualizar mais frequentemente, edite `app.py`:

```python
# Linha 94 - Mudar de 3600 para 300 (5 minutos)
@st.cache_data(ttl=300)  # ← Muda de 1 hora para 5 minutos
def carregar_dados_vivos():
    integrador = IntegradorDadosVivos()
    return integrador.atualizar_todos_dados()
```

Depois faça commit e push:
```bash
git add app.py
git commit -m "Reduzir cache para 5 minutos"
git push origin main
```

**O Streamlit Cloud fará deploy automático em 1-2 minutos!**

### 3.3 Atualização Manual

Se quiser forçar atualização imediata:

1. Acesse seu dashboard no Streamlit Cloud
2. Clique no ☰ (menu, canto superior direito)
3. Selecione "Rerun"

---

## 🎨 Passo 4: Melhorias de UI (Cores e Seleção)

### 4.1 Problema: Campos Ficam Brancos ao Selecionar

**Solução:** O CSS já foi adicionado ao `app.py` (linhas 54-65).

Quando você seleciona um campo (Region, Criticidade, Estado), ele fica:
- ✅ Fundo azul (#3b82f6)
- ✅ Texto em negrito
- ✅ Fácil de ver

### 4.2 Customizar Cores

Se quiser mudar as cores, edite `app.py` (linhas 25-85):

```python
# Exemplo: Mudar cor de seleção de azul para verde
.stSelectbox > div > div[data-selected] {
    background-color: #10b981 !important;  # ← Verde em vez de azul
    font-weight: bold !important;
}
```

Depois faça commit:
```bash
git add app.py
git commit -m "Mudar cor de seleção para verde"
git push origin main
```

### 4.3 Cores Disponíveis

Use qualquer cor em formato hexadecimal:

```
Azul:        #3b82f6
Verde:       #10b981
Vermelho:    #ef4444
Amarelo:     #f59e0b
Roxo:        #a78bfa
Laranja:     #f97316
```

---

## ⏰ Passo 5: Agendamento de Atualização (Avançado)

Se quiser que o dashboard **se atualize sozinho** a cada X horas:

### 5.1 Usar GitHub Actions (Gratuito)

Crie o arquivo `.github/workflows/update.yml`:

```yaml
name: Atualizar Dados

on:
  schedule:
    # Executar a cada 6 horas
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Instalar dependências
        run: |
          pip install -r requirements.txt
      
      - name: Atualizar dados
        run: |
          python3 dados_vivos.py
          python3 noticias.py
      
      - name: Fazer commit
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "Atualizar dados automaticamente" || true
          git push
```

**Como adicionar:**

1. Crie a pasta `.github/workflows/` no seu repositório
2. Crie o arquivo `update.yml` dentro dela
3. Faça commit e push

```bash
mkdir -p .github/workflows
# Criar o arquivo update.yml com o conteúdo acima
git add .github/workflows/update.yml
git commit -m "Adicionar atualização automática com GitHub Actions"
git push origin main
```

---

## 🐛 Troubleshooting

### Problema 1: "Module not found: noticias"

**Solução:**
```bash
# Verificar se o arquivo noticias.py existe
ls -la noticias.py

# Se não existir, copie-o para o repositório
# Depois faça commit:
git add noticias.py
git commit -m "Adicionar módulo de notícias"
git push origin main
```

### Problema 2: Dashboard não atualiza

**Solução:**
1. Acesse seu dashboard
2. Clique no ☰ (menu superior direito)
3. Selecione "Rerun"
4. Se ainda não funcionar, aguarde 5 minutos

### Problema 3: Erro "BeautifulSoup not found"

**Solução:** Adicione ao `requirements.txt`:
```
beautifulsoup4==4.12.2
```

Depois:
```bash
git add requirements.txt
git commit -m "Adicionar beautifulsoup4 às dependências"
git push origin main
```

### Problema 4: Cores não mudam ao selecionar

**Solução:** Limpe o cache do navegador:
- Windows: `Ctrl + Shift + Delete`
- Mac: `Cmd + Shift + Delete`
- Linux: `Ctrl + Shift + Delete`

Depois recarregue a página.

---

## 📊 Monitorar seu Dashboard

### Ver Logs

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique no seu app
3. Clique em "Manage app"
4. Veja a aba "Logs"

### Ver Estatísticas

1. Clique em "Settings"
2. Veja quantas pessoas acessaram seu app
3. Veja o uso de memória e CPU

---

## 🔐 Segurança

### Proteger seu Dashboard com Senha

Crie o arquivo `.streamlit/secrets.toml`:

```toml
[credentials]
username = "seu-usuario"
password = "sua-senha-segura"
```

Depois adicione ao `app.py`:

```python
import streamlit as st

# Verificar autenticação
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Login"):
        if username == st.secrets["credentials"]["username"] and \
           password == st.secrets["credentials"]["password"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# Resto do código aqui...
```

---

## 📈 Próximos Passos

1. ✅ Deploy no Streamlit Cloud
2. ✅ Compartilhar link com clientes
3. ✅ Monitorar acessos
4. ✅ Customizar cores e branding
5. ✅ Adicionar autenticação (opcional)
6. ✅ Integrar com seu CRM

---

## 🎓 Resumo

| Etapa | Tempo | Dificuldade |
|-------|-------|-------------|
| Criar conta GitHub | 5 min | ⭐ Fácil |
| Fazer upload do código | 10 min | ⭐ Fácil |
| Deploy no Streamlit | 5 min | ⭐ Fácil |
| Customizar cores | 5 min | ⭐ Fácil |
| Adicionar autenticação | 15 min | ⭐⭐ Médio |
| **Total** | **40 min** | - |

---

## 📞 Suporte

Se tiver dúvidas:

1. Verifique a [documentação do Streamlit](https://docs.streamlit.io/)
2. Abra uma issue no GitHub
3. Consulte o [Streamlit Community Forum](https://discuss.streamlit.io/)

---

## 🎉 Parabéns!

Seu dashboard está no ar! 🚀

Agora você tem:
- ✅ Dashboard com dados vivos
- ✅ Calculadora de ROI
- ✅ Diagnóstico regional
- ✅ Feed de notícias
- ✅ Atualização automática
- ✅ URL pública para compartilhar
- ✅ Código 100% seu no GitHub

**Próximo passo:** Customize para seu negócio e comece a vender! 💰
