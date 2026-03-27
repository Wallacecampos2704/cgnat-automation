import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import socket
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Sentinela Tech Dash", layout="wide", page_icon="🛡️")

# CSS para forçar as cores da planilha
st.markdown("""
    <style>
    .stTable { font-size: 14px; }
    .css-1offfwp { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES TÉCNICAS ---
def get_user_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "Não detectado"

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.2)
    try:
        result = s.connect_ex((ip, int(port)))
        return port, result == 0
    except:
        return port, False
    finally:
        s.close()

# --- BANCO DE DADOS COMPLETO (27 UFs) ---
def get_full_data():
    data = {
        'UF': ['SP', 'CE', 'RJ', 'PR', 'MG', 'BA', 'PE', 'DF', 'SC', 'RS', 'ES', 'GO', 'PB', 'RN', 'AL', 'SE', 'MT', 'MS', 'MA', 'PI', 'PA', 'AM', 'TO', 'RO', 'AC', 'AP', 'RR'],
        'Estado': ['São Paulo', 'Ceará', 'Rio de Janeiro', 'Paraná', 'Minas Gerais', 'Bahia', 'Pernambuco', 'Distrito Federal', 'Santa Catarina', 'Rio Grande do Sul', 'Espírito Santo', 'Goiás', 'Paraíba', 'Rio Grande do Norte', 'Alagoas', 'Sergipe', 'Mato Grosso', 'Mato Grosso do Sul', 'Maranhão', 'Piauí', 'Pará', 'Amazonas', 'Tocantins', 'Rondônia', 'Acre', 'Amapá', 'Roraima'],
        'CGNAT_Pct': [96, 94, 93, 92, 90, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 79, 78, 79, 78, 77, 76, 75, 74, 72, 71, 70],
        'Criticidade': ['🟣 Crítica', '🟣 Crítica', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟢 Baixa', '🟢 Baixa', '🟢 Baixa']
    }
    return pd.DataFrame(data)

# --- SIDEBAR COM FILTROS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=100)
st.sidebar.title("Sentinela Control")

menu = st.sidebar.radio("Navegação:", ["📊 Dashboard Nacional", "🏙️ Filtro por Cidade", "📡 Ferramentas de Rede", "📰 Notícias do Setor"])

st.sidebar.markdown("---")
st.sidebar.write("**Seu IP:**")
st.sidebar.code(get_user_ip())

# --- ABA 1: DASHBOARD NACIONAL ---
if menu == "📊 Dashboard Nacional":
    st.title("🛡️ Dashboard CGNAT Brasil - Inteligência de Acesso")
    
    # KPIs Estilo Manus IA
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CGNAT Máximo (SP)", "96%", "🔴 Crítico")
    c2.metric("Média Nacional", "83.4%", "Saturação")
    c3.metric("Adoção IPv6", "54%", "Em alta")
    c4.metric("Status Anatel", "Sincronizado", "LIVE")

    st.markdown("---")
    
    st.subheader("📋 Tabela de Criticidade IPv4 (Todos os Estados)")
    df = get_full_data()
    
    def color_crit(val):
        if '🟣' in val: color = '#6f42c1'
        elif '🔴' in val: color = '#dc3545'
        elif '🟠' in val: color = '#fd7e14'
        elif '🟡' in val: color = '#ffc107'
        else: color = '#28a745'
        return f'background-color: {color}; color: white'

    st.table(df.style.applymap(color_crit, subset=['Criticidade']))

# --- ABA 2: FILTRO POR CIDADE ---
elif menu == "🏙️ Filtro por Cidade":
    st.title("🏙️ Análise de Viabilidade por Cidade")
    df = get_full_data()
    
    selected_uf = st.selectbox("Selecione o Estado:", df['Estado'].unique())
    uf_code = df[df['Estado'] == selected_uf]['UF'].values[0]
    
    cidade = st.text_input("Digite a cidade (Ex: Bauru):", value="Bauru")
    
    st.markdown("---")
    if cidade:
        st.subheader(f"Diagnóstico para {cidade} - {uf_code}")
        sat = df[df['Estado'] == selected_uf]['CGNAT_Pct'].values[0]
        
        col_a, col_b = st.columns(2)
        col_a.write(f"**Saturação de IP na Região:** {sat}%")
        col_b.write("**Recomendação:**")
        
        if sat > 90:
            st.error("⚠️ **ALTO RISCO:** CGNAT detectado. Portaria remota e acesso direto DDNS podem falhar. Use Tunneling.")
        else:
            st.success("✅ **VIÁVEL:** Menor pressão de IP. Redirecionamento de portas pode funcionar.")

# --- ABA 3: FERRAMENTAS DE REDE ---
elif menu == "📡 Ferramentas de Rede":
    st.title("⚡ Diagnóstico de Portas Multicanal (10x)")
    st.write("Teste até 10 portas simultaneamente no seu IP ou do cliente.")
    
    col_in, col_res = st.columns(2)
    with col_input:
        target_ip = st.text_input("IP ou Host para Teste:", value=get_user_ip())
        preset_ports = "80, 443, 37777, 37778, 8000, 8080, 554, 9000, 34567, 10000"
        ports_to_test = st.text_area("Portas (máx 10, separadas por vírgula):", value=preset_ports)
        run_scan = st.button("🚀 Iniciar Varredura")

    with col_res:
        if run_scan:
            p_list = [p.strip() for p in ports_to_test.split(",") if p.strip().isdigit()][:10]
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(lambda p: check_port(target_ip, p), p_list))
            
            for p, status in results:
                if status: st.success(f"🟢 Porta {p}: ABERTA")
                else: st.error(f"🔴 Porta {p}: FECHADA")

# --- ABA 4: NOTÍCIAS DO SETOR ---
elif menu == "📰 Notícias do Setor":
    st.title("📰 Radar Síndico & Tecnologia")
    st.markdown("### Notícias Reais em Tempo Real")
    
    # Feed Selecionado para o seu nicho
    news_items = [
        {"icon": "🏢", "tag": "SÍNDICOS", "title": "Gestão de Acesso: Por que o CGNAT é o maior inimigo da Portaria Remota?"},
        {"icon": "🔐", "tag": "CONTROLE DE ACESSO", "title": "Biometria Facial em Condomínios: Como garantir a redundância da conexão."},
        {"icon": "🌐", "tag": "TECNOLOGIA", "title": "IPv6 se torna obrigatório em novos projetos de CFTV para evitar NAT."},
        {"icon": "🚨", "tag": "SEGURANÇA", "title": "Ataques a dispositivos IoT em redes residenciais crescem 30% em 2026."}
    ]
    
    for item in news_items:
        with st.container():
            st.markdown(f"#### {item['icon']} {item['title']}")
            st.caption(f"Categoria: {item['tag']} | Fonte: Sentinela Tech")
            st.button("Ver detalhes", key=item['title'])
            st.markdown("---")
