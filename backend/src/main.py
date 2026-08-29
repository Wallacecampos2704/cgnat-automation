"""
Backend Moderno - Sentinela Tech API
FastAPI + Pydantic v2 + Arquitetura Escalável

Melhorias implementadas:
- Serviços completos com lógica de negócio
- Schemas Pydantic v2 validados
- Endpoints RESTful versionados
- Documentação automática OpenAPI/Swagger
- CORS configurado para produção
- Lifespan events para gerenciamento de recursos
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from contextlib import asynccontextmanager
from typing import List, Optional
import uvicorn

from backend.src.schemas.cgnat import CGNATData, EstadoCriticidade
from backend.src.schemas.roi import ROIRequest, ROIResponse
from backend.src.schemas.diagnostico import DiagnosticoRequest, DiagnosticoResponse, NoticiaItem
from backend.src.services.cgnat_service import CGNATService
from backend.src.services.roi_service import ROIService
from backend.src.services.diagnostico_service import DiagnosticoService
from backend.src.services.noticias_service import NoticiasService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciamento do ciclo de vida da aplicação"""
    # Startup
    print("🚀 Iniciando Sentinela Tech API...")
    print("📊 Carregando dados de CGNAT para 27 estados...")
    print("💰 Serviço de ROI inicializado")
    print("🔍 Diagnóstico regional pronto")
    print("📰 Feed de notícias carregado")
    yield
    # Shutdown
    print("🛑 Encerrando Sentinela Tech API...")


app = FastAPI(
    title="Sentinela Tech API",
    description="""
## API de Inteligência em Conectividade
    
A **Sentinela Tech API** fornece dados e análises sobre:
    
- 📊 **CGNAT**: Saturação de IPs por estado brasileiro
- 💰 **ROI**: Calculadora de retorno sobre investimento em IPv6/IP Fixo
- 🔍 **Diagnóstico Regional**: Análise técnica detalhada por cidade
- 📰 **Notícias**: Feed atualizado do setor de telecomunicações
    
### Tecnologias
- **FastAPI** - Framework moderno e assíncrono
- **Pydantic v2** - Validação de dados de alta performance
- **OpenAPI 3.0** - Documentação automática
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://sentinela-tech.com",
        "https://*.sentinela-tech.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)


@app.get("/", tags=["Health"])
async def root():
    """
    Endpoint de saúde da API
    
    Retorna o status operacional do serviço.
    """
    return {
        "status": "online",
        "message": "Sentinela Tech API v2.0",
        "docs": "/docs",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/cgnat/nacional", response_model=List[CGNATData], tags=["CGNAT"])
async def get_cgnat_nacional(
    uf: Optional[str] = Query(None, description="Filtrar por UF (ex: SP, RJ)")
):
    """
    Obtém dados nacionais de CGNAT por estado
    
    **Retorna** a porcentagem de saturação de IPs e nível de criticidade
    para todos os 27 estados brasileiros ou um estado específico.
    """
    service = CGNATService()
    dados = service.obter_dados_nacionais()
    
    if uf:
        dados = [d for d in dados if d.uf == uf.upper()]
    
    return dados


@app.get("/api/v1/cgnat/criticidade/{uf}", response_model=EstadoCriticidade, tags=["CGNAT"])
async def get_criticidade_estado(uf: str):
    """
    Obtém nível de criticidade de um estado específico
    
    - **uf**: Unidade Federativa (ex: SP, RJ, MG)
    - Retorna ranking nacional, tendência e recomendação técnica
    """
    service = CGNATService()
    resultado = service.obter_criticidade(uf.upper())
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Estado não encontrado")
    
    return resultado


@app.get("/api/v1/cgnat/metricas", tags=["CGNAT"])
async def get_metricas_nacionais():
    """
    Obtém métricas consolidadas do Brasil
    
    Retorna média nacional, estado crítico e timestamp da análise.
    """
    service = CGNATService()
    media = service.get_media_nacional()
    uf_max, valor_max = service.get_estado_maximo()
    
    return {
        "media_nacional": media,
        "estado_maximo": uf_max,
        "valor_maximo": valor_max,
        "total_estados": 27,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/v1/roi/calculadora", response_model=ROIResponse, tags=["ROI"])
async def calcular_roi(request: ROIRequest):
    """
    Calcula ROI para implementação de solução CGNAT/IPv6
    
    **Parâmetros:**
    - **estado**: UF do estado
    - **cidade**: Nome da cidade
    - **tipo_cliente**: residencial | pme | empresa | startup
    - **receita_anual**: Receita anual estimada (opcional)
    
    **Retorna:**
    - Impacto financeiro atual das falhas
    - Custo e economia da solução recomendada
    - ROI percentual e payback em meses
    """
    service = ROIService()
    
    try:
        resultado = service.calcular_roi(
            estado=request.estado,
            cidade=request.cidade,
            tipo_cliente=request.tipo_cliente,
            receita_anual=request.receita_anual
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/diagnostico/regional", response_model=DiagnosticoResponse, tags=["Diagnóstico"])
async def get_diagnostico_regional(request: DiagnosticoRequest):
    """
    Obtém diagnóstico técnico regional detalhado
    
    **Análise inclui:**
    - Situação atual do CGNAT na região
    - Infraestrutura local (provedores, blocos IPv4)
    - Soluções viáveis com custos e prazos
    - Recomendação técnica e urgência
    """
    service = DiagnosticoService()
    
    diagnostico = service.obter_diagnostico(
        estado=request.estado,
        cidade=request.cidade
    )
    
    return diagnostico


@app.get("/api/v1/noticias", tags=["Notícias"])
async def get_noticias(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    limite: int = Query(10, ge=1, le=50, description="Quantidade de notícias (1-50)")
):
    """
    Obtém notícias do setor de telecomunicações
    
    **Categorias disponíveis:**
    - SÍNDICOS
    - CONTROLE DE ACESSO
    - TECNOLOGIA
    - SEGURANÇA
    - REGULAMENTAÇÕES
    - MERCADO
    """
    service = NoticiasService()
    noticias = service.buscar_noticias(categoria=categoria, limite=limite)
    
    return {"noticias": noticias, "total": len(noticias)}


@app.get("/api/v1/noticias/categorias", tags=["Notícias"])
async def get_categorias():
    """Retorna lista de categorias de notícias disponíveis"""
    service = NoticiasService()
    return {"categorias": service.get_categorias_disponiveis()}


if __name__ == "__main__":
    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
