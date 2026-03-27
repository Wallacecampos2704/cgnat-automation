# 🪟 Guia de Setup para Windows - CGNAT Dashboard

## 📋 Pré-requisitos

Você precisa ter instalado:

### 1. Git
- Baixe em: https://git-scm.com/download/win
- Execute o instalador
- Deixe as opções padrão

### 2. Python 3.8+
- Baixe em: https://www.python.org/downloads/
- **IMPORTANTE**: Marque "Add Python to PATH"
- Execute o instalador

### 3. Personal Access Token do GitHub
- Acesse: https://github.com/settings/tokens
- Clique "Generate new token (classic)"
- Preencha:
  - **Note**: "CGNAT Dashboard"
  - **Expiration**: "90 days"
  - **Scopes**: Marque "repo" (todos os subitens)
- Clique "Generate token"
- **COPIE O TOKEN** (você não verá novamente!)

---

## 🚀 Passo 1: Preparar os Arquivos

### 1.1 Criar Pasta do Projeto

Crie uma pasta em algum lugar do seu computador:

```
C:\Users\seu-usuario\Documentos\cgnat-automation
```

### 1.2 Copiar Arquivos

Copie estes arquivos para a pasta:

```
app.py
dados_vivos.py
calculadora_roi.py
diagnostico_regional.py
noticias.py
requirements.txt
README.md
GUIA_PUBLICACAO.md
```

### 1.3 Verificar Estrutura

Sua pasta deve ter:
```
cgnat-automation/
├── app.py
├── dados_vivos.py
├── calculadora_roi.py
├── diagnostico_regional.py
├── noticias.py
├── requirements.txt
├── README.md
└── GUIA_PUBLICACAO.md
```

---

## 🔧 Passo 2: Executar o Setup Script

### 2.1 Abrir PowerShell

1. Pressione `Win + R`
2. Digite `powershell`
3. Pressione Enter

### 2.2 Navegar para a Pasta

```powershell
cd C:\Users\seu-usuario\Documentos\cgnat-automation
```

### 2.3 Executar o Script

```powershell
.\SETUP_WINDOWS.bat
```

### 2.4 Preencher as Informações

O script pedirá:

```
Digite seu usuário GitHub: Wallacecampos2704
Digite seu email GitHub: seu-email@gmail.com
Digite seu Personal Access Token do GitHub: ghp_xxxxxxxxxxxxx
```

**Cole o token que você copiou antes!**

---

## ✅ Passo 3: Verificar se Funcionou

Após o script terminar, verifique:

1. Acesse: https://github.com/Wallacecampos2704/cgnat-automation
2. Você deve ver os arquivos lá

Se não vir, execute manualmente:

```powershell
cd C:\Users\seu-usuario\Documentos\cgnat-automation

git add .
git commit -m "Adicionar arquivos do CGNAT Dashboard"
git push origin main
```

---

## 🌐 Passo 4: Publicar no Streamlit Cloud

### 4.1 Criar Conta no Streamlit Cloud

1. Acesse: https://share.streamlit.io
2. Clique "Sign up"
3. Selecione "Sign up with GitHub"
4. Autorize o Streamlit

### 4.2 Deploy da Aplicação

1. Clique "New app"
2. Preencha:
   - **Repository**: `Wallacecampos2704/cgnat-automation`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Clique "Deploy!"

**Aguarde 2-3 minutos...**

### 4.3 Seu Dashboard Estará Em

```
https://wallacecampos2704-cgnat-automation.streamlit.app
```

---

## 📝 Passo 5: Testar Localmente (Opcional)

Se quiser testar antes de publicar:

### 5.1 Instalar Dependências

```powershell
cd C:\Users\seu-usuario\Documentos\cgnat-automation

pip install -r requirements.txt
```

### 5.2 Executar o App

```powershell
streamlit run app.py
```

Seu app abrirá em: `http://localhost:8501`

---

## 🔄 Passo 6: Atualizar o Dashboard

Sempre que você quer fazer mudanças:

### 6.1 Editar Arquivo

Edite qualquer arquivo (ex: `app.py`)

### 6.2 Fazer Commit

```powershell
cd C:\Users\seu-usuario\Documentos\cgnat-automation

git add .
git commit -m "Descrição da mudança"
git push origin main
```

### 6.3 Deploy Automático

Streamlit Cloud fará deploy automaticamente em 1-2 minutos!

---

## 🐛 Troubleshooting

### Erro: "Git não está instalado"

**Solução:**
1. Baixe Git: https://git-scm.com/download/win
2. Execute o instalador
3. Reinicie o PowerShell
4. Tente novamente

### Erro: "Token inválido"

**Solução:**
1. Acesse: https://github.com/settings/tokens
2. Crie um novo token
3. Execute o script novamente com o novo token

### Erro: "Repositório já existe"

**Solução:**
1. Acesse: https://github.com/Wallacecampos2704/cgnat-automation
2. Clique em "Settings"
3. Clique em "Delete this repository"
4. Execute o script novamente

### Erro: "Python não encontrado"

**Solução:**
1. Baixe Python: https://www.python.org/downloads/
2. **Marque "Add Python to PATH"** durante instalação
3. Reinicie o PowerShell
4. Tente novamente

---

## ✨ Pronto!

Seu dashboard está no ar! 🎉

- 📊 Dashboard: https://wallacecampos2704-cgnat-automation.streamlit.app
- 📁 Código: https://github.com/Wallacecampos2704/cgnat-automation
- 📝 Documentação: GUIA_PUBLICACAO.md

---

## 📞 Próximos Passos

1. Compartilhe o link com seus clientes
2. Customize cores conforme sua marca
3. Adicione autenticação (opcional)
4. Integre com seu CRM

**Sucesso! 🚀**
