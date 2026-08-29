"""
Schemas Pydantic v2 para ROI
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class ROIRequest(BaseModel):
    """Schema de requisição para cálculo de ROI"""
    estado: str = Field(..., min_length=2, max_length=2, description="UF do estado")
    cidade: str = Field(..., min_length=1, description="Nome da cidade")
    tipo_cliente: Literal["residencial", "pme", "empresa", "startup"] = Field(
        ..., description="Tipo de cliente"
    )
    receita_anual: Optional[float] = Field(
        None, ge=0, description="Receita anual do cliente"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado": "SP",
                "cidade": "Bauru",
                "tipo_cliente": "pme",
                "receita_anual": 600000.0
            }
        }


class ImpactoFinanceiro(BaseModel):
    """Schema para impacto financeiro atual"""
    perda_downtime: float = Field(..., description="Perda por downtime em R$")
    perda_bloqueios: float = Field(..., description="Perda por bloqueios em R$")
    perda_produtividade: float = Field(..., description="Perda por produtividade em R$")
    perda_total_anual: float = Field(..., description="Perda total anual em R$")
    perda_total_mensal: float = Field(..., description="Perda total mensal em R$")


class SolucaoROI(BaseModel):
    """Schema para solução de ROI"""
    tipo: str = Field(..., description="Tipo de solução")
    custo_mensal: float = Field(..., description="Custo mensal em R$")
    custo_anual: float = Field(..., description="Custo anual em R$")
    economia_anual: float = Field(..., description="Economia anual em R$")
    lucro_anual: float = Field(..., description="Lucro anual líquido em R$")
    roi_percentual: float = Field(..., description="ROI em porcentagem")
    payback_meses: float = Field(..., description="Payback em meses")


class ROIResponse(BaseModel):
    """Schema de resposta completa de ROI"""
    cliente: dict
    impacto_atual: ImpactoFinanceiro
    solucao: SolucaoROI
    recomendacao: str
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente": {
                    "estado": "SP",
                    "cidade": "Bauru",
                    "tipo": "pme",
                    "receita_anual": 600000.0
                },
                "impacto_atual": {
                    "perda_downtime": 60000.0,
                    "perda_bloqueios": 6400.0,
                    "perda_produtividade": 90000.0,
                    "perda_total_anual": 156400.0,
                    "perda_total_mensal": 13033.33
                },
                "solucao": {
                    "tipo": "IP Fixo / IPv6",
                    "custo_mensal": 300.0,
                    "custo_anual": 3600.0,
                    "economia_anual": 125120.0,
                    "lucro_anual": 121520.0,
                    "roi_percentual": 3375.6,
                    "payback_meses": 0.35
                },
                "recomendacao": "ALTAMENTE RECOMENDADO - Payback em menos de 1 mês",
                "timestamp": "2026-01-15T10:30:00"
            }
        }
