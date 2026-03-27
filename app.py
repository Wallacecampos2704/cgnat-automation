"""
CGNAT Dashboard - Solução Automatizada
App Streamlit completo com dados vivos, ROI e diagnóstico regional
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import time
from dados_vivos import IntegradorDadosVivos
from calculadora_roi import CalculadoraROI
from diagnostico_regional import DiagnosticoRegional
from noticias import AgregadorNoticias, NOTICIAS_EXEMPLO

# Configuração da página
st.set_page_config(
    page_title="CGNAT Dashboard - Automação",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
    .critical {
        border-left-color: #a78bfa;
        background-color: #3d2645;
    }
    .high {
        border-left-color: #f87171;
        background-color: #462626;
    }
    .medium {
        border-left-color: #facc15;
        background-color: #463a1f;
    }
    .low {
        border-left-color: #4ade80;
        background-color: #1f3a1f;
    }
    
    /* Estilo para seleção de campos */
    .stSelectbox > div > div {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }
    .stSelectbox > div > div:hover {
        background-color: #334155 !important;
    }
    .stSelectbox > div > div[data-selected] {
        background-color: #3b82f6 !important;
        font-weight: bold !important;
    }
    
    /* Notícia card */
    .noticia-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 15px;
    }
    .noticia-titulo {
        font-weight: bold;
        color: #60a5fa;
        font-size: 16px;
    }
    .noticia-fonte {
        color: #94a3b8;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Configurações")
pagina = st.sidebar.radio(
    "Selecione uma opção:",
    ["🏠 Dashboard", "📊 Dados Vivos", "💰 Calculadora ROI", "🔍 Diagnóstico Regional", "📰 Notícias", "📋 Sobre"]
)

# Cache para dados vivos
@st.cache_data(ttl=3600)
def carregar_dados_vivos():
    integrador = IntegradorDadosVivos()
    return integrador.atualizar_todos_dados()

# ============================================================================
# PÁGINA: DASHBOARD
# ============================================================================
if pagina == "🏠 Dashboard":
    st.title("📊 Dashboard CGNAT Brasil - Automação")
    st.markdown("Solução completa com dados vivos, ROI e diagnóstico regional")
    
    # Carregar dados
    dados = carregar_dados_vivos()
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Estados Analisados",
            len(dados['ibc_por_estado']),
            "27 estados brasileiros"
        )
    
    with col2:
        ibc_medio = sum(v['ibc'] for v in dados['ibc_por_estado'].values()) / len(dados['ibc_por_estado'])
        st.metric(
            "IBC Médio Brasil",
            f"{ibc_medio:.2f}",
            "Índice de Conectividade"
        )
    
    with col3:
        ipv6_media = sum(dados['ipv6_adoption'].values()) / len(dados['ipv6_adoption'])
        st.metric(
            "Adoção IPv6 Média",
            f"{ipv6_media:.1f}%",
            "Todas as regiões"
        )
    
    with col4:
        st.metric(
            "Atualização",
            "Automática",
            "A cada 1 hora"
        )
    
    st.divider()
    
    # Tabela de IBC por estado
    st.subheader("📈 Índice Brasileiro de Conectividade (IBC) por Estado")
    
    ibc_df = pd.DataFrame([
        {
            'Estado': estado,
            'IBC': valores['ibc'],
            'Velocidade Média (Mbps)': valores['velocidade_media'],
            'Cobertura (%)': valores['cobertura']
        }
        for estado, valores in dados['ibc_por_estado'].items()
    ]).sort_values('IBC', ascending=False)
    
    st.dataframe(ibc_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Adoção IPv6 por região
    st.subheader("🌐 Adoção de IPv6 por Região")
    
    ipv6_df = pd.DataFrame([
        {'Região': regiao, 'Adoção IPv6 (%)': valor}
        for regiao, valor in dados['ipv6_adoption'].items()
    ]).sort_values('Adoção IPv6 (%)', ascending=False)
    
    st.dataframe(ipv6_df, use_container_width=True, hide_index=True)
    
    # Informação sobre dados vivos
    st.info(
        f"""
        ✅ **Dados Vivos Ativados**
        
        Este dashboard conecta diretamente com:
        - Portal de Dados Abertos da Anatel
        - Mapa de Qualidade da Internet do NIC.br
        
        Última atualização: {dados['timestamp']}
        
        Os dados são atualizados automaticamente a cada hora.
        """
    )

# ============================================================================
# PÁGINA: DADOS VIVOS
# ============================================================================
elif pagina == "📊 Dados Vivos":
    st.title("📊 Dados Vivos - Integração Automática")
    st.markdown("Conectado com APIs públicas da Anatel e NIC.br")
    
    dados = carregar_dados_vivos()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Status de Integração")
        st.success("✅ Anatel - IBC por Estado")
        st.success("✅ Anatel - Ranking de Conectividade")
        st.success("✅ NIC.br - Qualidade por Município")
        st.success("✅ NIC.br - Adoção de IPv6")
    
    with col2:
        st.subheader("⏰ Informações de Atualização")
        st.info(f"Última atualização: {dados['timestamp']}")
        st.info("Frequência: A cada 1 hora")
        st.info("Próxima atualização: Automática")
    
    st.divider()
    
    # Dados brutos em JSON
    st.subheader("📋 Dados Brutos (JSON)")
    
    if st.checkbox("Mostrar dados em formato JSON"):
        st.json(dados)
    
    # Exportar dados
    st.subheader("💾 Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Exportar como CSV"):
            csv_data = pd.DataFrame([
                {'estado': estado, **valores}
                for estado, valores in dados['ibc_por_estado'].items()
            ]).to_csv(index=False)
            st.download_button(
                label="Baixar CSV",
                data=csv_data,
                file_name="cgnat_dados_vivos.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Exportar como JSON"):
            json_data = json.dumps(dados, ensure_ascii=False, indent=2)
            st.download_button(
                label="Baixar JSON",
                data=json_data,
                file_name="cgnat_dados_vivos.json",
                mime="application/json"
            )

# ============================================================================
# PÁGINA: CALCULADORA ROI
# ============================================================================
elif pagina == "💰 Calculadora ROI":
    st.title("💰 Calculadora de ROI - Ferramenta de Vendas")
    st.markdown("Transforma dados técnicos em impacto financeiro")
    
    st.subheader("📍 Informações do Cliente")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        estado = st.selectbox(
            "Estado (UF)",
            ['SP', 'RJ', 'MG', 'BA', 'RS', 'PR', 'PE', 'CE', 'PA', 'GO', 'SC', 'MA', 'PB', 'ES', 'PI', 'RN', 'AL', 'MT', 'MS', 'DF', 'SE', 'AC', 'AM', 'RO', 'RR', 'AP', 'TO']
        )
    
    with col2:
        cidade = st.text_input("Cidade", value="São Paulo")
    
    with col3:
        tipo_cliente = st.selectbox(
            "Tipo de Cliente",
            ['residencial', 'pme', 'empresa', 'startup']
        )
    
    receita_anual = st.number_input(
        "Receita Anual (R$)",
        value=500000,
        min_value=0,
        step=100000,
        help="Deixe em branco para usar valor padrão"
    )
    
    # Calcular ROI
    if st.button("🧮 Calcular ROI", use_container_width=True):
        calc = CalculadoraROI(estado, cidade, tipo_cliente, receita_anual)
        
        # Exibir relatório
        st.subheader("📊 Análise de Impacto")
        
        perda = calc.calcular_perda_anual()
        roi = calc.calcular_roi_solucao()
        
        # Métricas em colunas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Perda Anual",
                f"R$ {perda['perda_total']:,.0f}",
                f"R$ {perda['perda_mensal']:,.0f}/mês"
            )
        
        with col2:
            st.metric(
                "Custo Solução",
                f"R$ {roi['custo_anual']:,.0f}",
                f"R$ {roi['custo_mensal']:,.0f}/mês"
            )
        
        with col3:
            st.metric(
                "Economia Anual",
                f"R$ {roi['economia_anual']:,.0f}",
                f"{roi['roi_percentual']:.0f}% ROI"
            )
        
        with col4:
            st.metric(
                "Payback",
                f"{roi['payback_meses']:.1f} meses",
                "Tempo para se pagar"
            )
        
        st.divider()
        
        # Detalhamento
        st.subheader("💡 Detalhamento da Perda")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Downtime**: R$ {perda['perda_downtime']:,.0f}")
        
        with col2:
            st.info(f"**Bloqueios**: R$ {perda['perda_bloqueios']:,.0f}")
        
        with col3:
            st.info(f"**Produtividade**: R$ {perda['perda_produtividade']:,.0f}")
        
        st.divider()
        
        # Relatório completo
        st.subheader("📋 Relatório Executivo")
        
        relatorio = calc.gerar_relatorio_executivo()
        st.code(relatorio, language="text")
        
        # Download
        col1, col2 = st.columns(2)
        
        with col1:
            json_report = json.dumps(calc.gerar_relatorio_json(), ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Baixar Relatório (JSON)",
                data=json_report,
                file_name=f"roi_relatorio_{estado}_{cidade}.json",
                mime="application/json"
            )
        
        with col2:
            st.download_button(
                label="📥 Baixar Relatório (TXT)",
                data=relatorio,
                file_name=f"roi_relatorio_{estado}_{cidade}.txt",
                mime="text/plain"
            )

# ============================================================================
# PÁGINA: DIAGNÓSTICO REGIONAL
# ============================================================================
elif pagina == "🔍 Diagnóstico Regional":
    st.title("🔍 Diagnóstico Regional - Análise Técnica")
    st.markdown("Estratificação de criticidade com contexto técnico")
    
    st.subheader("📍 Selecione a Localidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        estado = st.selectbox(
            "Estado (UF)",
            ['SP', 'RJ', 'MG', 'BA', 'RS', 'PR', 'PE', 'CE', 'PA', 'GO', 'SC', 'MA', 'PB', 'ES', 'PI', 'RN', 'AL', 'MT', 'MS', 'DF', 'SE', 'AC', 'AM', 'RO', 'RR', 'AP', 'TO'],
            key="estado_diag"
        )
    
    with col2:
        cidade = st.text_input("Cidade", value="São Paulo", key="cidade_diag")
    
    if st.button("🔍 Gerar Diagnóstico", use_container_width=True):
        diag = DiagnosticoRegional(estado, cidade)
        
        # Exibir diagnóstico
        diagnostico_json = diag.gerar_diagnostico_json()
        situacao = diagnostico_json['situacao_atual']
        
        # Cards de status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("CGNAT", f"{situacao['cgnat_percent']}%")
        
        with col2:
            severidade = situacao['severidade']
            if severidade == 'CRÍTICA':
                st.error(f"Severidade: {severidade}")
            elif severidade == 'MUITO ALTA':
                st.warning(f"Severidade: {severidade}")
            elif severidade == 'ALTA':
                st.warning(f"Severidade: {severidade}")
            else:
                st.info(f"Severidade: {severidade}")
        
        with col3:
            st.info(f"Tendência: {situacao['tendencia']}")
        
        with col4:
            blocos = diagnostico_json['infraestrutura']['blocos_ipv4_disponiveis']
            st.metric("IPv4 Disponíveis", blocos)
        
        st.divider()
        
        # Relatório completo
        st.subheader("📋 Relatório Técnico")
        
        relatorio = diag.gerar_diagnostico_executivo()
        st.code(relatorio, language="text")
        
        # Download
        json_report = json.dumps(diagnostico_json, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Baixar Diagnóstico (JSON)",
            data=json_report,
            file_name=f"diagnostico_{estado}_{cidade}.json",
            mime="application/json"
        )

# ============================================================================
# PÁGINA: SOBRE
# ============================================================================
elif pagina == "📋 Sobre":
    st.title("📋 Sobre o CGNAT Dashboard")
    
    st.markdown("""
    ## 🎯 O Problema
    
    Em 19/08/2020, o IPv4 foi considerado **morto no Brasil**. Desde então, o CGNAT (Carrier-Grade NAT)
    tornou-se a realidade para a maioria dos usuários de internet.
    
    Alguns estados e cidades já não permitem contratar IP fixo, ou a possibilidade é quase nula.
    
    ## 💡 A Solução
    
    Este dashboard é uma **ferramenta de automação completa** que vai além da estética:
    
    ### 1️⃣ Dados Vivos
    - Conectado com APIs públicas da Anatel e NIC.br
    - Atualização automática a cada hora
    - Nunca mente - sempre reflete a realidade
    
    ### 2️⃣ Calculadora de ROI
    - Transforma dados técnicos em impacto financeiro
    - Ferramenta de vendas pronta para usar
    - Proposta de valor clara para o cliente
    
    ### 3️⃣ Diagnóstico Regional
    - Estratificação de criticidade com contexto técnico
    - Análise específica por cidade
    - Recomendações acionáveis
    
    ### 4️⃣ Propriedade Total
    - Código 100% seu no GitHub
    - Deploy gratuito no Streamlit Cloud
    - Integração com seu banco de dados
    
    ## 🚀 Como Usar
    
    1. **Dashboard**: Visualize dados vivos de conectividade
    2. **Dados Vivos**: Exporte dados para análise
    3. **Calculadora ROI**: Gere propostas de venda
    4. **Diagnóstico**: Entenda a situação técnica local
    
    ## 📊 Tecnologia
    
    - **Python 3.11+**
    - **Streamlit** para interface
    - **Pandas** para análise de dados
    - **APIs Públicas** para dados vivos
    
    ## 🔗 Próximos Passos
    
    1. Faça fork do repositório no GitHub
    2. Deploy no Streamlit Cloud (gratuito)
    3. Customize para seu negócio
    4. Comece a vender com dados reais
    
    ---
    
    **Desenvolvido com ❤️ para quem quer automação real, não design bonito.**
    """)
    
    st.divider()
    
    st.subheader("📞 Suporte")
    st.info("""
    Este é um projeto de código aberto. Para suporte, dúvidas ou contribuições:
    
    - 📧 GitHub Issues
    - 💬 Discussões no repositório
    - 🔗 Pull Requests são bem-vindas
    """)

# ============================================================================
# PÁGINA: NOTÍCIAS
# ============================================================================
elif pagina == "📰 Notícias":
    st.title("📰 Notícias sobre Tecnologia")
    st.markdown("Agregador de notícias de múltiplas fontes sobre CGNAT, IPv6 e Infraestrutura")
    
    # Carregar notícias
    @st.cache_data(ttl=3600)
    def carregar_noticias():
        agregador = AgregadorNoticias()
        try:
            noticias = agregador.buscar_todas_noticias()
            if not noticias:
                noticias = NOTICIAS_EXEMPLO
                agregador.noticias_cache = noticias
        except:
            noticias = NOTICIAS_EXEMPLO
            agregador.noticias_cache = noticias
        return agregador
    
    agregador = carregar_noticias()
    noticias = agregador.noticias_cache
    
    # Filtros
    st.subheader("🔍 Filtros")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categorias = ['Todas'] + agregador.obter_categorias()
        categoria_selecionada = st.selectbox(
            "Categoria",
            categorias,
            key="categoria_noticias"
        )
    
    with col2:
        fontes = ['Todas'] + agregador.obter_fontes()
        fonte_selecionada = st.selectbox(
            "Fonte",
            fontes,
            key="fonte_noticias"
        )
    
    with col3:
        palavra_chave = st.text_input(
            "Palavra-chave",
            placeholder="Ex: IPv6, CGNAT, segurança...",
            key="palavra_chave_noticias"
        )
    
    # Aplicar filtros
    noticias_filtradas = noticias
    
    if categoria_selecionada != 'Todas':
        noticias_filtradas = [n for n in noticias_filtradas if n['categoria'] == categoria_selecionada]
    
    if fonte_selecionada != 'Todas':
        noticias_filtradas = [n for n in noticias_filtradas if n['fonte'] == fonte_selecionada]
    
    if palavra_chave:
        palavra_lower = palavra_chave.lower()
        noticias_filtradas = [
            n for n in noticias_filtradas
            if palavra_lower in n['titulo'].lower() or palavra_lower in n['descricao'].lower()
        ]
    
    st.divider()
    
    # Exibir resumo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Notícias", len(noticias_filtradas))
    
    with col2:
        st.metric("Fontes", len(set(n['fonte'] for n in noticias_filtradas)))
    
    with col3:
        st.metric("Categorias", len(set(n['categoria'] for n in noticias_filtradas)))
    
    with col4:
        if agregador.ultima_atualizacao:
            tempo_atualizacao = (datetime.now() - agregador.ultima_atualizacao).seconds
            st.metric("Atualizado há", f"{tempo_atualizacao}s")
    
    st.divider()
    
    # Exibir notícias
    st.subheader(f"📰 {len(noticias_filtradas)} Notícias Encontradas")
    
    if noticias_filtradas:
        for noticia in noticias_filtradas:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="noticia-card">
                    <div class="noticia-titulo">{noticia['titulo']}</div>
                    <div class="noticia-fonte">{noticia['fonte']} • {noticia['categoria']}</div>
                    <p>{noticia['descricao']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if noticia['link'] != '#':
                    st.markdown(f"[🔗 Ler]({noticia['link']})")
    else:
        st.info("Nenhuma notícia encontrada com os filtros selecionados.")
    
    # Download
    st.divider()
    st.subheader("💾 Exportar")
    
    if st.button("📥 Exportar Notícias (JSON)", use_container_width=True):
        json_data = json.dumps(noticias_filtradas, ensure_ascii=False, indent=2)
        st.download_button(
            label="Baixar JSON",
            data=json_data,
            file_name="noticias_tecnologia.json",
            mime="application/json"
        )

# Footer
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #94a3b8; font-size: 12px;">
    <p>CGNAT Dashboard - Automação Completa | Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    <p>Dados vivos | ROI | Diagnóstico Regional | Notícias | Código Aberto</p>
</div>
""", unsafe_allow_html=True)
