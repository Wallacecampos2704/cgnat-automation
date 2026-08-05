// Dados CGNAT por Estado (27 UFs)
const dadosCGNAT = {
    estados: [
        { uf: 'SP', nome: 'São Paulo', saturacao: 78.5, ips: 12500000 },
        { uf: 'RJ', nome: 'Rio de Janeiro', saturacao: 82.3, ips: 8900000 },
        { uf: 'MG', nome: 'Minas Gerais', saturacao: 71.2, ips: 7200000 },
        { uf: 'RS', nome: 'Rio Grande do Sul', saturacao: 68.9, ips: 4800000 },
        { uf: 'PR', nome: 'Paraná', saturacao: 73.4, ips: 4500000 },
        { uf: 'SC', nome: 'Santa Catarina', saturacao: 65.7, ips: 3200000 },
        { uf: 'BA', nome: 'Bahia', saturacao: 76.8, ips: 5100000 },
        { uf: 'PE', nome: 'Pernambuco', saturacao: 79.2, ips: 3800000 },
        { uf: 'CE', nome: 'Ceará', saturacao: 74.5, ips: 3500000 },
        { uf: 'GO', nome: 'Goiás', saturacao: 69.3, ips: 2900000 },
        { uf: 'PA', nome: 'Pará', saturacao: 81.7, ips: 3100000 },
        { uf: 'AM', nome: 'Amazonas', saturacao: 72.1, ips: 1800000 },
        { uf: 'MA', nome: 'Maranhão', saturacao: 77.9, ips: 2400000 },
        { uf: 'ES', nome: 'Espírito Santo', saturacao: 64.2, ips: 1500000 },
        { uf: 'PB', nome: 'Paraíba', saturacao: 75.6, ips: 1600000 },
        { uf: 'RN', nome: 'Rio Grande do Norte', saturacao: 70.8, ips: 1400000 },
        { uf: 'MT', nome: 'Mato Grosso', saturacao: 67.4, ips: 1300000 },
        { uf: 'MS', nome: 'Mato Grosso do Sul', saturacao: 63.9, ips: 1100000 },
        { uf: 'DF', nome: 'Distrito Federal', saturacao: 85.2, ips: 1900000 },
        { uf: 'AL', nome: 'Alagoas', saturacao: 78.1, ips: 1200000 },
        { uf: 'PI', nome: 'Piauí', saturacao: 73.7, ips: 1100000 },
        { uf: 'TO', nome: 'Tocantins', saturacao: 66.5, ips: 750000 },
        { uf: 'SE', nome: 'Sergipe', saturacao: 71.9, ips: 890000 },
        { uf: 'RO', nome: 'Rondônia', saturacao: 68.3, ips: 720000 },
        { uf: 'AC', nome: 'Acre', saturacao: 62.4, ips: 380000 },
        { uf: 'AP', nome: 'Amapá', saturacao: 69.7, ips: 420000 },
        { uf: 'RR', nome: 'Roraima', saturacao: 64.8, ips: 310000 }
    ],
    historico: [
        { mes: 'Jan/25', total: 98500000 },
        { mes: 'Fev/25', total: 101200000 },
        { mes: 'Mar/25', total: 104800000 },
        { mes: 'Abr/25', total: 107500000 },
        { mes: 'Mai/25', total: 110900000 },
        { mes: 'Jun/25', total: 114200000 },
        { mes: 'Jul/25', total: 117800000 },
        { mes: 'Ago/25', total: 121500000 },
        { mes: 'Set/25', total: 125100000 },
        { mes: 'Out/25', total: 128900000 },
        { mes: 'Nov/25', total: 132400000 },
        { mes: 'Dez/25', total: 136200000 }
    ]
};

