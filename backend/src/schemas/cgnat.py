"""
Schemas Pydantic v2 para CGNAT
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CGNATData(BaseModel):
    """Schema para dados de CGNAT por estado"""
    uf: str = Field(..., description="Unidade Federativa", min_length=2, max_length=2)
    estado: str = Field(..., description="Nome do estado")
    cgnat_pct: float = Field(..., ge=0, le=100, description="Porcentagem de CGNAT")
    criticidade: str = Field(..., description="Nível de criticidade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "uf": "SP",
                "estado": "São Paulo",
                "cgnat_pct": 96.0,
                "criticidade": "🟣 Crítica"
            }
        }


class EstadoCriticidade(BaseModel):
    """Schema detalhado de criticidade por estado"""
    uf: str
    estado: str
    cgnat_pct: float
    criticidade: str
    ranking_nacional: Optional[int] = None
    tendencia: str = "Estável"
    recomendacao: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "uf": "SP",
                "estado": "São Paulo",
                "cgnat_pct": 96.0,
                "criticidade": "🟣 Crítica",
                "ranking_nacional": 1,
                "tendencia": "Estável em nível crítico",
                "recomendacao": "Implementar IPv6 urgentemente"
            }
        }


class MetricasNacionais(BaseModel):
    """Schema para métricas nacionais consolidadas"""
    media_nacional: float
    estado_maximo: str
    valor_maximo: float
    total_estados: int
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "media_nacional": 83.4,
                "estado_maximo": "SP",
                "valor_maximo": 96.0,
                "total_estados": 27,
                "timestamp": "2026-01-15T10:30:00"
            }
        }
