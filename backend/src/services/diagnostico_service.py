"""
Serviço de Diagnóstico Regional - Sentinela Tech
Fornece análise técnica detalhada por região
"""

from typing import List, Optional
from datetime import datetime

from backend.src.schemas.diagnostico import (
    DiagnosticoRequest,
    DiagnosticoResponse,
    SituacaoAtual,
    InfraestruturaLocal,
    SolucoesViaveis,
)


class DiagnosticoService:
    """Serviço para diagnósticos técnicos regionais"""
    
    # Dados de infraestrutura por estado
    _INFRAESTRUTURA_ESTADOS = {
        'SP': {
            'provedores': ['Vivo', 'Claro', 'NET', 'Algar Telecom', 'Provedores Locais'],
            'blocos_ipv4': 2,
            'cgnat_pct': 96.0,
            'causa_raiz': 'Saturação de Fibra (2019-2020) - Polo de ISPs',
        },
        'RJ': {
            'provedores': ['Claro', 'Vivo', 'TIM', 'Provedores Locais'],
            'blocos_ipv4': 3,
            'cgnat_pct': 93.0,
            'causa_raiz': 'Alta densidade populacional + Expansão Fibra',
        },
        'PR': {
            'provedores': ['Vivo', 'Claro', 'Copel Telecom', 'Provedores Locais'],
            'blocos_ipv4': 3,
            'cgnat_pct': 92.0,
            'causa_raiz': 'Forte presença de ISPs regionais',
        },
        'MG': {
            'provedores': ['Vivo', 'Claro', 'Oi', 'Provedores Locais'],
            'blocos_ipv4': 4,
            'cgnat_pct': 90.0,
            'causa_raiz': 'Expansão acelerada de fibra óptica',
        },
        'RS': {
            'provedores': ['Vivo', 'Claro', 'Oi', 'Provedores Locais'],
            'blocos_ipv4': 4,
            'cgnat_pct': 87.0,
            'causa_raiz': 'Crescimento de FTTH em cidades médias',
        },
        'BA': {
            'provedores': ['Vivo', 'Claro', 'Oi', 'Bahia Fibra'],
            'blocos_ipv4': 5,
            'cgnat_pct': 91.0,
            'causa_raiz': 'Expansão de fibra no interior',
        },
        'CE': {
            'provedores': ['Vivo', 'Claro', 'Oi', 'Brisanet'],
            'blocos_ipv4': 4,
            'cgnat_pct': 94.0,
            'causa_raiz': 'Polo regional de ISPs no Nordeste',
        },
        'DF': {
            'provedores': ['Vivo', 'Claro', 'TIM', 'Oi'],
            'blocos_ipv4': 3,
            'cgnat_pct': 89.0,
            'causa_raiz': 'Alta demanda corporativa',
        },
    }
    
    _DEFAULT_INFRA = {
        'provedores': ['Vivo', 'Claro', 'Oi', 'Provedores Locais'],
        'blocos_ipv4': 5,
        'cgnat_pct': 80.0,
        'causa_raiz': 'Expansão nacional de fibra óptica',
    }
    
    def obter_diagnostico(self, estado: str, cidade: str) -> DiagnosticoResponse:
        """
        Obtém diagnóstico técnico detalhado para uma região
        
        Args:
            estado: UF do estado
            cidade: Nome da cidade
            
        Returns:
            DiagnosticoResponse com análise completa da região
        """
        uf_upper = estado.upper()
        
        # Obtém dados do estado ou usa padrão
        infra_data = self._INFRAESTRUTURA_ESTADOS.get(uf_upper, self._DEFAULT_INFRA)
        
        # Determina severidade baseada na porcentagem de CGNAT
        cgnat_pct = infra_data['cgnat_pct']
        severidade = self._classificar_severidade(cgnat_pct)
        
        # Gera tendência
        tendencia = self._gerar_tendencia(cgnat_pct)
        
        # Define soluções viáveis
        solucoes = self._definir_solucoes(cgnat_pct)
        
        # Gera recomendação técnica
        recomendacao = self._gerar_recomendacao(cgnat_pct, severidade)
        
        # Define urgência
        urgencia = self._definir_urgencia(severidade)
        
        return DiagnosticoResponse(
            localizacao={
                'estado': uf_upper,
                'cidade': cidade.title(),
            },
            situacao_atual=SituacaoAtual(
                cgnat_percent=cgnat_pct,
                severidade=severidade,
                causa_raiz=infra_data['causa_raiz'],
                tendencia=tendencia,
            ),
            infraestrutura=InfraestruturaLocal(
                provedores_dominantes=infra_data['provedores'],
                blocos_ipv4_disponiveis=infra_data['blocos_ipv4'],
            ),
            solucoes=solucoes,
            recomendacao_tecnica=recomendacao,
            urgencia=urgencia,
            timestamp=datetime.now(),
        )
    
    def _classificar_severidade(self, cgnat_pct: float) -> str:
        """Classifica severidade baseada na porcentagem de CGNAT"""
        if cgnat_pct >= 95:
            return "CRÍTICA"
        elif cgnat_pct >= 90:
            return "MUITO ALTA"
        elif cgnat_pct >= 85:
            return "ALTA"
        elif cgnat_pct >= 75:
            return "MODERADA"
        else:
            return "BAIXA"
    
    def _gerar_tendencia(self, cgnat_pct: float) -> str:
        """Gera análise de tendência"""
        if cgnat_pct >= 95:
            return "Piorando - Saturação máxima atingida"
        elif cgnat_pct >= 90:
            return "Piorando - Fibra continua expandindo"
        elif cgnat_pct >= 80:
            return "Estável - Monitorar evolução"
        else:
            return "Estável - Baixa pressão de IP"
    
    def _definir_solucoes(self, cgnat_pct: float) -> SolucoesViaveis:
        """Define soluções viáveis baseadas na severidade"""
        if cgnat_pct >= 90:
            return SolucoesViaveis(
                alternativas=['IPv6', 'IP Fixo Premium', 'VPN Corporativa'],
                custo_estimado='R$ 200-300/mês',
                tempo_implementacao='2-3 dias',
            )
        elif cgnat_pct >= 80:
            return SolucoesViaveis(
                alternativas=['IPv6', 'IP Fixo', 'Tunneling'],
                custo_estimado='R$ 150-250/mês',
                tempo_implementacao='3-5 dias',
            )
        else:
            return SolucoesViaveis(
                alternativas=['IPv6 Preventivo', 'Monitoramento'],
                custo_estimado='R$ 100-150/mês',
                tempo_implementacao='5-7 dias',
            )
    
    def _gerar_recomendacao(self, cgnat_pct: float, severidade: str) -> str:
        """Gera recomendação técnica"""
        if severidade in ['CRÍTICA', 'MUITO ALTA']:
            return 'Implementar IPv6 como solução de curto prazo. Avaliar tunneling para redundância.'
        elif severidade == 'ALTA':
            return 'Planejar migração para IPv6. Considerar IP fixo como solução temporária.'
        elif severidade == 'MODERADA':
            return 'Acompanhar evolução do CGNAT. Preparar infraestrutura para IPv6.'
        else:
            return 'Condições favoráveis. Implementar IPv6 preventivamente.'
    
    def _definir_urgencia(self, severidade: str) -> str:
        """Define nível de urgência"""
        if severidade == 'CRÍTICA':
            return 'MÁXIMA - Implementar em até 1 semana'
        elif severidade == 'MUITO ALTA':
            return 'ALTA - Implementar em até 2 semanas'
        elif severidade == 'ALTA':
            return 'MÉDIA - Planejar implementação em 1 mês'
        else:
            return 'BAIXA - Incluir no planejamento estratégico'
