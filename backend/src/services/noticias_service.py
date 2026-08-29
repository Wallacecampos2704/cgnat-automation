"""
Serviço de Notícias - Sentinela Tech
Gerencia notícias do setor de telecomunicações e tecnologia
"""

from typing import List, Optional
from datetime import datetime, timedelta
import random

from backend.src.schemas.diagnostico import NoticiaItem


class NoticiasService:
    """Serviço para busca e gerenciamento de notícias do setor"""
    
    # Banco de notícias simuladas (em produção, isso viria de APIs reais)
    _NOTICIAS_BASE = [
        {
            'titulo': 'Gestão de Acesso: Por que o CGNAT é o maior inimigo da Portaria Remota?',
            'descricao': 'Especialistas alertam para os problemas de conectividade em condomínios devido à saturação de IPs.',
            'fonte': 'Sentinela Tech',
            'categoria': 'SÍNDICOS',
            'dias_atras': 1,
        },
        {
            'titulo': 'Biometria Facial em Condomínios: Como garantir a redundância da conexão',
            'descricao': 'Soluções de backup de link são essenciais para sistemas biométricos críticos.',
            'fonte': 'Portal Condomínio',
            'categoria': 'CONTROLE DE ACESSO',
            'dias_atras': 3,
        },
        {
            'titulo': 'IPv6 se torna obrigatório em novos projetos de CFTV para evitar NAT',
            'descricao': 'Fabricantes de câmeras IP passam a exigir suporte nativo a IPv6 em novas instalações.',
            'fonte': 'Security News',
            'categoria': 'TECNOLOGIA',
            'dias_atras': 5,
        },
        {
            'titulo': 'Ataques a dispositivos IoT em redes residenciais crescem 30% em 2026',
            'descricao': 'Pesquisa aponta aumento significativo de vulnerabilidades em dispositivos conectados.',
            'fonte': 'CyberSec Brasil',
            'categoria': 'SEGURANÇA',
            'dias_atras': 7,
        },
        {
            'titulo': 'Anatel anuncia novas regulamentações sobre IPv6',
            'descricao': 'Agência estabelece cronograma para migração obrigatória de provedores até 2027.',
            'fonte': 'Anatel',
            'categoria': 'REGULAMENTAÇÕES',
            'dias_atras': 2,
        },
        {
            'titulo': 'Provedores de internet aceleram implantação de IPv6 no Brasil',
            'descricao': 'Grandes ISPs brasileiros já possuem mais de 60% de sua rede compatível com IPv6.',
            'fonte': 'Teleco',
            'categoria': 'TECNOLOGIA',
            'dias_atras': 4,
        },
        {
            'titulo': 'Portaria remota falha em 40% dos condomínios por problema de IP',
            'descricao': 'Levantamento mostra que CGNAT é principal causa de chamados técnicos.',
            'fonte': 'Revista Síndico',
            'categoria': 'SÍNDICOS',
            'dias_atras': 6,
        },
        {
            'titulo': 'VPN corporativa: solução ou paliativo para falta de IP público?',
            'descricao': 'Debate entre especialistas divide opiniões sobre melhor abordagem.',
            'fonte': 'TI Inside',
            'categoria': 'TECNOLOGIA',
            'dias_atras': 8,
        },
        {
            'titulo': 'Custo de IP fixo cai 25% no último ano',
            'descricao': 'Concorrência entre operadoras beneficia pequenas e médias empresas.',
            'fonte': 'Canal Telecom',
            'categoria': 'MERCADO',
            'dias_atras': 10,
        },
        {
            'titulo': 'Como dimensionar corretamente a infraestrutura de rede do seu condomínio',
            'descricao': 'Guia completo para síndicos e administradores evitarem problemas de conectividade.',
            'fonte': 'Portal Condomínio',
            'categoria': 'SÍNDICOS',
            'dias_atras': 12,
        },
    ]
    
    def buscar_noticias(
        self,
        categoria: Optional[str] = None,
        limite: int = 10,
    ) -> List[NoticiaItem]:
        """
        Busca notícias do setor
        
        Args:
            categoria: Filtrar por categoria (opcional)
            limite: Quantidade máxima de notícias (1-50)
            
        Returns:
            Lista de NoticiaItem ordenadas por data
        """
        # Limita entre 1 e 50
        limite = max(1, min(limite, 50))
        
        # Filtra por categoria se especificado
        noticias_filtradas = self._NOTICIAS_BASE
        
        if categoria:
            categoria_upper = categoria.upper()
            noticias_filtradas = [
                n for n in self._NOTICIAS_BASE
                if n['categoria'].upper() == categoria_upper
            ]
        
        # Converte para objetos NoticiaItem com datas calculadas
        hoje = datetime.now()
        noticias_items = []
        
        for noticia in noticias_filtradas:
            data_noticia = hoje - timedelta(days=noticia['dias_atras'])
            
            item = NoticiaItem(
                titulo=noticia['titulo'],
                descricao=noticia['descricao'],
                link=f"https://sentinela-tech.com.br/noticias/{self._slugify(noticia['titulo'])}",
                fonte=noticia['fonte'],
                categoria=noticia['categoria'],
                data=data_noticia,
            )
            noticias_items.append(item)
        
        # Ordena por data (mais recente primeiro)
        noticias_items.sort(key=lambda x: x.data, reverse=True)
        
        return noticias_items[:limite]
    
    def _slugify(self, text: str) -> str:
        """Cria slug a partir do título"""
        slug = text.lower()
        slug = slug.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o')
        slug = slug.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        slug = slug.replace('ó', 'o').replace('ú', 'u')
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug
    
    def get_categorias_disponiveis(self) -> List[str]:
        """Retorna lista de categorias disponíveis"""
        categorias = set(n['categoria'] for n in self._NOTICIAS_BASE)
        return sorted(list(categorias))
