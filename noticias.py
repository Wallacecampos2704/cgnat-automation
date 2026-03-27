"""
Módulo de Notícias - Agregador de Múltiplas Fontes
Puxa notícias sobre tecnologia, CGNAT, IPv6 e infraestrutura de internet
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import json
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgregadorNoticias:
    """Agrega notícias de múltiplas fontes sobre tecnologia"""
    
    # Fontes de notícias com suas URLs e seletores CSS
    FONTES = {
        'Canaltech': {
            'url': 'https://canaltech.com.br/tecnologia/',
            'seletor_titulo': 'h2.title',
            'seletor_link': 'a.link',
            'seletor_descricao': 'p.description',
            'categoria': 'Notícias Gerais'
        },
        'Tecnoblog': {
            'url': 'https://tecnoblog.net/',
            'seletor_titulo': 'h2.post-title',
            'seletor_link': 'a.post-link',
            'seletor_descricao': 'p.post-excerpt',
            'categoria': 'Lançamentos'
        },
        'TecMundo': {
            'url': 'https://www.tecmundo.com.br/tecnologia',
            'seletor_titulo': 'h2.title',
            'seletor_link': 'a.article-link',
            'seletor_descricao': 'p.description',
            'categoria': 'Notícias Gerais'
        },
        'Olhar Digital': {
            'url': 'https://olhardigital.com.br/tecnologia/',
            'seletor_titulo': 'h2.title',
            'seletor_link': 'a.link',
            'seletor_descricao': 'p.description',
            'categoria': 'Inovação'
        },
        'TechTudo': {
            'url': 'https://www.techtudo.com.br/noticias/',
            'seletor_titulo': 'h2.title',
            'seletor_link': 'a.link',
            'seletor_descricao': 'p.description',
            'categoria': 'Dicas e Tutoriais'
        },
        'IT Forum': {
            'url': 'https://www.itforum.com.br/',
            'seletor_titulo': 'h2.title',
            'seletor_link': 'a.link',
            'seletor_descricao': 'p.description',
            'categoria': 'TI e Negócios'
        },
        'Itshow': {
            'url': 'https://www.itshow.com.br/',
            'seletor_titulo': 'h2.title',
            'seletor_link': 'a.link',
            'seletor_descricao': 'p.description',
            'categoria': 'TI e Telecomunicações'
        },
    }
    
    # Palavras-chave para filtrar notícias relevantes
    PALAVRAS_CHAVE = [
        'CGNAT', 'IPv6', 'IPv4', 'IP público', 'internet', 'provedor',
        'infraestrutura', 'conectividade', 'banda larga', 'fibra óptica',
        'rede', 'telecomunicações', 'Anatel', 'ISP', 'modem', 'roteador',
        'NAT', 'firewall', 'segurança', 'cibersegurança', 'ataque',
        'tecnologia', 'inovação', 'lançamento', 'startup', 'cloud',
        'servidor', 'dados', 'API', 'programação', 'desenvolvimento'
    ]
    
    def __init__(self):
        self.noticias_cache = []
        self.ultima_atualizacao = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def buscar_noticias_fonte(self, fonte_nome: str) -> List[Dict]:
        """Busca notícias de uma fonte específica"""
        try:
            fonte = self.FONTES.get(fonte_nome)
            if not fonte:
                logger.warning(f"Fonte não encontrada: {fonte_nome}")
                return []
            
            response = requests.get(fonte['url'], headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                logger.error(f"Erro ao acessar {fonte_nome}: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            noticias = []
            
            # Buscar elementos
            titulos = soup.select(fonte['seletor_titulo'])[:10]  # Limitar a 10
            
            for titulo in titulos:
                try:
                    # Extrair informações
                    titulo_texto = titulo.get_text(strip=True)
                    
                    # Procurar link próximo
                    link_elem = titulo.find_parent().find('a')
                    link = link_elem.get('href', '#') if link_elem else '#'
                    
                    # Procurar descrição próxima
                    desc_elem = titulo.find_parent().find('p')
                    descricao = desc_elem.get_text(strip=True)[:150] if desc_elem else ''
                    
                    # Verificar se contém palavras-chave
                    texto_completo = (titulo_texto + ' ' + descricao).lower()
                    tem_palavra_chave = any(palavra.lower() in texto_completo for palavra in self.PALAVRAS_CHAVE)
                    
                    if tem_palavra_chave and titulo_texto:
                        noticia = {
                            'titulo': titulo_texto,
                            'descricao': descricao,
                            'link': link,
                            'fonte': fonte_nome,
                            'categoria': fonte['categoria'],
                            'data': datetime.now().isoformat(),
                        }
                        noticias.append(noticia)
                
                except Exception as e:
                    logger.debug(f"Erro ao processar notícia: {e}")
                    continue
            
            logger.info(f"✅ {fonte_nome}: {len(noticias)} notícias encontradas")
            return noticias
        
        except Exception as e:
            logger.error(f"❌ Erro ao buscar notícias de {fonte_nome}: {e}")
            return []
    
    def buscar_todas_noticias(self) -> List[Dict]:
        """Busca notícias de todas as fontes"""
        logger.info("🔄 Iniciando busca de notícias de todas as fontes...")
        
        todas_noticias = []
        
        for fonte_nome in self.FONTES.keys():
            noticias = self.buscar_noticias_fonte(fonte_nome)
            todas_noticias.extend(noticias)
        
        # Ordenar por data (mais recentes primeiro)
        todas_noticias.sort(key=lambda x: x['data'], reverse=True)
        
        self.noticias_cache = todas_noticias
        self.ultima_atualizacao = datetime.now()
        
        logger.info(f"✅ Total de notícias encontradas: {len(todas_noticias)}")
        return todas_noticias
    
    def filtrar_por_categoria(self, categoria: str) -> List[Dict]:
        """Filtra notícias por categoria"""
        return [n for n in self.noticias_cache if n['categoria'].lower() == categoria.lower()]
    
    def filtrar_por_fonte(self, fonte: str) -> List[Dict]:
        """Filtra notícias por fonte"""
        return [n for n in self.noticias_cache if n['fonte'].lower() == fonte.lower()]
    
    def filtrar_por_palavra_chave(self, palavra: str) -> List[Dict]:
        """Filtra notícias por palavra-chave"""
        palavra_lower = palavra.lower()
        return [
            n for n in self.noticias_cache 
            if palavra_lower in n['titulo'].lower() or palavra_lower in n['descricao'].lower()
        ]
    
    def obter_categorias(self) -> List[str]:
        """Retorna lista de categorias únicas"""
        categorias = set()
        for fonte in self.FONTES.values():
            categorias.add(fonte['categoria'])
        return sorted(list(categorias))
    
    def obter_fontes(self) -> List[str]:
        """Retorna lista de fontes"""
        return sorted(list(self.FONTES.keys()))
    
    def exportar_json(self, filepath: str):
        """Exporta notícias para JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.noticias_cache, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Notícias exportadas para {filepath}")
    
    def gerar_resumo(self) -> Dict:
        """Gera resumo das notícias"""
        categorias = {}
        for noticia in self.noticias_cache:
            cat = noticia['categoria']
            categorias[cat] = categorias.get(cat, 0) + 1
        
        return {
            'total_noticias': len(self.noticias_cache),
            'fontes': len(set(n['fonte'] for n in self.noticias_cache)),
            'categorias': categorias,
            'ultima_atualizacao': self.ultima_atualizacao.isoformat() if self.ultima_atualizacao else None,
        }


