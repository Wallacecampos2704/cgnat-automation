// Aplicação Principal - Sentinela Tech Dash

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização
    initNavigation();
    initMenuMobile();
    initDashboard();
    initNoticias();
    initInovacoes();
    initInfraestrutura();
    initFerramentas();
});

// Navegação entre seções
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active de todos
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Adiciona active no clicado
            link.classList.add('active');
            const target = link.getAttribute('href').substring(1);
            document.getElementById(target).classList.add('active');
            
            // Fecha menu mobile se aberto
            document.getElementById('mainNav').classList.remove('active');
            
            // Renderiza gráficos da seção se necessário
            if (target === 'dashboard') renderDashboardCharts();
            if (target === 'cgnat') renderCGNATDetails();
            if (target === 'infraestrutura') renderInfraCharts();
        });
    });
}

// Menu Mobile
function initMenuMobile() {
    const menuToggle = document.getElementById('menuToggle');
    const mainNav = document.getElementById('mainNav');

    menuToggle.addEventListener('click', () => {
        mainNav.classList.toggle('active');
    });
}

// Dashboard Inicial
function initDashboard() {
    // Atualiza KPIs
    const totalIPs = dadosBrasil.estados.reduce((acc, est) => acc + est.ips, 0);
    const saturacaoMedia = dadosBrasil.estados.reduce((acc, est) => acc + est.saturacao, 0) / dadosBrasil.estados.length;
    const ufsCriticas = dadosBrasil.estados.filter(est => est.saturacao > 75).length;

    animateValue('kpi-total-cgnat', 0, totalIPs, 2000);
    animateValue('kpi-saturacao', 0, saturacaoMedia.toFixed(1), 2000, '%');
    animateValue('kpi-ufs-criticas', 0, ufsCriticas, 2000);
    animateValue('kpi-noticias', 0, noticias.length, 2000);

    // Renderiza gráficos do dashboard
    setTimeout(renderDashboardCharts, 500);
}

