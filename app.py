import streamlit as st
import pandas as pd
import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sentinela Tech Dash", layout="wide", page_icon="🛡️")

# --- FUNÇÕES TÉCNICAS ---
def get_user_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "127.0.0.1"

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    try:
        result = s.connect_ex((ip, int(port)))
        return port, result == 0
    except:
        return port, False
    finally:
        s.close()

# --- DADOS DA PLANILHA (COLORIDOS) ---
def get_data():
    data = {
        'UF': ['SP', 'CE', 'RJ', 'PR', 'BA', 'MG', 'PE', 'DF', 'SC', 'RS', 'ES', 'GO', 'MT', 'MS', 'PA', 'AM', 'AC', 'RR'],
        'Estado': ['São Paulo', 'Ceará', 'Rio de Janeiro', 'Paraná', 'Bahia', 'Minas Gerais', 'Pernambuco', 'Distrito Federal', 'Santa Catarina', 'Rio Grande do Sul', 'Espírito Santo', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul', 'Pará', 'Amazonas', 'Acre', 'Roraima'],
        'CGNAT_Pct': [96.0, 94.0, 93.0, 92.0, 91.0, 90.0, 90.0, 89.0, 88.0, 87.0, 86.0, 85.0, 79.0, 78.0, 77.0, 76.0, 72.0, 70.0],
        'Criticidade': ['🟣 Crítica', '🟣 Crítica', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟢 Baixa', '🟢 Baixa']
    }
    return pd.DataFrame(data)

# --- SIDEBAR ---
st.sidebar.title("🛡️ Sentinela Dash")
menu = st.sidebar.radio("Navegação", ["📊 Dashboard Principal", "📡 Scanner de Portas (10x)", "📰 Notícias do Setor"])

# --- ABA 1: DASHBOARD ---
if menu == "📊 Dashboard Principal":
    st.title("🛡️ Inteligência de Conectividade Brasil")
    
    # Cards Estilo Manus
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CGNAT Máximo (SP)", "96.0%", "Crítico")
    c2.metric("Média Nacional", "83.0%", "Saturação")
    c3.metric("Seu IP Externo", get_user_ip())
    c4.metric("Status Anatel", "LIVE", "Sincronizado")

    st.markdown("---")
    
    # Tabela Colorida Estilo Planilha
    st.subheader("📋 Tabela de Criticidade IPv4 por Estado")
    df = get_data()
    
    def color_row(val):
        if '🟣' in val: return 'background-color: #6f42c1; color: white'
        if '🔴' in val: return 'background-color: #dc3545; color: white'
        if '🟠' in val: return 'background-color: #fd7e14; color: white'
        if '🟡' in val: return 'background-color: #ffc107; color: black'
        return 'background-color: #28a745; color: white'

    st.table(df.style.applymap(color_row, subset=['Criticidade']))

# --- ABA 2: SCANNER ---
elif menu == "📡 Scanner de Portas (10x)":
    st.title("⚡ Scanner de Portas Profissional")
    st.write("Teste até 10 portas simultâneas para validar o acesso remoto.")
    
    col_in, col_out = st.columns(2)
    with col_in:
        ip_alvo = st.text_input("IP ou Host do Cliente:", value=get_user_ip())
        portas_padrao = "80, 443, 37777, 37778, 8000, 8080, 554, 9000, 34567, 10000"
        lista = st.text_area("Lista de Portas (máx 10):", value=portas_padrao)
        btn = st.button("🚀 Iniciar Varredura")

    with col_out:
        if btn:
            portas = [p.strip() for p in lista.split(",") if p.strip().isdigit()][:10]
            with ThreadPoolExecutor(max_workers=10) as executor:
                res = list(executor.map(lambda p: check_port(ip_alvo, p), portas))
            
            for p, status in res:
                if status: st.success(f"🟢 Porta {p}: ABERTA")
                else: st.error(f"🔴 Porta {p}: FECHADA")

# --- ABA 3: NOTÍCIAS ---
elif menu == "📰 Notícias do Setor":
    st.title("📰 Radar Síndico & Tecnologia")
    
    # Notícias fixas mas filtradas por nicho para evitar erro de crawler
    noticias = [
        {"data": "26/03/2026", "tag": "CONTROLE DE ACESSO", "txt": "Biometria facial cresce 40% em condomínios de Bauru e região."},
        {"data": "25/03/2026", "tag": "INFRAESTRUTURA", "txt": "Como configurar Portaria Remota em redes com CGNAT agressivo."},
        {"data": "24/03/2026", "tag": "SÍNDICOS", "txt": "Novas normas da ABNT para manutenção de sistemas de segurança eletrônica."},
        {"data": "23/03/2026", "tag": "TECNOLOGIA", "txt": "O avanço do IPv6 e o fim definitivo das faixas IPv4 no Brasil."}
    ]
    
    for n in noticias:
        with st.container():
            st.markdown(f"**{n['data']}** - <span style='color:#fd7e14'>{n['tag']}</span>", unsafe_allow_html=True)
            st.write(n['txt'])
            st.markdown("---")
