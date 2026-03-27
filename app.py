import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import socket
from bs4 import BeautifulSoup

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sentinela Tech Dash", layout="wide", page_icon="🛡️")

# --- ESTILO CSS PARA CORES DA PLANILHA ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .badge-critica { background-color: #6f42c1; color: white; padding: 4px 8px; border-radius: 4px; }
    .badge-muitoalta { background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; }
    .badge-alta { background-color: #fd7e14; color: white; padding: 4px 8px; border-radius: 4px; }
    </style>
    """, unsafe_base_code=True)

# --- FUNÇÕES TÉCNICAS (REDES) ---
def get_user_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Não foi possível detectar"

def test_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, int(port)))
        return True
    except:
        return False
    finally:
        s.close()

# --- CARREGAMENTO DE DADOS (PLANILHA ATUALIZADA) ---
@st.cache_data(ttl=3600)
def load_data():
    # Aqui os dados são dinâmicos simulando base Anatel/NIC.br
    data = {
        'UF': ['SP', 'CE', 'RJ', 'PR', 'BA', 'MG', 'PE', 'DF'],
        'Estado': ['São Paulo', 'Ceará', 'Rio de Janeiro', 'Paraná', 'Bahia', 'Minas Gerais', 'Pernambuco', 'Distrito Federal'],
        'CGNAT_Est': [96.0, 94.0, 93.0, 92.0, 91.0, 90.0, 90.0, 89.0],
        'Criticidade': ['Crítica', 'Crítica', 'Muito Alta', 'Muito Alta', 'Muito Alta', 'Muito Alta', 'Muito Alta', 'Alta']
    }
    return pd.DataFrame(data)

# --- SIDEBAR (FILTROS) ---
st.sidebar.title("🔍 Filtros & Ferramentas")
aba = st.sidebar.radio("Navegar para:", ["📊 Painel de Controle", "📡 Ferramentas de Rede", "📰 Notícias Tech/Síndico"])

# --- CONTEÚDO PRINCIPAL ---
if aba == "📊 Painel de Controle":
    st.title("🛡️ Dashboard CGNAT Brasil - Inteligência de Acesso")
    
    # KPIs Estilo Manus IA (Melhorado)
    c1, c2, c3 = st.columns(3)
    c1.metric("CGNAT Máximo (SP)", "96.0%", delta="Estado Crítico", delta_color="inverse")
    c2.metric("Média Nacional", "83.0%", "Estável")
    c3.metric("Seu IP Atual", get_user_ip())

    st.markdown("---")
    
    # Tabela Colorida (Igual à sua planilha)
    st.subheader("📋 Mapa de Saturação por Estado")
    df = load_data()
    
    def color_criticidade(val):
        color = '#6f42c1' if val == 'Crítica' else '#dc3545' if val == 'Muito Alta' else '#fd7e14'
        return f'background-color: {color}; color: white'

    st.table(df.style.applymap(color_criticidade, subset=['Criticidade']))
    
    # Filtro por Cidade (Exemplo Bauru)
    st.markdown("### 🏙️ Consulta por Cidade")
    cidade = st.selectbox("Selecione a cidade para análise de viabilidade:", ["Bauru", "São Paulo", "Rio de Janeiro", "Curitiba"])
    if cidade == "Bauru":
        st.warning(f"⚠️ **{cidade}:** Incidência de 94.5% de CGNAT. Acesso direto P2P/DDNS com alto risco de falha.")

elif aba == "📡 Ferramentas de Rede":
    st.title("⚡ Scanner de Portas & Diagnóstico")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**Seu IP Externo:** {get_user_ip()}")
        st.write("Se este IP for diferente do IP que aparece no seu roteador, você está em **CGNAT**.")
    
    with col_b:
        ip_teste = st.text_input("IP para teste (Ex: Seu IP Externo):", value=get_user_ip())
        porta_teste = st.text_input("Porta (Ex: 80, 8080, 37777):", value="80")
        if st.button("Testar Porta"):
            with st.spinner("Escaneando..."):
                resultado = test_port(ip_teste, porta_teste)
                if resultado:
                    st.success(f"✅ Porta {porta_teste} está ABERTA em {ip_teste}")
                else:
                    st.error(f"❌ Porta {porta_teste} está FECHADA ou Filtrada.")

elif aba == "📰 Notícias Tech/Síndico":
    st.title("📰 Radar de Tecnologia para Condomínios")
    st.caption("Notícias em tempo real focadas em Segurança, Síndicos e Tecnologia.")
    
    # Simulação de Feed focado (Você pode conectar com RSS real aqui)
    noticias = [
        {"titulo": "Novas tecnologias de biometria facial para condomínios em 2026", "tag": "Controle de Acesso"},
        {"titulo": "Como o fim do IPv4 impacta a segurança das câmeras IP", "tag": "Infraestrutura"},
        {"titulo": "Dicas para Síndicos: Como gerir a portaria remota em zonas de CGNAT", "tag": "Gestão"},
        {"titulo": "Anatel anuncia novas metas de expansão do IPv6 no Brasil", "tag": "Telecom"}
    ]
    
    for n in noticias:
        with st.expander(f"[{n['tag']}] {n['titulo']}"):
            st.write("As novas regulamentações e o avanço da fibra óptica exigem que profissionais de segurança dominem o tunelamento...")
            st.button("Ler notícia completa", key=n['titulo'])
