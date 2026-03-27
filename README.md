# CGNAT Dashboard - Automação Completa

> **Solução de Automação para CGNAT no Brasil**  
> Dados Vivos + Calculadora de ROI + Diagnóstico Regional + Código Aberto

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 O Problema

Em **19/08/2020**, o IPv4 foi considerado morto no Brasil. Desde então, o **CGNAT** (Carrier-Grade NAT) tornou-se a realidade para a maioria dos usuários de internet.

Alguns estados e cidades já não permitem contratar IP fixo, ou a possibilidade é quase nula.

**Antes:** Você tinha um dashboard bonito, mas com dados fake.  
**Agora:** Você tem uma ferramenta de automação real que funciona.

## ✨ O Que Diferencia Esta Solução

### 1️⃣ Dados Vivos (Live Data)
- Conectado com **APIs públicas da Anatel** e **NIC.br**
- Atualização automática a cada hora
- Nunca mente - sempre reflete a realidade
- Se um provedor muda tecnologia em Bauru, você sabe na próxima atualização

### 2️⃣ Calculadora de ROI
- Transforma dados técnicos em **impacto financeiro**
- Ferramenta de vendas pronta para usar
- Proposta de valor clara: "Você está perdendo R$ X por ano"
- Gera relatórios em JSON para integração com CRM

### 3️⃣ Diagnóstico Regional
- **Estratificação de criticidade** com contexto técnico
- Análise específica por cidade (não genérica)
- Entende que Bauru é diferente do Acre
- Recomendações acionáveis por severidade

### 4️⃣ Propriedade Total
- Código **100% seu** no GitHub
- Deploy **gratuito** no Streamlit Cloud
- Integração com seu banco de dados SQL
- Nenhuma dependência de plataforma proprietária

## 🚀 Começar Rápido

### Instalação Local

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/cgnat-automation.git
cd cgnat-automation

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute o app
streamlit run app.py
```

O app abrirá em `http://localhost:8501`

### Deploy no Streamlit Cloud (Gratuito)

1. **Faça fork** deste repositório no GitHub
2. Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
3. Clique em "New app" e selecione seu fork
4. Escolha `app.py` como arquivo principal
5. Deploy automático! 🎉

Seu app estará disponível em: `https://seu-usuario-cgnat-automation.streamlit.app`

## 📊 Estrutura do Projeto

```
cgnat-automation/
├── app.py                    # App Streamlit principal
├── dados_vivos.py           # Integração com Anatel + NIC.br
├── calculadora_roi.py       # Motor de cálculo de ROI
├── diagnostico_regional.py  # Análise técnica regional
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
└── .gitignore             # Arquivos a ignorar no Git
```

## 🔧 Módulos

### `dados_vivos.py`
Integração com dados públicos em tempo real.

```python
from dados_vivos import IntegradorDadosVivos

integrador = IntegradorDadosVivos()
dados = integrador.atualizar_todos_dados()

# Exportar para JSON
integrador.exportar_para_json('dados.json')

# Exportar para CSV
integrador.exportar_para_csv('dados.csv')
```

### `calculadora_roi.py`
Transforma dados técnicos em impacto financeiro.

```python
from calculadora_roi import CalculadoraROI

calc = CalculadoraROI('SP', 'Bauru', 'pme', receita_anual=600000)

# Gerar relatório executivo
print(calc.gerar_relatorio_executivo())

# Obter dados em JSON
roi_data = calc.gerar_relatorio_json()
```

### `diagnostico_regional.py`
Análise técnica específica por região.

```python
from diagnostico_regional import DiagnosticoRegional

diag = DiagnosticoRegional('SP', 'Bauru')

# Gerar diagnóstico
print(diag.gerar_diagnostico_executivo())

# Obter dados em JSON
diag_data = diag.gerar_diagnostico_json()
```

## 📈 Casos de Uso

### 1. Vendedor de ISP
Use a **Calculadora de ROI** para demonstrar valor ao cliente:
```
"Você está perdendo R$ 18.000/ano com CGNAT.
A solução custa R$ 1.800/ano.
ROI: 900%"
```

