"""
Serviço de CGNAT - Sentinela Tech
Gerencia dados de saturação de IP por estado
"""

from typing import List, Optional
from datetime import datetime
from functools import lru_cache

from backend.src.schemas.cgnat import CGNATData, EstadoCriticidade


class CGNATService:
    """Serviço para operações relacionadas ao CGNAT"""
    
    # Dados estáticos dos 27 estados brasileiros
    _DADOS_ESTADOS = {
        'SP': {'estado': 'São Paulo', 'cgnat_pct': 96.0, 'criticidade': '🟣 Crítica'},
        'CE': {'estado': 'Ceará', 'cgnat_pct': 94.0, 'criticidade': '🟣 Crítica'},
        'RJ': {'estado': 'Rio de Janeiro', 'cgnat_pct': 93.0, 'criticidade': '🔴 Muito Alta'},
        'PR': {'estado': 'Paraná', 'cgnat_pct': 92.0, 'criticidade': '🔴 Muito Alta'},
        'MG': {'estado': 'Minas Gerais', 'cgnat_pct': 90.0, 'criticidade': '🔴 Muito Alta'},
        'BA': {'estado': 'Bahia', 'cgnat_pct': 91.0, 'criticidade': '🔴 Muito Alta'},
        'PE': {'estado': 'Pernambuco', 'cgnat_pct': 90.0, 'criticidade': '🔴 Muito Alta'},
        'DF': {'estado': 'Distrito Federal', 'cgnat_pct': 89.0, 'criticidade': '🟠 Alta'},
        'SC': {'estado': 'Santa Catarina', 'cgnat_pct': 88.0, 'criticidade': '🟠 Alta'},
        'RS': {'estado': 'Rio Grande do Sul', 'cgnat_pct': 87.0, 'criticidade': '🟠 Alta'},
        'ES': {'estado': 'Espírito Santo', 'cgnat_pct': 86.0, 'criticidade': '🟠 Alta'},
        'GO': {'estado': 'Goiás', 'cgnat_pct': 85.0, 'criticidade': '🟠 Alta'},
        'PB': {'estado': 'Paraíba', 'cgnat_pct': 84.0, 'criticidade': '🟠 Alta'},
        'RN': {'estado': 'Rio Grande do Norte', 'cgnat_pct': 83.0, 'criticidade': '🟠 Alta'},
        'AL': {'estado': 'Alagoas', 'cgnat_pct': 82.0, 'criticidade': '🟠 Alta'},
        'SE': {'estado': 'Sergipe', 'cgnat_pct': 81.0, 'criticidade': '🟠 Alta'},
        'MT': {'estado': 'Mato Grosso', 'cgnat_pct': 79.0, 'criticidade': '🟡 Moderada'},
        'MS': {'estado': 'Mato Grosso do Sul', 'cgnat_pct': 78.0, 'criticidade': '🟡 Moderada'},
        'MA': {'estado': 'Maranhão', 'cgnat_pct': 79.0, 'criticidade': '🟡 Moderada'},
        'PI': {'estado': 'Piauí', 'cgnat_pct': 78.0, 'criticidade': '🟡 Moderada'},
        'PA': {'estado': 'Pará', 'cgnat_pct': 77.0, 'criticidade': '🟡 Moderada'},
        'AM': {'estado': 'Amazonas', 'cgnat_pct': 76.0, 'criticidade': '🟡 Moderada'},
        'TO': {'estado': 'Tocantins', 'cgnat_pct': 75.0, 'criticidade': '🟡 Moderada'},
        'RO': {'estado': 'Rondônia', 'cgnat_pct': 74.0, 'criticidade': '🟡 Moderada'},
        'AC': {'estado': 'Acre', 'cgnat_pct': 72.0, 'criticidade': '🟢 Baixa'},
        'AP': {'estado': 'Amapá', 'cgnat_pct': 71.0, 'criticidade': '🟢 Baixa'},
        'RR': {'estado': 'Roraima', 'cgnat_pct': 70.0, 'criticidade': '🟢 Baixa'},
    }
    
    _RECOMENDACOES = {
        '🟣 Crítica': 'Implementar IPv6 urgentemente. Soluções de tunneling são essenciais.',
        '🔴 Muito Alta': 'Avaliar migração para IPv6. Considerar IP fixo como solução temporária.',
        '🟠 Alta': 'Planejar transição para IPv6. Monitorar saturação regularmente.',
        '🟡 Moderada': 'Acompanhar evolução do CGNAT. Preparar infraestrutura para IPv6.',
        '🟢 Baixa': 'Condições favoráveis para IPv4. Implementar IPv6 preventivamente.',
    }
    
    def obter_dados_nacionais(self) -> List[CGNATData]:
        """Retorna dados de CGNAT de todos os estados"""
        return [
            CGNATData(
                uf=uf,
                estado=dados['estado'],
                cgnat_pct=dados['cgnat_pct'],
                criticidade=dados['criticidade']
            )
            for uf, dados in self._DADOS_ESTADOS.items()
        ]
    
    def obter_criticidade(self, uf: str) -> Optional[EstadoCriticidade]:
        """Retorna criticidade detalhada de um estado específico"""
        uf_upper = uf.upper()
        
        if uf_upper not in self._DADOS_ESTADOS:
            return None
        
        dados = self._DADOS_ESTADOS[uf_upper]
        dados_estados_list = list(self._DADOS_ESTADOS.items())
        
        # Calcular ranking baseado na porcentagem de CGNAT
        ranking = sorted(
            [(k, v['cgnat_pct']) for k, v in self._DADOS_ESTADOS.items()],
            key=lambda x: x[1],
            reverse=True
        ).index((uf_upper, dados['cgnat_pct'])) + 1
        
        return EstadoCriticidade(
            uf=uf_upper,
            estado=dados['estado'],
            cgnat_pct=dados['cgnat_pct'],
            criticidade=dados['criticidade'],
            ranking_nacional=ranking,
            tendencia=self._get_tendencia(dados['cgnat_pct']),
            recomendacao=self._RECOMENDACOES.get(dados['criticidade'], 'Sem recomendação específica')
        )
    
    def _get_tendencia(self, cgnat_pct: float) -> str:
        """Determina a tendência baseada na porcentagem de CGNAT"""
        if cgnat_pct >= 95:
            return "Estável em nível crítico"
        elif cgnat_pct >= 90:
            return "Em alta - Saturação crescente"
        elif cgnat_pct >= 80:
            return "Estável - Monitorar evolução"
        else:
            return "Baixa pressão de IP"
    
    @classmethod
    def get_media_nacional(cls) -> float:
        """Calcula a média nacional de CGNAT"""
        valores = [d['cgnat_pct'] for d in cls._DADOS_ESTADOS.values()]
        return round(sum(valores) / len(valores), 1)
    
    @classmethod
    def get_estado_maximo(cls) -> tuple[str, float]:
        """Retorna o estado com maior saturação de CGNAT"""
        max_uf = max(cls._DADOS_ESTADOS.keys(), key=lambda x: cls._DADOS_ESTADOS[x]['cgnat_pct'])
        return max_uf, cls._DADOS_ESTADOS[max_uf]['cgnat_pct']