// Notícias de Segurança Eletrônica
const noticias = [
    {
        id: 1,
        titulo: 'Brasil lidera adoção de câmeras IA na América Latina',
        resumo: 'Empresas brasileiras investem R$ 2.5 bi em sistemas de vigilância com inteligência artificial para 2026.',
        categoria: 'brasil',
        data: '2026-01-15',
        fonte: 'Segurança Total',
        icone: '🎥'
    },
    {
        id: 2,
        titulo: 'Nova vulnerabilidade em sistemas CFTV é descoberta',
        resumo: 'Pesquisadores identificam falha crítica em 500 mil dispositivos de monitoramento worldwide.',
        categoria: 'mundo',
        data: '2026-01-14',
        fonte: 'CyberSec News',
        icone: '⚠️'
    },
    {
        id: 3,
        titulo: 'Startup brasileira desenvolve drone autônomo para patrulhamento',
        resumo: 'Tecnologia usa reconhecimento facial e térmico para identificar invasões em tempo real.',
        categoria: 'inovacao',
        data: '2026-01-13',
        fonte: 'Inovação BR',
        icone: '🚁'
    },
    {
        id: 4,
        titulo: '5G privado revoluciona segurança industrial no Brasil',
        resumo: 'Indústrias adotam redes 5G dedicadas para sistemas de monitoramento de alta precisão.',
        categoria: 'redes',
        data: '2026-01-12',
        fonte: 'Telecom Brasil',
        icone: '📡'
    },
    {
        id: 5,
        titulo: 'Investimento em fibra óptica cresce 45% no Nordeste',
        resumo: 'Expansão da infraestrutura permite implementação de sistemas de segurança mais robustos.',
        categoria: 'infraestrutura',
        data: '2026-01-11',
        fonte: 'Infra News',
        icone: '🌐'
    },
    {
        id: 6,
        titulo: 'EUA anunciam nova regulamentação para IoT de segurança',
        resumo: 'Leis mais rigorosas visam proteger dados de milhões de dispositivos conectados.',
        categoria: 'mundo',
        data: '2026-01-10',
        fonte: 'Global Security',
        icone: '🇺🇸'
    },
    {
        id: 7,
        titulo: 'Biometria facial atinge 99.8% de precisão em testes brasileiros',
        resumo: 'Tecnologia desenvolvida por universidade federal supera padrões internacionais.',
        categoria: 'inovacao',
        data: '2026-01-09',
        fonte: 'Ciência Tech',
        icone: '👤'
    },
    {
        id: 8,
        titulo: 'Ataques a sistemas de segurança crescem 120% em 2025',
        resumo: 'Relatório aponta aumento significativo de tentativas de invasão a redes corporativas.',
        categoria: 'brasil',
        data: '2026-01-08',
        fonte: 'CERT.br',
        icone: '🔒'
    },
    {
        id: 9,
        titulo: 'Europa investe € 10 bi em cidades seguras inteligentes',
        resumo: 'Projeto integra câmeras, sensores e IA para criar ambientes urbanos mais seguros.',
        categoria: 'mundo',
        data: '2026-01-07',
        fonte: 'Euro Tech',
        icone: '🇪🇺'
    },
    {
        id: 10,
        titulo: 'Anatel aprova novo padrão para transmissão de vídeo segurança',
        resumo: 'Norma técnica garante qualidade mínima e interoperabilidade entre fabricantes.',
        categoria: 'infraestrutura',
        data: '2026-01-06',
        fonte: 'Anatel Oficial',
        icone: '📋'
    },
    {
        id: 11,
        titulo: 'Redes mesh ganham espaço em condomínios inteligentes',
        resumo: 'Tecnologia oferece redundância e cobertura total para sistemas de monitoramento.',
        categoria: 'redes',
        data: '2026-01-05',
        fonte: 'Condomínio Tech',
        icone: '🕸️'
    },
    {
        id: 12,
        titulo: 'Robôs de segurança começam operação em shoppings do RJ',
        resumo: 'Equipamentos autônomos fazem rondas noturnas e identificam anomalias.',
        categoria: 'inovacao',
        data: '2026-01-04',
        fonte: 'Rio Segurança',
        icone: '🤖'
    }
];

// Inovações e Tendências
const inovacoes = {
    tendencias: [
        {
            titulo: 'IA Generativa na Análise de Vídeo',
            descricao: 'Sistemas capazes de descrever cenas, identificar comportamentos suspeitos e gerar relatórios automáticos.',
            impacto: 'Alto',
            ano: '2026'
        },
        {
            titulo: 'Integração Blockchain para Logs de Segurança',
            descricao: 'Registros imutáveis de eventos de segurança garantindo integridade forense.',
            impacto: 'Médio',
            ano: '2026'
        },
        {
            titulo: 'Sensores Quânticos para Detecção',
            descricao: 'Tecnologia emergente promete detecção de movimento com sensibilidade sem precedentes.',
            impacto: 'Alto',
            ano: '2027'
        }
    ],
    startups: [
        {
            nome: 'SecureVision AI',
            localizacao: 'São Paulo, SP',
            foco: 'Reconhecimento de padrões em vídeo',
            investimento: 'R$ 15 mi'
        },
        {
            nome: 'NetGuard Solutions',
            localizacao: 'Florianópolis, SC',
            foco: 'Segurança de rede para IoT',
            investimento: 'R$ 8 mi'
        },
        {
            nome: 'BioMetrica',
            localizacao: 'Recife, PE',
            foco: 'Biometria multimodal',
            investimento: 'R$ 12 mi'
        }
    ],
    patentes: [
        {
            titulo: 'Sistema de Autenticação por Comportamento',
            depositante: 'Universidade de Campinas',
            ano: '2025',
            status: 'Concedida'
        },
        {
            titulo: 'Método de Criptografia para Vídeo em Tempo Real',
            depositante: 'Embraer Defesa',
            ano: '2025',
            status: 'Em análise'
        }
    ],
    cases: [
        {
            empresa: 'Banco Central do Brasil',
            desafio: 'Modernizar sistema de vigilância de 50 agências',
            solucao: 'IA + Câmeras 4K + Analytics',
            resultado: 'Redução de 87% em incidentes de segurança'
        },
        {
            empresa: 'Aeroporto de Guarulhos',
            desafio: 'Monitorar área de 14 km² com eficiência',
            solucao: 'Drones autônomos + Torres inteligentes',
            resultado: 'Cobertura 100% e resposta em < 2 minutos'
        }
    ]
};

// Dados de Infraestrutura
const infraestrutura = {
    velocidade: [
        { estado: 'SP', velocidade: 145.8 },
        { estado: 'RJ', velocidade: 132.4 },
        { estado: 'DF', velocidade: 158.2 },
        { estado: 'RS', velocidade: 128.9 },
        { estado: 'PR', velocidade: 135.6 },
        { estado: 'SC', velocidade: 141.3 },
        { estado: 'MG', velocidade: 118.7 },
        { estado: 'ES', velocidade: 112.4 },
        { estado: 'BA', velocidade: 98.5 },
        { estado: 'PE', velocidade: 105.2 }
    ],
    ipv6: {
        adesao: 48.7,
        crescimento: 12.3,
        ranking: 3
    },
    marketShare: [
        { isp: 'Claro', share: 32.5 },
        { isp: 'Vivo', share: 28.3 },
        { isp: 'TIM', share: 18.7 },
        { isp: 'Oi', share: 12.1 },
        { isp: 'Outros', share: 8.4 }
    ]
};

// Exportar dados
window.dadosBrasil = dadosCGNAT;
window.noticiasData = noticias;
window.inovacoesData = inovacoes;
window.infraestruturaData = infraestrutura;
