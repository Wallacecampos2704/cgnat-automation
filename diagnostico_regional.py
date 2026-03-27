"""
Motor de Diagnóstico Regional
Estratifica criticidade CGNAT com contexto técnico por região
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiagnosticoRegional:
    """Análise técnica regional com contexto de infraestrutura"""
    
    # Base de conhecimento regional
    BASE_CONHECIMENTO = {
        'SP': {
            'São Paulo': {
                'cgnat_percent': 98,
                'causa_raiz': 'Saturação Total + Densidade Urbana Extrema',
                'provedores_dominantes': ['Vivo', 'Claro', 'NET', 'Embratel'],
                'blocos_ipv4_disponiveis': 0,
                'tendencia': 'Estável em nível crítico',
                'alternativas': ['IPv6 (recomendado)', 'IP Fixo Premium', 'Multiconexão'],
                'custo_solucao': 'R$ 300-500/mês',
                'tempo_implementacao': '3-5 dias',
                'severidade': 'CRÍTICA',
            },
            'Bauru': {
                'cgnat_percent': 96,
                'causa_raiz': 'Saturação de Fibra (2019-2020) - Polo de ISPs',
                'provedores_dominantes': ['Vivo', 'Claro', 'NET', 'Provedores Locais'],
                'blocos_ipv4_disponiveis': 2,
                'tendencia': 'Piorando - Fibra continua expandindo',
                'alternativas': ['IPv6', 'IP Fixo Premium', 'VPN Corporativa'],
                'custo_solucao': 'R$ 200-300/mês',
                'tempo_implementacao': '2-3 dias',
                'severidade': 'CRÍTICA',
            },
            'Campinas': {
                'cgnat_percent': 94,
                'causa_raiz': 'Hub Tecnológico - Alta Densidade de Startups',
                'provedores_dominantes': ['Vivo', 'Claro', 'NET'],
                'blocos_ipv4_disponiveis': 3,
                'tendencia': 'Piorando rapidamente',
                'alternativas': ['IPv6', 'IP Fixo', 'Multiconexão'],
                'custo_solucao': 'R$ 250-400/mês',
                'tempo_implementacao': '2-3 dias',
                'severidade': 'CRÍTICA',
            },
            'Ribeirão Preto': {
                'cgnat_percent': 91,
                'causa_raiz': 'Expansão de Fibra + Crescimento Urbano',
                'provedores_dominantes': ['Vivo', 'Claro', 'NET'],
                'blocos_ipv4_disponiveis': 5,
                'tendencia': 'Piorando',
                'alternativas': ['IPv6', 'IP Fixo', 'Contrato Corporativo'],
                'custo_solucao': 'R$ 180-280/mês',
                'tempo_implementacao': '1-2 dias',
                'severidade': 'MUITO ALTA',
            },
            'Interior (Outras Cidades)': {
                'cgnat_percent': 85,
                'causa_raiz': 'Saturação Moderada - Mercado em Transição',
                'provedores_dominantes': ['Vivo', 'Claro', 'Provedores Locais'],
                'blocos_ipv4_disponiveis': 10,
                'tendencia': 'Estável',
                'alternativas': ['IP Fixo (viável)', 'IPv6', 'Contrato Corporativo'],
                'custo_solucao': 'R$ 120-200/mês',
                'tempo_implementacao': '1-2 dias',
                'severidade': 'ALTA',
            },
        },
        'RJ': {
            'Rio de Janeiro': {
                'cgnat_percent': 97,
                'causa_raiz': 'Saturação Total + Densidade Urbana',
                'provedores_dominantes': ['Vivo', 'Claro', 'NET', 'Embratel'],
                'blocos_ipv4_disponiveis': 1,
                'tendencia': 'Estável em nível crítico',
                'alternativas': ['IPv6 (recomendado)', 'IP Fixo Premium'],
                'custo_solucao': 'R$ 350-500/mês',
                'tempo_implementacao': '3-5 dias',
                'severidade': 'CRÍTICA',
            },
            'Niterói': {
                'cgnat_percent': 93,
                'causa_raiz': 'Proximidade com Rio + Crescimento',
                'provedores_dominantes': ['Vivo', 'Claro', 'NET'],
                'blocos_ipv4_disponiveis': 4,
                'tendencia': 'Piorando',
                'alternativas': ['IPv6', 'IP Fixo', 'Multiconexão'],
                'custo_solucao': 'R$ 250-350/mês',
                'tempo_implementacao': '2-3 dias',
                'severidade': 'MUITO ALTA',
            },
        },
        'AC': {
            'Rio Branco': {
                'cgnat_percent': 72,
                'causa_raiz': 'Mercado em Estruturação - Infraestrutura Nova',
                'provedores_dominantes': ['Oi', 'Vivo', 'Provedores Locais'],
                'blocos_ipv4_disponiveis': 15,
                'tendencia': 'Melhorando - Infraestrutura nova',
                'alternativas': ['IP Fixo (viável)', 'IPv6', 'Contrato Corporativo'],
                'custo_solucao': 'R$ 80-120/mês',
                'tempo_implementacao': '1-2 dias',
                'severidade': 'MODERADA',
            },
        },
        'AM': {
            'Manaus': {
                'cgnat_percent': 76,
                'causa_raiz': 'Mercado em Crescimento - Provedores Diversos',
                'provedores_dominantes': ['Vivo', 'Claro', 'Oi', 'Provedores Locais'],
                'blocos_ipv4_disponiveis': 12,
                'tendencia': 'Estável',
                'alternativas': ['IP Fixo (viável)', 'IPv6', 'Contrato Corporativo'],
                'custo_solucao': 'R$ 100-150/mês',
                'tempo_implementacao': '1-2 dias',
                'severidade': 'MODERADA',
            },
        },
    }
    
    def __init__(self, estado, cidade):
        self.estado = estado
        self.cidade = cidade
    
    def obter_diagnostico(self):
        """Obtém diagnóstico técnico da localidade"""
        if self.estado in self.BASE_CONHECIMENTO:
            if self.cidade in self.BASE_CONHECIMENTO[self.estado]:
                return self.BASE_CONHECIMENTO[self.estado][self.cidade]
        
        # Fallback: diagnóstico genérico por estado
        return self._diagnostico_generico()
    
    def _diagnostico_generico(self):
        """Diagnóstico genérico quando não há dados específicos"""
        return {
            'cgnat_percent': 80,
            'causa_raiz': 'Dados não disponíveis - Estimativa conservadora',
            'provedores_dominantes': ['Vivo', 'Claro', 'NET', 'Oi'],
            'blocos_ipv4_disponiveis': 8,
            'tendencia': 'Monitorar',
            'alternativas': ['IPv6', 'IP Fixo', 'Contrato Corporativo'],
            'custo_solucao': 'R$ 150-300/mês',
            'tempo_implementacao': '1-3 dias',
            'severidade': 'ALTA',
        }
    
    def gerar_diagnostico_executivo(self):
        """Gera relatório executivo com recomendações técnicas"""
        diag = self.obter_diagnostico()
        
        relatorio = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      DIAGNÓSTICO TÉCNICO REGIONAL - CGNAT                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📍 LOCALIZAÇÃO
   Cidade: {self.cidade}
   Estado: {self.estado}
   Data: {datetime.now().strftime('%d/%m/%Y')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 SITUAÇÃO ATUAL

   CGNAT: {diag['cgnat_percent']}%
   Severidade: {diag['severidade']}
   
   Causa Raiz:
   {diag['causa_raiz']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 INFRAESTRUTURA LOCAL

   Provedores Dominantes:
   {', '.join(diag['provedores_dominantes'])}
   
   Blocos IPv4 Disponíveis: {diag['blocos_ipv4_disponiveis']}
   Tendência: {diag['tendencia']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ SOLUÇÕES VIÁVEIS

   {chr(10).join([f'   • {alt}' for alt in diag['alternativas']])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 INVESTIMENTO E PRAZO

   Custo Estimado: {diag['custo_solucao']}
   Tempo de Implementação: {diag['tempo_implementacao']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 RECOMENDAÇÃO TÉCNICA

{self._gerar_recomendacao(diag)}

╔═══════════════════════════════════════════════════════════════════════════════╗
║                    Próximos Passos: Análise de ROI Detalhada                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        return relatorio
    
    def _gerar_recomendacao(self, diag):
        """Gera recomendação baseada na severidade"""
        severidade = diag['severidade']
        
        recomendacoes = {
            'CRÍTICA': """
   🚨 URGÊNCIA MÁXIMA
   
   O CGNAT em {cidade} atingiu nível crítico ({cgnat}%). A situação é insustentável
   para qualquer negócio que dependa de conectividade estável.
   
   AÇÕES IMEDIATAS:
   1. Implementar IPv6 como solução de curto prazo (2-3 dias)
   2. Contratar IP Fixo Premium para serviços críticos
   3. Avaliar multiconexão como redundância
   
   PRAZO: Implementar em até 1 semana
   """.format(cidade=self.cidade, cgnat=diag['cgnat_percent']),
            
            'MUITO ALTA': """
   ⚠️  ALTA PRIORIDADE
   
   CGNAT em {cidade} está em nível muito alto ({cgnat}%). A implementação de
   solução é recomendada para os próximos 2-3 meses.
   
   AÇÕES RECOMENDADAS:
   1. Avaliar IPv6 como solução principal
   2. IP Fixo para serviços críticos
   3. Planejar transição gradual
   
   PRAZO: Implementar em até 3 meses
   """.format(cidade=self.cidade, cgnat=diag['cgnat_percent']),
            
            'ALTA': """
   ⚡ AÇÃO NECESSÁRIA
   
   CGNAT em {cidade} está em nível alto ({cgnat}%). Recomenda-se planejar
   solução para os próximos 6 meses.
   
   AÇÕES RECOMENDADAS:
   1. Avaliar viabilidade de IP Fixo
   2. Considerar IPv6 como alternativa
   3. Monitorar evolução mensal
   
   PRAZO: Implementar em até 6 meses
   """.format(cidade=self.cidade, cgnat=diag['cgnat_percent']),
            
            'MODERADA': """
   ℹ️  MONITORAR
   
   CGNAT em {cidade} está em nível moderado ({cgnat}%). Situação controlável,
   mas recomenda-se monitoramento contínuo.
   
   AÇÕES RECOMENDADAS:
   1. Monitorar evolução mensal
   2. Avaliar IPv6 como preparação
   3. Reavalie em 12 meses
   
   PRAZO: Reavaliação em 12 meses
   """.format(cidade=self.cidade, cgnat=diag['cgnat_percent']),
        }
        
        return recomendacoes.get(severidade, "Situação desconhecida")
    
    def gerar_diagnostico_json(self):
        """Gera diagnóstico em formato JSON"""
        diag = self.obter_diagnostico()
        
        return {
            'localizacao': {
                'estado': self.estado,
                'cidade': self.cidade,
            },
            'situacao_atual': {
                'cgnat_percent': diag['cgnat_percent'],
                'severidade': diag['severidade'],
                'causa_raiz': diag['causa_raiz'],
                'tendencia': diag['tendencia'],
            },
            'infraestrutura': {
                'provedores_dominantes': diag['provedores_dominantes'],
                'blocos_ipv4_disponiveis': diag['blocos_ipv4_disponiveis'],
            },
            'solucoes': {
                'alternativas': diag['alternativas'],
                'custo_estimado': diag['custo_solucao'],
                'tempo_implementacao': diag['tempo_implementacao'],
            },
            'timestamp': datetime.now().isoformat(),
        }


# Uso
if __name__ == "__main__":
    # Exemplo 1: São Paulo
    diag_sp = DiagnosticoRegional('SP', 'São Paulo')
    print(diag_sp.gerar_diagnostico_executivo())
    
    # Exemplo 2: Bauru
    print("\n" + "="*80 + "\n")
    diag_bauru = DiagnosticoRegional('SP', 'Bauru')
    print(diag_bauru.gerar_diagnostico_executivo())
    
    # Exemplo 3: Rio Branco
    print("\n" + "="*80 + "\n")
    diag_ac = DiagnosticoRegional('AC', 'Rio Branco')
    print(diag_ac.gerar_diagnostico_executivo())