function renderDashboardCharts() {
    // Gráfico de Evolução
    const traceEvolucao = {
        x: dadosBrasil.historico.map(h => h.mes),
        y: dadosBrasil.historico.map(h => h.total / 1000000),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#2563eb', width: 3 },
        marker: { size: 8 },
        name: 'IPs CGNAT (Milhões)'
    };

    const layoutEvolucao = {
        title: '',
        xaxis: { title: 'Mês' },
        yaxis: { title: 'Total (Milhões)' },
        margin: { t: 30, b: 50, l: 60, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot('chart-evolucao', [traceEvolucao], layoutEvolucao, {responsive: true, displayModeBar: false});

    // Gráfico de Saturação por Estado (Top 10)
    const topEstados = [...dadosBrasil.estados]
        .sort((a, b) => b.saturacao - a.saturacao)
        .slice(0, 10);

    const traceSaturacao = {
        x: topEstados.map(e => e.uf),
        y: topEstados.map(e => e.saturacao),
        type: 'bar',
        marker: {
            color: topEstados.map(e => 
                e.saturacao > 75 ? '#ef4444' : 
                e.saturacao > 60 ? '#f59e0b' : '#10b981'
            )
        },
        name: 'Saturação (%)'
    };

    const layoutSaturacao = {
        title: '',
        xaxis: { title: 'Estado' },
        yaxis: { title: 'Saturação (%)', range: [0, 100] },
        margin: { t: 30, b: 50, l: 60, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot('chart-saturacao', [traceSaturacao], layoutSaturacao, {responsive: true, displayModeBar: false});

    // Mapa de Calor (Choropleth simplificado)
    renderMapaCalor();
}

function renderMapaCalor() {
    const traceMapa = {
        type: 'choropleth',
        locationmode: 'country names',
        locations: ['Brazil'],
        z: [dadosBrasil.estados.reduce((acc, e) => acc + e.saturacao, 0) / dadosBrasil.estados.length],
        text: ['Brasil'],
        colorscale: [
            [0, '#10b981'],
            [0.5, '#f59e0b'],
            [1, '#ef4444']
        ],
        autocolorscale: false,
        showscale: false,
        hoverinfo: 'text'
    };

    // Como o choropleth do Brasil requer geojson, usamos um gráfico de barras horizontais como alternativa
    const estadosOrdenados = [...dadosBrasil.estados].sort((a, b) => b.saturacao - a.saturacao);

    const traceBarras = {
        y: estadosOrdenados.map(e => e.nome),
        x: estadosOrdenados.map(e => e.saturacao),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: estadosOrdenados.map(e => 
                e.saturacao > 75 ? '#ef4444' : 
                e.saturacao > 60 ? '#f59e0b' : '#10b981'
            )
        }
    };

    const layoutMapa = {
        title: 'Saturação CGNAT por Estado',
        xaxis: { title: 'Saturação (%)', range: [0, 100] },
        margin: { t: 30, b: 50, l: 150, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        height: 800
    };

    Plotly.newPlot('mapa-brasil', [traceBarras], layoutMapa, {responsive: true, displayModeBar: false});
}

// Detalhes CGNAT
function renderCGNATDetails() {
    // Popula filtro de estados
    const filtroEstado = document.getElementById('filtro-estado');
    dadosBrasil.estados.forEach(est => {
        const option = document.createElement('option');
        option.value = est.uf;
        option.textContent = `${est.nome} (${est.uf})`;
        filtroEstado.appendChild(option);
    });

    // Top 5 Estados
    const top5 = [...dadosBrasil.estados]
        .sort((a, b) => b.saturacao - a.saturacao)
        .slice(0, 5);

    const topContainer = document.getElementById('top-estados');
    topContainer.innerHTML = top5.map(est => `
        <div class="estado-item">
            <span class="estado-nome">${est.nome}</span>
            <span class="estado-valor">${est.saturacao.toFixed(1)}%</span>
        </div>
    `).join('');

    // Histórico Mensal
    const traceHistorico = {
        x: dadosBrasil.historico.map(h => h.mes),
        y: dadosBrasil.historico.map(h => h.total / 1000000),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#0891b2', width: 3 },
        fill: 'tozeroy'
    };

    const layoutHistorico = {
        margin: { t: 30, b: 50, l: 60, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot('historico-mensal', [traceHistorico], layoutHistorico, {responsive: true, displayModeBar: false});

    // Alertas
    const alertasContainer = document.getElementById('alertas-lista');
    const criticos = dadosBrasil.estados.filter(e => e.saturacao > 75);
    
    alertasContainer.innerHTML = criticos.map(est => `
        <div class="alerta-item">
            <span class="alerta-icon">⚠️</span>
            <div>
                <strong>${est.nome}</strong> - Saturação crítica de ${est.saturacao.toFixed(1)}%
                <br><small>${(est.ips / 1000000).toFixed(1)} milhões de IPs afetados</small>
            </div>
        </div>
    `).join('');
}

// Notícias
function initNoticias() {
    renderNoticias('todas');

    const filtros = document.querySelectorAll('.filtro-btn');
    filtros.forEach(btn => {
        btn.addEventListener('click', () => {
            filtros.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderNoticias(btn.dataset.categoria);
        });
    });
}

function renderNoticias(categoria) {
    const container = document.getElementById('noticias-grid');
    const filtradas = categoria === 'todas' 
        ? noticias 
        : noticias.filter(n => n.categoria === categoria);

    container.innerHTML = filtradas.map(n => `
        <div class="noticia-card">
            <div class="noticia-imagem">${n.icone}</div>
            <div class="noticia-conteudo">
                <span class="noticia-categoria">${formatarCategoria(n.categoria)}</span>
                <h4 class="noticia-titulo">${n.titulo}</h4>
                <p class="noticia-resumo">${n.resumo}</p>
                <div class="noticia-meta">
                    <span>${formatarData(n.data)}</span>
                    <span>${n.fonte}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function formatarCategoria(cat) {
    const categorias = {
        brasil: '🇧🇷 Brasil',
        mundo: '🌍 Mundo',
        inovacao: '💡 Inovação',
        redes: '📡 Redes',
        infraestrutura: '🏗️ Infraestrutura'
    };
    return categorias[cat] || cat;
}

function formatarData(dataStr) {
    const data = new Date(dataStr);
    return data.toLocaleDateString('pt-BR');
}

// Inovações
function initInovacoes() {
    renderTabInovacoes('tendencias');

    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            tabs.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderTabInovacoes(btn.dataset.tab);
        });
    });
}

function renderTabInovacoes(tab) {
    const container = document.getElementById('conteudo-inovacoes');
    const dados = inovacoesData[tab];

    if (tab === 'tendencias') {
        container.innerHTML = dados.map(t => `
            <div style="margin-bottom: 25px; padding: 20px; background: #f8fafc; border-radius: 10px;">
                <h4 style="color: #2563eb; margin-bottom: 10px;">${t.titulo}</h4>
                <p style="color: #64748b; margin-bottom: 10px;">${t.descricao}</p>
                <div style="display: flex; gap: 20px;">
                    <span style="background: #10b981; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem;">Impacto: ${t.impacto}</span>
                    <span style="background: #0891b2; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem;">${t.ano}</span>
                </div>
            </div>
        `).join('');
    } else if (tab === 'startups') {
        container.innerHTML = `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">` +
            dados.map(s => `
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px;">
                    <h4 style="color: #2563eb; margin-bottom: 10px;">${s.nome}</h4>
                    <p style="color: #64748b; font-size: 0.9rem;">📍 ${s.localizacao}</p>
                    <p style="color: #64748b; font-size: 0.9rem;">🎯 ${s.foco}</p>
                    <p style="color: #10b981; font-weight: bold; margin-top: 10px;">💰 ${s.investimento}</p>
                </div>
            `).join('') + `</div>`;
    } else if (tab === 'patentes') {
        container.innerHTML = dados.map(p => `
            <div style="margin-bottom: 20px; padding: 20px; background: #f8fafc; border-radius: 10px; border-left: 4px solid #2563eb;">
                <h4 style="color: #2563eb; margin-bottom: 10px;">${p.titulo}</h4>
                <p style="color: #64748b;">Depositante: ${p.depositante}</p>
                <div style="display: flex; gap: 15px; margin-top: 10px;">
                    <span>Ano: ${p.ano}</span>
                    <span style="background: ${p.status === 'Concedida' ? '#10b981' : '#f59e0b'}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.8rem;">${p.status}</span>
                </div>
            </div>
        `).join('');
    } else if (tab === 'cases') {
        container.innerHTML = dados.map(c => `
            <div style="margin-bottom: 25px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;">
                <h4 style="margin-bottom: 15px;">🏢 ${c.empresa}</h4>
                <div style="display: grid; gap: 10px;">
                    <div><strong>Desafio:</strong> ${c.desafio}</div>
                    <div><strong>Solução:</strong> ${c.solucao}</div>
                    <div style="background: rgba(16, 185, 129, 0.3); padding: 10px; border-radius: 8px;"><strong>✅ Resultado:</strong> ${c.resultado}</div>
                </div>
            </div>
        `).join('');
    }
}

// Infraestrutura
function initInfraestrutura() {
    // Será renderizado quando a seção for ativa
}

function renderInfraCharts() {
    // Velocidade por Estado
    const traceVelocidade = {
        x: infraestruturaData.velocidade.map(d => d.estado),
        y: infraestruturaData.velocidade.map(d => d.velocidade),
        type: 'bar',
        marker: { color: '#0891b2' }
    };

    const layoutVelocidade = {
        margin: { t: 30, b: 50, l: 60, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot('chart-velocidade', [traceVelocidade], layoutVelocidade, {responsive: true, displayModeBar: false});

    // Adoção IPv6
    const traceIPv6 = {
        values: [infraestruturaData.ipv6.adesao, 100 - infraestruturaData.ipv6.adesao],
        labels: ['Com IPv6', 'Sem IPv6'],
        type: 'pie',
        marker: { colors: ['#10b981', '#e2e8f0'] }
    };

    const layoutIPv6 = {
        margin: { t: 30, b: 30, l: 30, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        showlegend: true
    };

    Plotly.newPlot('chart-ipv6', [traceIPv6], layoutIPv6, {responsive: true, displayModeBar: false});

    // Market Share
    const traceMarket = {
        x: infraestruturaData.marketShare.map(d => d.isp),
        y: infraestruturaData.marketShare.map(d => d.share),
        type: 'bar',
        marker: { 
            color: ['#ef4444', '#f59e0b', '#10b981', '#0891b2', '#64748b']
        }
    };

    const layoutMarket = {
        margin: { t: 30, b: 50, l: 60, r: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot('chart-market-share', [traceMarket], layoutMarket, {responsive: true, displayModeBar: false});
}

// Ferramentas
function initFerramentas() {
    // Calculadora ROI
    document.getElementById('form-roi').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const investimento = parseFloat(document.getElementById('roi-investimento').value);
        const retorno = parseFloat(document.getElementById('roi-retorno').value);
        const periodo = parseInt(document.getElementById('roi-periodo').value);

        const roiTotal = ((retorno * periodo - investimento) / investimento) * 100;
        const roiMensal = (retorno / investimento) * 100;
        const payback = investimento / retorno;

        const resultado = document.getElementById('resultado-roi');
        resultado.innerHTML = `
            <h4 style="color: #2563eb; margin-bottom: 15px;">📊 Resultados do ROI</h4>
            <div style="display: grid; gap: 10px;">
                <div><strong>ROI Total:</strong> <span style="color: ${roiTotal > 0 ? '#10b981' : '#ef4444'}">${roiTotal.toFixed(2)}%</span></div>
                <div><strong>ROI Mensal:</strong> ${roiMensal.toFixed(2)}%</div>
                <div><strong>Payback:</strong> ${payback.toFixed(1)} meses</div>
                <div><strong>Lucro Líquido:</strong> R$ ${(retorno * periodo - investimento).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
            </div>
        `;
        resultado.classList.add('visible');
    });

    // Diagnóstico Regional
    const selectEstado = document.getElementById('diag-estado');
    dadosBrasil.estados.forEach(est => {
        const option = document.createElement('option');
        option.value = est.uf;
        option.textContent = est.nome;
        selectEstado.appendChild(option);
    });

    document.getElementById('form-diagnostico').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const uf = document.getElementById('diag-estado').value;
        const tipo = document.getElementById('diag-tipo').value;
        const estado = dadosBrasil.estados.find(e => e.uf === uf);

        let recomendacao = '';
        let urgencia = '';
        
        if (estado.saturacao > 75) {
            urgencia = 'Alta';
            recomendacao = 'Recomenda-se migração urgente para IPv6 ou contratação de link dedicado.';
        } else if (estado.saturacao > 60) {
            urgencia = 'Média';
            recomendacao = 'Planejar migração para IPv6 nos próximos 6 meses.';
        } else {
            urgencia = 'Baixa';
            recomendacao = 'Condições adequadas. Monitorar evolução trimestralmente.';
        }

        const resultado = document.getElementById('resultado-diagnostico');
        resultado.innerHTML = `
            <h4 style="color: #2563eb; margin-bottom: 15px;">🔍 Diagnóstico para ${estado.nome}</h4>
            <div style="display: grid; gap: 10px;">
                <div><strong>Saturação CGNAT:</strong> ${estado.saturacao.toFixed(1)}%</div>
                <div><strong>IPs Afetados:</strong> ${(estado.ips / 1000000).toFixed(1)} milhões</div>
                <div><strong>Tipo de Rede:</strong> ${tipo.charAt(0).toUpperCase() + tipo.slice(1)}</div>
                <div><strong>Urgência:</strong> <span style="background: ${urgencia === 'Alta' ? '#ef4444' : urgencia === 'Média' ? '#f59e0b' : '#10b981'}; color: white; padding: 3px 10px; border-radius: 15px;">${urgencia}</span></div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-top: 10px;"><strong>Recomendação:</strong> ${recomendacao}</div>
            </div>
        `;
        resultado.classList.add('visible');
    });
}

// Animação de valores
function animateValue(id, start, end, duration, suffix = '') {
    const obj = document.getElementById(id);
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        
        if (typeof end === 'number' && end > 1000000) {
            obj.textContent = (current / 1000000).toFixed(1) + 'M' + suffix;
        } else if (typeof end === 'number' && end > 1000) {
            obj.textContent = Math.floor(current).toLocaleString('pt-BR') + suffix;
        } else {
            obj.textContent = current.toFixed(1) + suffix;
        }
    }, 16);
}
