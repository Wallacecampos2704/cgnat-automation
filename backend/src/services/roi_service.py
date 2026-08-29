"""
Serviço de ROI - Sentinela Tech
Calcula Retorno sobre Investimento para soluções CGNAT/IPv6
"""

from typing import Literal, Optional
from datetime import datetime

from backend.src.schemas.roi import (
    ROIRequest,
    ROIResponse,
    ImpactoFinanceiro,
    SolucaoROI,
)


class ROIService:
    """Serviço para cálculos de ROI relacionados a soluções de conectividade"""
    
    # Fatores de impacto por tipo de cliente
    _IMPACTO_POR_CLIENTE = {
        'residencial': {'downtime_pct': 0.05, 'bloqueios_pct': 0.02, 'produtividade_pct': 0.03},
        'pme': {'downtime_pct': 0.10, 'bloqueios_pct': 0.04, 'produtividade_pct': 0.08},
        'empresa': {'downtime_pct': 0.15, 'bloqueios_pct': 0.06, 'produtividade_pct': 0.12},
        'startup': {'downtime_pct': 0.20, 'bloqueios_pct': 0.08, 'produtividade_pct': 0.15},
    }
    
    # Custos médios de soluções
    _CUSTOS_SOLUCOES = {
        'ip_fixo': {'mensal': 150.0, 'descricao': 'IP Fixo'},
        'ipv6': {'mensal': 100.0, 'descricao': 'IPv6 + Tunneling'},
        'vpn_corp': {'mensal': 300.0, 'descricao': 'VPN Corporativa'},
        'link_dedicado': {'mensal': 800.0, 'descricao': 'Link Dedicado'},
    }
    
    def calcular_roi(
        self,
        estado: str,
        cidade: str,
        tipo_cliente: Literal["residencial", "pme", "empresa", "startup"],
        receita_anual: Optional[float] = None,
    ) -> ROIResponse:
        """
        Calcula ROI para implementação de solução de conectividade
        
        Args:
            estado: UF do estado
            cidade: Nome da cidade
            tipo_cliente: Tipo de cliente (residencial, pme, empresa, startup)
            receita_anual: Receita anual estimada do cliente
            
        Returns:
            ROIResponse com análise completa de ROI
        """
        # Define receita base se não fornecida
        if receita_anual is None:
            receitas_base = {
                'residencial': 60000.0,
                'pme': 600000.0,
                'empresa': 2400000.0,
                'startup': 1200000.0,
            }
            receita_anual = receitas_base.get(tipo_cliente, 600000.0)
        
        # Calcula impactos financeiros atuais
        fatores = self._IMPACTO_POR_CLIENTE[tipo_cliente]
        
        perda_downtime = receita_anual * fatores['downtime_pct']
        perda_bloqueios = receita_anual * fatores['bloqueios_pct']
        perda_produtividade = receita_anual * fatores['produtividade_pct']
        perda_total_anual = perda_downtime + perda_bloqueios + perda_produtividade
        perda_total_mensal = perda_total_anual / 12
        
        impacto_atual = ImpactoFinanceiro(
            perda_downtime=round(perda_downtime, 2),
            perda_bloqueios=round(perda_bloqueios, 2),
            perda_produtividade=round(perda_produtividade, 2),
            perda_total_anual=round(perda_total_anual, 2),
            perda_total_mensal=round(perda_total_mensal, 2),
        )
        
        # Seleciona solução recomendada baseada no tipo de cliente
        solucao_recomendada = self._selecionar_solucao(tipo_cliente)
        custos = self._CUSTOS_SOLUCOES[solucao_recomendada]
        
        custo_mensal = custos['mensal']
        custo_anual = custo_mensal * 12
        
        # Considerando que a solução elimina 80% das perdas
        economia_anual = perda_total_anual * 0.80
        lucro_anual = economia_anual - custo_anual
        roi_percentual = ((lucro_anual / custo_anual) * 100) if custo_anual > 0 else 0
        payback_meses = (custo_anual / economia_anual * 12) if economia_anual > 0 else float('inf')
        
        solucao = SolucaoROI(
            tipo=custos['descricao'],
            custo_mensal=custo_mensal,
            custo_anual=custo_anual,
            economia_anual=round(economia_anual, 2),
            lucro_anual=round(lucro_anual, 2),
            roi_percentual=round(roi_percentual, 2),
            payback_meses=round(payback_meses, 2) if payback_meses != float('inf') else 999.99,
        )
        
        # Gera recomendação
        recomendacao = self._gerar_recomendacao(payback_meses, roi_percentual)
        
        return ROIResponse(
            cliente={
                'estado': estado.upper(),
                'cidade': cidade.title(),
                'tipo': tipo_cliente,
                'receita_anual': receita_anual,
            },
            impacto_atual=impacto_atual,
            solucao=solucao,
            recomendacao=recomendacao,
            timestamp=datetime.now(),
        )
    
    def _selecionar_solucao(self, tipo_cliente: str) -> str:
        """Seleciona a solução mais adequada baseada no tipo de cliente"""
        if tipo_cliente == 'residencial':
            return 'ipv6'
        elif tipo_cliente == 'pme':
            return 'ip_fixo'
        elif tipo_cliente == 'empresa':
            return 'vpn_corp'
        else:  # startup
            return 'ip_fixo'
    
    def _gerar_recomendacao(self, payback_meses: float, roi_percentual: float) -> str:
        """Gera recomendação baseada no ROI calculado"""
        if payback_meses < 1:
            return "ALTAMENTE RECOMENDADO - Payback em menos de 1 mês"
        elif payback_meses < 3:
            return "RECOMENDADO - Payback rápido em menos de 3 meses"
        elif payback_meses < 6:
            return "VIÁVEL - Payback em médio prazo"
        elif roi_percentual > 100:
            return "ANALISAR - ROI positivo mas payback alongado"
        else:
            return "AVALIAR CUSTOS - ROI limitado"