# Notícias de exemplo (fallback quando scraping não funciona)
NOTICIAS_EXEMPLO = [
    {
        'titulo': 'Anatel anuncia novas regulamentações sobre IPv6',
        'descricao': 'A Agência Nacional de Telecomunicações publicou novas normas para acelerar a adoção de IPv6 no Brasil.',
        'link': 'https://www.anatel.gov.br',
        'fonte': 'Anatel',
        'categoria': 'Regulamentações',
        'data': datetime.now().isoformat(),
    },
    {
        'titulo': 'CGNAT afeta 80% dos usuários de internet no Brasil',
        'descricao': 'Estudo mostra que a maioria dos provedores brasileiros utiliza CGNAT em suas conexões residenciais.',
        'link': 'https://canaltech.com.br',
        'fonte': 'Canaltech',
        'categoria': 'Notícias Gerais',
        'data': (datetime.now() - timedelta(days=1)).isoformat(),
    },
    {
        'titulo': 'Novo roteador com suporte a IPv6 é lançado no mercado',
        'descricao': 'Fabricante anuncia roteador com suporte completo a IPv6 e CGNAT bypass.',
        'link': 'https://tecnoblog.net',
        'fonte': 'Tecnoblog',
        'categoria': 'Lançamentos',
        'data': (datetime.now() - timedelta(days=2)).isoformat(),
    },
    {
        'titulo': 'Segurança em redes com CGNAT: desafios e soluções',
        'descricao': 'Artigo técnico explora os desafios de segurança ao usar CGNAT e apresenta soluções.',
        'link': 'https://www.itforum.com.br',
        'fonte': 'IT Forum',
        'categoria': 'TI e Negócios',
        'data': (datetime.now() - timedelta(days=3)).isoformat(),
    },
    {
        'titulo': 'Infraestrutura de internet no Brasil melhora em 2026',
        'descricao': 'Relatório mostra aumento na velocidade média e redução de latência em todo o país.',
        'link': 'https://olhardigital.com.br',
        'fonte': 'Olhar Digital',
        'categoria': 'Inovação',
        'data': (datetime.now() - timedelta(days=4)).isoformat(),
    },
]


# Uso
if __name__ == "__main__":
    agregador = AgregadorNoticias()
    
    # Buscar notícias (usar exemplo se scraping falhar)
    try:
        noticias = agregador.buscar_todas_noticias()
        if not noticias:
            noticias = NOTICIAS_EXEMPLO
            agregador.noticias_cache = noticias
    except:
        noticias = NOTICIAS_EXEMPLO
        agregador.noticias_cache = noticias
    
    # Exibir resumo
    resumo = agregador.gerar_resumo()
    print(f"\n✅ Notícias Carregadas")
    print(f"Total: {resumo['total_noticias']}")
    print(f"Fontes: {resumo['fontes']}")
    print(f"Categorias: {resumo['categorias']}")
    
    # Exibir algumas notícias
    print(f"\n📰 Primeiras 5 notícias:")
    for i, noticia in enumerate(noticias[:5], 1):
        print(f"\n{i}. {noticia['titulo']}")
        print(f"   Fonte: {noticia['fonte']} | Categoria: {noticia['categoria']}")
        print(f"   {noticia['descricao'][:80]}...")
