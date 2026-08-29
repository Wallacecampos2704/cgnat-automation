"""
Schemas Pydantic v2 para Diagnóstico Regional
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class DiagnosticoRequest(BaseModel):
    """Schema de requisição para diagnóstico regional"""
    estado: str = Field(..., min_length=2, max_length=2, description="UF do estado")
    cidade: str = Field(..., min_length=1, description="Nome da cidade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado": "SP",
                "cidade": "Bauru"
            }
        }


class SituacaoAtual(BaseModel):
    """Schema para situação atual do CGNAT"""
    cgnat_percent: float = Field(..., ge=0, le=100)
    severidade: Literal["CRÍTICA", "MUITO ALTA", "ALTA", "MODERADA", "BAIXA"]
    causa_raiz: str
    tendencia: str


class InfraestruturaLocal(BaseModel):
    """Schema para infraestrutura local"""
    provedores_dominantes: List[str]
    blocos_ipv4_disponiveis: int = Field(..., ge=0)


class SolucoesViaveis(BaseModel):
    """Schema para soluções viáveis"""
    alternativas: List[str]
    custo_estimado: str
    tempo_implementacao: str


class DiagnosticoResponse(BaseModel):
    """Schema de resposta completa de diagnóstico"""
    localizacao: dict
    situacao_atual: SituacaoAtual
    infraestrutura: InfraestruturaLocal
    solucoes: SolucoesViaveis
    recomendacao_tecnica: str
    urgencia: str
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "localizacao": {
                    "estado": "SP",
                    "cidade": "Bauru"
                },
                "situacao_atual": {
                    "cgnat_percent": 96.0,
                    "severidade": "CRÍTICA",
                    "causa_raiz": "Saturação de Fibra (2019-2020) - Polo de ISPs",
                    "tendencia": "Piorando - Fibra continua expandindo"
                },
                "infraestrutura": {
                    "provedores_dominantes": ["Vivo", "Claro", "NET", "Provedores Locais"],
                    "blocos_ipv4_disponiveis": 2
                },
                "solucoes": {
                    "alternativas": ["IPv6", "IP Fixo Premium", "VPN Corporativa"],
                    "custo_estimado": "R$ 200-300/mês",
                    "tempo_implementacao": "2-3 dias"
                },
                "recomendacao_tecnica": "Implementar IPv6 como solução de curto prazo",
                "urgencia": "MÁXIMA - Implementar em até 1 semana",
                "timestamp": "2026-01-15T10:30:00"
            }
        }


class NoticiaItem(BaseModel):
    """Schema para item de notícia"""
    titulo: str
    descricao: str
    link: str
    fonte: str
    categoria: str
    data: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Anatel anuncia novas regulamentações sobre IPv6",
                "descricao": "A Agência Nacional de Telecomunicações publicou novas normas.",
                "link": "https://www.anatel.gov.br",
                "fonte": "Anatel",
                "categoria": "Regulamentações",
                "data": "2026-01-15T10:30:00"
            }
        }
