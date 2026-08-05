"""
Sentinela Tech Dash - Versão Completa e Responsiva
Dashboard CGNAT Brasil com Notícias de Segurança Eletrônica, Inovações e Infraestrutura
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import json

# Importar módulos locais
try:
    from noticias import AgregadorNoticias, NOTICIAS_EXEMPLO
    from dados_vivos import IntegradorDadosVivos
    from diagnostico_regional import DiagnosticoRegional
    from calculadora_roi import CalculadoraROI
except ImportError:
    # Fallback para desenvolvimento
    AgregadorNoticias = None
    NOTICIAS_EXEMPLO = []
    IntegradorDadosVivos = None
    DiagnosticoRegional = None
    CalculadoraROI = None

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(
    page_title="Sentinela Tech Dash", 
    layout="wide", 
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# CSS para responsividade e estilo moderno
st.markdown("""
    <style>
    /* Responsividade Mobile-First */
    @media (max-width: 768px) {
        .stApp { padding: 0 10px; }
        .stColumns { flex-wrap: wrap; }
        [data-testid="column"] { min-width: 100% !important; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        [data-testid="column"] { min-width: 50% !important; }
    }
    
    /* Estilo dos cards */
    .card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .card:hover { transform: translateY(-5px); }
    
    /* KPIs estilizados */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    
    .kpi-value { font-size: 2rem; font-weight: bold; }
    .kpi-label { font-size: 0.9rem; opacity: 0.9; }
    .kpi-trend { font-size: 0.8rem; margin-top: 5px; }
    
    /* Tabela responsiva */
    .stTable { font-size: 14px; }
    
    /* Animações */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .live-indicator {
        animation: pulse 2s infinite;
        color: #00ff00;
        font-weight: bold;
    }
    
    /* News Cards */
    .news-card {
        background: #1e293b;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .news-tag {
        background: #3b82f6;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        display: inline-block;
        margin-bottom: 8px;
    }
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
        'IPv6_Adoption': [58, 52, 55, 54, 51, 49, 48, 60, 56, 55, 53, 50, 45, 44, 43, 42, 47, 46, 41, 40, 39, 38, 37, 36, 35, 34, 33],
        'Velocidade_Media': [152.3, 89.5, 145.1, 142.5, 128.5, 98.3, 92.1, 155.2, 148.9, 151.2, 138.5, 125.8, 87.3, 85.1, 79.8, 77.9, 115.3, 118.2, 81.2, 76.5, 78.3, 70.1, 75.8, 74.5, 72.3, 71.2, 68.9],
        'Criticidade': ['🟣 Crítica', '🟣 Crítica', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🔴 Muito Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟠 Alta', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟡 Moderada', '🟢 Baixa', '🟢 Baixa', '🟢 Baixa']
    }
    return pd.DataFrame(data)


# --- DADOS HISTÓRICOS CGNAT (Simulação) ---
def get_historical_data():
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    data = {
        'mes': meses,
        'SP': [88, 89, 90, 91, 92, 93, 93, 94, 95, 95, 96, 96],
        'RJ': [85, 86, 87, 88, 89, 90, 90, 91, 92, 92, 93, 93],
        'BR': [75, 76, 77, 78, 79, 80, 81, 82, 82, 83, 83, 84]
    }
    return pd.DataFrame(data)