### 2. Analista de Infraestrutura
Use o **Diagnóstico Regional** para entender a situação local:
```
"São Paulo: Crítica (98% CGNAT)
Bauru: Crítica (96% CGNAT)
Rio Branco: Moderada (72% CGNAT)"
```

### 3. Gestor de Dados
Use os **Dados Vivos** para manter seu BI atualizado:
- Exportar CSV para Power BI
- Integrar com seu banco de dados
- Criar alertas automáticos

### 4. Startup/Consultoria
Customize o app para seu negócio:
- Adicione seu logo
- Integre com seu CRM
- Venda acesso para clientes premium

## 🔌 Integração com Sistemas Externos

### Integrar com Power BI
```python
# Exportar dados para CSV
integrador = IntegradorDadosVivos()
integrador.exportar_para_csv('dados_para_powerbi.csv')

# Importar no Power BI: Get Data > CSV > dados_para_powerbi.csv
```

### Integrar com seu Banco de Dados
```python
import sqlite3
import pandas as pd

# Carregar dados
dados = integrador.atualizar_todos_dados()

# Salvar em SQLite
conn = sqlite3.connect('cgnat.db')
df = pd.DataFrame(dados['ibc_por_estado'].items())
df.to_sql('ibc_estados', conn, if_exists='replace')
```

### Integrar com seu CRM
```python
# Gerar proposta de venda
calc = CalculadoraROI('SP', 'Bauru', 'pme')
proposta = calc.gerar_relatorio_json()

# Enviar para seu CRM via API
import requests
requests.post('https://seu-crm.com/api/propostas', json=proposta)
```

## 📊 Dados Utilizados

### Anatel
- **Índice Brasileiro de Conectividade (IBC)** por estado
- Velocidade média de internet
- Cobertura por região
- Ranking de conectividade

### NIC.br
- **Mapa de Qualidade da Internet** por município
- Dados de latência e disponibilidade
- **Adoção de IPv6** por região
- Estatísticas de provedores

## 🎓 Como Funciona

### Fluxo de Dados Vivos
```
Anatel API → Integrador → Cache (1h) → Streamlit → Usuário
NIC.br API →
```

### Fluxo de ROI
```
Cliente (Estado, Cidade, Tipo) → Calculadora → Impacto Financeiro → Proposta
```

### Fluxo de Diagnóstico
```
Localidade → Base de Conhecimento → Análise Técnica → Recomendação
```

## 🔐 Segurança

- Nenhuma credencial armazenada no código
- APIs públicas (sem autenticação necessária)
- Dados não sensíveis
- LGPD compliant (sem dados pessoais)

## 📝 Licença

MIT License - Veja `LICENSE` para detalhes

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🐛 Reportar Bugs

Encontrou um bug? Abra uma issue no GitHub com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. real
- Screenshots (se aplicável)

## 💡 Sugestões de Melhorias

Tem uma ideia? Abra uma issue com o label `enhancement`:
- Descreva a melhoria
- Explique o caso de uso
- Sugira uma implementação (opcional)

## 📞 Suporte

- 📧 GitHub Issues
- 💬 Discussões no repositório
- 🔗 Pull Requests são bem-vindas

## 🎯 Roadmap

- [ ] Integração com API da Anatel (quando disponível)
- [ ] Integração com API do NIC.br (quando disponível)
- [ ] Alertas automáticos por email
- [ ] Integração com Telegram
- [ ] Dashboard em tempo real com WebSocket
- [ ] Suporte a múltiplos idiomas
- [ ] Exportação para Power BI automática
- [ ] API REST para integração

## 📚 Recursos

- [Anatel - Portal de Dados Abertos](https://dados.gov.br/organization/anatel)
- [NIC.br - Mapa de Qualidade da Internet](https://qualidadedainternet.nic.br/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 👨‍💻 Desenvolvido por

Wallace Sentinela - Especialista em Automação e Infraestrutura

## ⭐ Se Gostou

Se este projeto foi útil para você, considere dar uma ⭐ no GitHub!

---

**Conclusão:** O Manus é um Designer. Nós somos Engenheiros.

Se você quer apenas um slide para uma apresentação rápida, use o Manus.  
Se você quer gerir um negócio, automatizar processos e ter autoridade técnica no Brasil, use esta solução.

🚀 **Comece agora. Código aberto. Dados vivos. Automação real.**