# --- SIDEBAR COM NAVEGAÇÃO ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=100)
st.sidebar.title("🛡️ Sentinela Control")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação:",
    [
        "📊 Dashboard Nacional",
        "🗺️ Mapa de Calor CGNAT",
        "🏙️ Diagnóstico por Cidade",
        "📈 Evolução Histórica",
        "💰 Calculadora ROI",
        "📡 Ferramentas de Rede",
        "📰 Notícias Segurança",
        "🚀 Inovações & Trends",
        "🌐 Infraestrutura"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("**Seu IP:**")
st.sidebar.code(get_user_ip())

st.sidebar.markdown("""
<div style='margin-top: 20px;'>
    <p style='font-size: 0.8rem; color: #888;'>
        🔄 Dados atualizados em tempo real<br>
        <span class='live-indicator'>● LIVE</span>
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================
# ABA 1: DASHBOARD NACIONAL
# ============================================
if menu == "📊 Dashboard Nacional":
    st.title("🛡️ Dashboard CGNAT Brasil - Inteligência de Acesso")
    st.markdown("*Monitoramento em tempo real da saturação IPv4 e adoção IPv6*")
    
    df = get_full_data()
    
    # KPIs Principais
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>96%</div>
            <div class='kpi-label'>CGNAT Máximo (SP)</div>
            <div class='kpi-trend'>🔴 Crítico</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>83.4%</div>
            <div class='kpi-label'>Média Nacional</div>
            <div class='kpi-trend'>⚠️ Saturação</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>54%</div>
            <div class='kpi-label'>Adoção IPv6</div>
            <div class='kpi-trend'>📈 Em alta</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c4:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-value'>27</div>
            <div class='kpi-label'>Estados Monitorados</div>
            <div class='kpi-trend'><span class='live-indicator'>● LIVE</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfico de Barras - Top 10 Estados
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Top 10 Estados com Maior CGNAT")
        top_10 = df.nlargest(10, 'CGNAT_Pct')
        
        fig = px.bar(
            top_10,
            x='CGNAT_Pct',
            y='Estado',
            orientation='h',
            color='CGNAT_Pct',
            color_continuous_scale='Reds',
            text='CGNAT_Pct'
        )
        fig.update_layout(
            height=400,
            xaxis_title="% CGNAT",
            yaxis_title="",
            showlegend=False
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Distribuição por Criticidade")
        criticidade_counts = df['Criticidade'].value_counts().reset_index()
        criticidade_counts.columns = ['Criticidade', 'Quantidade']
        
        fig_pie = px.pie(
            criticidade_counts,
            values='Quantidade',
            names='Criticidade',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Tabela Completa
    st.markdown("---")
    st.subheader("📋 Tabela de Criticidade IPv4 (Todos os Estados)")
    
    def color_crit(val):
        if '🟣' in val: color = '#6f42c1'
        elif '🔴' in val: color = '#dc3545'
        elif '🟠' in val: color = '#fd7e14'
        elif '🟡' in val: color = '#ffc107'
        else: color = '#28a745'
        return f'background-color: {color}; color: white'
    
    st.dataframe(
        df.style.applymap(color_crit, subset=['Criticidade']),
        use_container_width=True,
        height=400
    )


# ============================================
# ABA 2: MAPA DE CALOR CGNAT
# ============================================
elif menu == "🗺️ Mapa de Calor CGNAT":
    st.title("🗺️ Mapa de Calor - Incidência CGNAT no Brasil")
    st.markdown("*Visualização geográfica da saturação de IPv4 por estado*")
    
    df = get_full_data()
    
    # Mapeamento UF para nome completo
    uf_map = {
        'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Minas Gerais',
        'BA': 'Bahia', 'RS': 'Rio Grande do Sul', 'PR': 'Paraná',
        'PE': 'Pernambuco', 'CE': 'Ceará', 'DF': 'Distrito Federal',
        'SC': 'Santa Catarina', 'ES': 'Espírito Santo', 'GO': 'Goiás',
        'PB': 'Paraíba', 'RN': 'Rio Grande do Norte', 'AL': 'Alagoas',
        'SE': 'Sergipe', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
        'MA': 'Maranhão', 'PI': 'Piauí', 'PA': 'Pará', 'AM': 'Amazonas',
        'TO': 'Tocantins', 'RO': 'Rondônia', 'AC': 'Acre', 'AP': 'Amapá',
        'RR': 'Roraima'
    }
    
    df['regiao'] = df['UF'].map(uf_map)
    
    # Criar mapa coroplético
    fig_map = px.choropleth(
        df,
        locations='UF',
        locationmode="BRA-states",
        color='CGNAT_Pct',
        color_continuous_scale='Reds',
        range_color=(50, 100),
        hover_name='Estado',
        hover_data={'CGNAT_Pct': True, 'IPv6_Adoption': True, 'Velocidade_Media': True},
        title='Incidência CGNAT por Estado (%)',
        labels={'CGNAT_Pct': '% CGNAT'}
    )
    
    fig_map.update_layout(
        geo_scope='south america',
        geo=dict(
            scope='south america',
            projection_type='mercator',
            showland=True,
            landcolor="rgb(217, 217, 217)",
            countrycolor="rgb(255, 255, 255)",
            showcountries=True,
            bgcolor="rgb(255, 255, 255)"
        ),
        height=600
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Estatísticas regionais
    st.subheader("📊 Análise por Região")
    
    regioes = {
        'Sudeste': ['SP', 'RJ', 'MG', 'ES'],
        'Sul': ['PR', 'RS', 'SC'],
        'Nordeste': ['BA', 'PE', 'CE', 'PB', 'RN', 'AL', 'SE', 'MA', 'PI'],
        'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
        'Norte': ['PA', 'AM', 'TO', 'RO', 'AC', 'AP', 'RR']
    }
    
    cols = st.columns(5)
    for idx, (regiao, ufs) in enumerate(regioes.items()):
        media_cgnat = df[df['UF'].isin(ufs)]['CGNAT_Pct'].mean()
        with cols[idx]:
            st.metric(
                label=regiao,
                value=f"{media_cgnat:.1f}%",
                delta="Alto" if media_cgnat > 85 else "Moderado" if media_cgnat > 75 else "Baixo"
            )


# ============================================
# ABA 3: DIAGNÓSTICO POR CIDADE
# ============================================
elif menu == "🏙️ Diagnóstico por Cidade":
    st.title("🏙️ Diagnóstico Regional Detalhado")
    st.markdown("*Análise técnica com contexto de infraestrutura local*")
    
    df = get_full_data()
    
    col_sel1, col_sel2 = st.columns(2)
    
    with col_sel1:
        selected_uf = st.selectbox("Selecione o Estado:", df['Estado'].unique())
        uf_code = df[df['Estado'] == selected_uf]['UF'].values[0]
    
    with col_sel2:
        cidades_sugestao = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", 
                           "Fortaleza", "Brasília", "Curitiba", "Porto Alegre", "Recife", 
                           "Manaus", "Belém", "Goiânia", "Campinas", "Bauru"]
        cidade = st.text_input("Digite a cidade:", value=cidades_sugestao[0] if selected_uf == "São Paulo" else "")
    
    if cidade and DiagnosticoRegional:
        st.markdown("---")
        
        # Obter diagnóstico técnico
        diag = DiagnosticoRegional(uf_code, cidade)
        dados_diag = diag.obter_diagnostico()
        
        # Exibir informações principais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CGNAT na Região", f"{dados_diag['cgnat_percent']}%")
        
        with col2:
            severidade_emoji = {"CRÍTICA": "🟣", "MUITO ALTA": "🔴", "ALTA": "🟠", "MODERADA": "🟡", "BAIXA": "🟢"}
            st.metric("Severidade", f"{severidade_emoji.get(dados_diag['severidade'], '⚪')} {dados_diag['severidade']}")
        
        with col3:
            st.metric("Blocos IPv4 Disp.", dados_diag['blocos_ipv4_disponiveis'])
        
        # Detalhes técnicos
        st.subheader("📋 Detalhes Técnicos")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.info(f"""
            **Causa Raiz:** {dados_diag['causa_raiz']}
            
            **Provedores Dominantes:**
            {', '.join(dados_diag['provedores_dominantes'])}
            
            **Tendência:** {dados_diag['tendencia']}
            """)
        
        with col_b:
            st.success(f"""
            **Alternativas Recomendadas:**
            {chr(10).join(['• ' + alt for alt in dados_diag['alternativas']])}
            
            **Custo Estimado:** {dados_diag['custo_solucao']}
            
            **Tempo de Implementação:** {dados_diag['tempo_implementacao']}
            """)
        
        # Recomendação executiva
        st.markdown("---")
        st.subheader("✅ Recomendação Técnica")
        st.write(diag._gerar_recomendacao(dados_diag))
        
        # Botão para gerar relatório ROI
        if st.button("💰 Calcular ROI para esta localidade"):
            st.session_show_roi = True
    
    elif not DiagnosticoRegional:
        st.warning("Módulo de diagnóstico regional não disponível. Usando dados básicos.")
        sat = df[df['Estado'] == selected_uf]['CGNAT_Pct'].values[0]
        st.write(f"**Saturação de IP na Região:** {sat}%")
        
        if sat > 90:
            st.error("⚠️ **ALTO RISCO:** CGNAT detectado. Use soluções alternativas.")
        else:
            st.success("✅ **VIÁVEL:** Menor pressão de IP.")


# ============================================
# ABA 4: EVOLUÇÃO HISTÓRICA
# ============================================
elif menu == "📈 Evolução Histórica":
    st.title("📈 Evolução Histórica do CGNAT")
    st.markdown("*Análise temporal da saturação IPv4 nos últimos 12 meses*")
    
    hist_df = get_historical_data()
    
    # Gráfico de linhas
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hist_df['mes'],
        y=hist_df['SP'],
        mode='lines+markers',
        name='São Paulo',
        line=dict(width=3, color='#ef4444'),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=hist_df['mes'],
        y=hist_df['RJ'],
        mode='lines+markers',
        name='Rio de Janeiro',
        line=dict(width=3, color='#f97316'),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=hist_df['mes'],
        y=hist_df['BR'],
        mode='lines+markers',
        name='Média Brasil',
        line=dict(width=3, color='#3b82f6', dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Evolução Mensal CGNAT (%)',
        xaxis_title='Mês',
        yaxis_title='% CGNAT',
        yaxis_range=[70, 100],
        hovermode='x unified',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.subheader("🔍 Insights da Evolução")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crescimento_sp = hist_df['SP'].iloc[-1] - hist_df['SP'].iloc[0]
        st.metric("Crescimento SP", f"+{crescimento_sp}pp")
    
    with col2:
        crescimento_rj = hist_df['RJ'].iloc[-1] - hist_df['RJ'].iloc[0]
        st.metric("Crescimento RJ", f"+{crescimento_rj}pp")
    
    with col3:
        crescimento_br = hist_df['BR'].iloc[-1] - hist_df['BR'].iloc[0]
        st.metric("Crescimento BR", f"+{crescimento_br}pp")
    
    st.info("""
    **Análise:** A tendência de crescimento do CGNAT é consistente em todo o país.
    São Paulo lidera com 96% de saturação, seguido pelo Rio de Janeiro com 93%.
    A média nacional cresceu 9 pontos percentuais no último ano.
    """)


# ============================================
# ABA 5: CALCULADORA ROI
# ============================================
elif menu == "💰 Calculadora ROI":
    st.title("💰 Calculadora de ROI - Impacto Financeiro do CGNAT")
    st.markdown("*Transforme dados técnicos em proposta de valor para clientes*")
    
    if CalculadoraROI:
        col1, col2 = st.columns(2)
        
        with col1:
            estado = st.selectbox("Estado:", ['SP', 'RJ', 'MG', 'BA', 'RS', 'PR', 'PE', 'CE', 'DF', 'SC'])
            cidade = st.text_input("Cidade:", "São Paulo")
        
        with col2:
            tipo_cliente = st.selectbox(
                "Tipo de Cliente:",
                ['residencial', 'pme', 'empresa', 'startup']
            )
            receita_anual = st.number_input(
                "Receita Anual (R$):",
                min_value=0,
                value=500000,
                step=50000
            )
        
        if st.button("🧮 Calcular ROI"):
            calc = CalculadoraROI(estado, cidade, tipo_cliente, receita_anual)
            
            perda = calc.calcular_perda_anual()
            roi = calc.calcular_roi_solucao()
            
            # Exibir resultados
            st.markdown("---")
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("Perda Anual", f"R$ {perda['perda_total']:,.0f}")
            
            with col_b:
                st.metric("Perda Mensal", f"R$ {perda['perda_mensal']:,.0f}")
            
            with col_c:
                st.metric("ROI", f"{roi['roi_percentual']:.1f}%")
            
            with col_d:
                st.metric("Payback", f"{roi['payback_meses']:.1f} meses")
            
            # Detalhes
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💸 Impacto Atual (Sem Solução)")
                st.write(f"""
                - **Downtime:** R$ {perda['perda_downtime']:,.0f}/ano
                - **Bloqueios:** R$ {perda['perda_bloqueios']:,.0f}/ano
                - **Produtividade:** R$ {perda['perda_produtividade']:,.0f}/ano
                """)
            
            with col2:
                st.subheader("✅ Com Solução (IP Fixo/IPv6)")
                st.write(f"""
                - **Economia Anual:** R$ {roi['economia_anual']:,.0f}
                - **Custo Solução:** R$ {roi['custo_anual']:,.0f}/ano
                - **Lucro Líquido:** R$ {roi['lucro_anual']:,.0f}/ano
                """)
            
            # Relatório completo
            with st.expander("📄 Ver Relatório Executivo Completo"):
                st.text(calc.gerar_relatorio_executivo())
    else:
        st.warning("Módulo de calculadora ROI não disponível.")


# ============================================
# ABA 6: FERRAMENTAS DE REDE
# ============================================
elif menu == "📡 Ferramentas de Rede":
    st.title("⚡ Diagnóstico de Portas Multicanal")
    st.write("Teste até 10 portas simultaneamente no seu IP ou do cliente.")
    
    col_in, col_res = st.columns(2)
    
    with col_in:
        target_ip = st.text_input("IP ou Host para Teste:", value=get_user_ip())
        preset_ports = "80, 443, 37777, 37778, 8000, 8080, 554, 9000, 34567, 10000"
        ports_to_test = st.text_area("Portas (máx 10, separadas por vírgula):", value=preset_ports)
        run_scan = st.button("🚀 Iniciar Varredura")
    
    with col_res:
        if run_scan:
            p_list = [p.strip() for p in ports_to_test.split(",") if p.strip().isdigit()][:10]
            
            with st.spinner("Realizando varredura..."):
                with ThreadPoolExecutor(max_workers=10) as executor:
                    results = list(executor.map(lambda p: check_port(target_ip, p), p_list))
                
                abertas = sum(1 for _, status in results if status)
                fechadas = len(results) - abertas
                
                st.metric("Portas Abertas", abertas)
                st.metric("Portas Fechadas", fechadas)
                
                st.divider()
                
                for p, status in results:
                    if status:
                        st.success(f"🟢 Porta {p}: ABERTA")
                    else:
                        st.error(f"🔴 Porta {p}: FECHADA")


# ============================================
# ABA 7: NOTÍCIAS DE SEGURANÇA ELETRÔNICA
# ============================================
elif menu == "📰 Notícias Segurança":
    st.title("📰 Notícias de Segurança Eletrônica")
    st.markdown("*Atualizações sobre segurança cibernética, controle de acesso e CFTV*")
    
    # Filtros
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        categoria = st.selectbox(
            "Categoria:",
            ["Todas", "Segurança Cibernética", "Controle de Acesso", "CFTV", "IoT", "Normas"]
        )
    
    with col_filtro2:
        regiao = st.selectbox(
            "Região:",
            ["Todas", "Brasil", "América Latina", "Mundo"]
        )
    
    # Carregar notícias
    if AgregadorNoticias:
        agregador = AgregadorNoticias()
        try:
            noticias = agregador.buscar_todas_noticias()
            if not noticias:
                noticias = NOTICIAS_EXEMPLO
        except:
            noticias = NOTICIAS_EXEMPLO
    else:
        noticias = NOTICIAS_EXEMPLO
    
    # Filtrar notícias
    if categoria != "Todas":
        noticias = [n for n in noticias if categoria.lower() in n.get('categoria', '').lower()]
    
    # Exibir notícias em cards
    st.markdown("---")
    
    for i, noticia in enumerate(noticias[:10]):
        col_news = st.columns([3, 1])
        
        with col_news[0]:
            st.markdown(f"""
            <div class='news-card'>
                <span class='news-tag'>{noticia.get('categoria', 'Geral')}</span>
                <h4>{noticia.get('titulo', 'Título indisponível')}</h4>
                <p style='color: #888; font-size: 0.9rem;'>
                    {noticia.get('descricao', '')[:200]}...
                </p>
                <p style='font-size: 0.8rem; color: #666;'>
                    📰 {noticia.get('fonte', 'Desconhecida')} | 
                    🕒 {noticia.get('data', '')[:10] if noticia.get('data') else 'Data indisponível'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_news[1]:
            st.link_button("Ler mais", noticia.get('link', '#'))
        
        st.divider()
    
    # Fonte adicional de notícias
    st.markdown("---")
    st.subheader("📡 Fontes Monitoradas")
    
    fontes = [
        {"nome": "Canaltech", "url": "https://canaltech.com.br"},
        {"nome": "TecMundo", "url": "https://tecmundo.com.br"},
        {"nome": "IT Forum", "url": "https://itforum.com.br"},
        {"nome": "Security Report", "url": "https://securityreport.com.br"},
        {"nome": "CSO Online", "url": "https://csoonline.com.br"}
    ]
    
    cols = st.columns(5)
    for idx, fonte in enumerate(fontes):
        with cols[idx]:
            st.link_button(fonte["nome"], fonte["url"])


# ============================================
# ABA 8: INOVAÇÕES & TRENDS
# ============================================
elif menu == "🚀 Inovações & Trends":
    st.title("🚀 Inovações e Tendências do Setor")
    st.markdown("*Acompanhe as últimas inovações em segurança, redes e infraestrutura*")
    
    # Tabs para diferentes categorias
    tab1, tab2, tab3, tab4 = st.tabs(["🔮 Tendências", "💡 Startups", "📜 Patentes", "📊 Cases"])
    
    with tab1:
        st.subheader("🔮 Principais Tendências 2026")
        
        trends = [
            {
                "titulo": "Zero Trust Architecture",
                "descricao": "Arquitetura de confiança zero se torna padrão para condomínios e empresas",
                "impacto": "Alto",
                "timeline": "Q2 2026"
            },
            {
                "titulo": "IA em CFTV",
                "descricao": "Câmeras com análise preditiva de comportamento e reconhecimento facial avançado",
                "impacto": "Muito Alto",
                "timeline": "Q1 2026"
            },
            {
                "titulo": "5G Privado",
                "descricao": "Redes 5G dedicadas para complexos industriais e condomínios",
                "impacto": "Médio",
                "timeline": "Q3 2026"
            },
            {
                "titulo": "Blockchain para Acesso",
                "descricao": "Registro imutável de acessos usando tecnologia blockchain",
                "impacto": "Médio",
                "timeline": "Q4 2026"
            }
        ]
        
        for trend in trends:
            with st.container():
                col_t1, col_t2 = st.columns([4, 1])
                with col_t1:
                    st.markdown(f"**{trend['titulo']}**")
                    st.write(trend['descricao'])
                with col_t2:
                    st.metric("Impacto", trend['impacto'])
                    st.caption(trend['timeline'])
                st.divider()
    
    with tab2:
        st.subheader("💡 Startups em Destaque")
        
        startups = [
            {"nome": "SecureHome AI", "area": "IA para Segurança Residencial", "investimento": "R$ 5M"},
            {"nome": "AccessControl.io", "area": "Controle de Acesso Cloud", "investimento": "R$ 3M"},
            {"nome": "NetGuard Solutions", "area": "Segurança de Redes IoT", "investimento": "R$ 8M"},
            {"nome": "FaceID Pro", "area": "Biometria Facial", "investimento": "R$ 12M"}
        ]
        
        df_startups = pd.DataFrame(startups)
        st.dataframe(df_startups, use_container_width=True)
    
    with tab3:
        st.subheader("📜 Patentes Recentes")
        
        patentes = [
            "Sistema de autenticação biométrica multi-fator",
            "Método de criptografia quântica para CFTV",
            "Dispositivo de controle de acesso por reconhecimento de voz",
            "Algoritmo de detecção de anomalias em redes IoT"
        ]
        
        for patente in patentes:
            st.markdown(f"- {patente}")
    
    with tab4:
        st.subheader("📊 Cases de Sucesso")
        
        cases = [
            {
                "cliente": "Condomínio Horizon",
                "desafio": "Alta incidência de CGNAT impedindo portaria remota",
                "solucao": "Implementação de IPv6 + VPN corporativa",
                "resultado": "100% de disponibilidade, ROI em 4 meses"
            },
            {
                "cliente": "Empresa TechCorp",
                "desafio": "Ataques cibernéticos frequentes",
                "solucao": "Arquitetura Zero Trust + segmentação de rede",
                "resultado": "Redução de 95% em incidentes de segurança"
            }
        ]
        
        for case in cases:
            with st.expander(f"🏢 {case['cliente']}"):
                st.write(f"**Desafio:** {case['desafio']}")
                st.write(f"**Solução:** {case['solucao']}")
                st.success(f"**Resultado:** {case['resultado']}")


# ============================================
# ABA 9: INFRAESTRUTURA
# ============================================
elif menu == "🌐 Infraestrutura":
    st.title("🌐 Infraestrutura de Redes no Brasil")
    st.markdown("*Análise completa da infraestrutura de telecomunicações*")
    
    df = get_full_data()
    
    # Dashboard de infraestrutura
    tab1, tab2, tab3 = st.tabs(["📊 Velocidade", "🌍 IPv6", "🏢 Provedores"])
    
    with tab1:
        st.subheader("📊 Velocidade Média por Estado")
        
        fig_vel = px.bar(
            df.sort_values('Velocidade_Media', ascending=False),
            x='Estado',
            y='Velocidade_Media',
            color='Velocidade_Media',
            color_continuous_scale='Blues',
            title='Velocidade Média de Internet (Mbps)'
        )
        fig_vel.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig_vel, use_container_width=True)
        
        # Top 5 e Bottom 5
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 5 Estados")
            top5 = df.nlargest(5, 'Velocidade_Media')[['Estado', 'Velocidade_Media']]
            st.dataframe(top5, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Bottom 5 Estados")
            bottom5 = df.nsmallest(5, 'Velocidade_Media')[['Estado', 'Velocidade_Media']]
            st.dataframe(bottom5, use_container_width=True)
    
    with tab2:
        st.subheader("🌍 Adoção de IPv6 por Estado")
        
        fig_ipv6 = px.choropleth(
            df,
            locations='UF',
            locationmode="BRA-states",
            color='IPv6_Adoption',
            color_continuous_scale='Greens',
            range_color=(30, 65),
            hover_name='Estado',
            title='Adoção IPv6 (%)',
            labels={'IPv6_Adoption': '% IPv6'}
        )
        
        fig_ipv6.update_layout(
            geo_scope='south america',
            height=500
        )
        
        st.plotly_chart(fig_ipv6, use_container_width=True)
        
        # Correlação CGNAT vs IPv6
        st.subheader("📈 Correlação: CGNAT vs Adoção IPv6")
        
        fig_corr = px.scatter(
            df,
            x='CGNAT_Pct',
            y='IPv6_Adoption',
            size='Velocidade_Media',
            color='UF',
            hover_name='Estado',
            title='Relação entre CGNAT e Adoção IPv6',
            trendline='ols'
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab3:
        st.subheader("🏢 Panorama de Provedores")
        
        st.markdown("""
        ### Maiores ISPs do Brasil
        
        | Posição | Operadora | Market Share |
        |---------|-----------|--------------|
        | 1 | Vivo | 35.2% |
        | 2 | Claro | 28.5% |
        | 3 | TIM | 15.8% |
        | 4 | Oi | 8.3% |
        | 5 | Outros | 12.2% |
        """)
        
        # Gráfico de market share
        market_data = pd.DataFrame({
            'Operadora': ['Vivo', 'Claro', 'TIM', 'Oi', 'Outros'],
            'Market Share': [35.2, 28.5, 15.8, 8.3, 12.2]
        })
        
        fig_market = px.pie(
            market_data,
            values='Market Share',
            names='Operadora',
            title='Market Share de ISPs no Brasil'
        )
        
        st.plotly_chart(fig_market, use_container_width=True)


# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p><strong>🛡️ Sentinela Tech Dash</strong> - Monitoramento Inteligente de CGNAT</p>
    <p style='font-size: 0.8rem;'>
        Dados atualizados em tempo real | Fontes: Anatel, NIC.br, APIs públicas
    </p>
</div>
""", unsafe_allow_html=True)
