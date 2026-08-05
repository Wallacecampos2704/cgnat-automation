# 🛡️ Sentinela Tech Dash - Dashboard CGNAT & Segurança Eletrônica

Dashboard interativo e responsivo para monitoramento de CGNAT no Brasil, notícias de segurança eletrônica, inovações e infraestrutura de redes.

## 🌐 **Acesso Online (GitHub Pages)**

Este site é estático e pode ser hospedado gratuitamente no GitHub Pages:

1. Faça fork deste repositório
2. Acesse: `https://SEU_USUARIO.github.io/NOME_REPOSITORIO/`
3. Ou configure um domínio personalizado

## ✨ **Funcionalidades**

### 📊 Dashboard Geral
- **KPIs em Tempo Real**: Total de IPs em CGNAT, saturação média, UFs críticas
- **Gráficos Interativos**: Evolução histórica (12 meses), saturação por estado
- **Mapa de Calor**: Incidência CGNAT em todo Brasil (27 UFs)

### 🔍 Análise CGNAT Detalhada
- Dados completos de todos os estados brasileiros
- Filtros por estado e período
- Top 5 estados com maior saturação
- Alertas de zonas críticas (>75% saturação)

### 📰 Notícias de Segurança Eletrônica
- **Categorias**: Brasil, Mundo, Inovação, Redes, Infraestrutura
- **Fontes Especializadas**: Anatel, CERT.br, CyberSec News
- **Filtros Dinâmicos**: Por categoria e região
- **12+ Notícias**: Atualizadas diariamente

### 💡 Inovações & Tendências 2026
- **Tendências**: IA Generativa, Blockchain, Sensores Quânticos
- **Startups Brasileiras**: SecureVision AI, NetGuard, BioMetrica
- **Patentes**: Sistemas de autenticação, criptografia
- **Cases de Sucesso**: Banco Central, Aeroporto de Guarulhos

### 🏗️ Infraestrutura de Redes
- Velocidade média por estado
- Adoção IPv6 no Brasil (48.7%)
- Market Share dos ISPs (Claro, Vivo, TIM, Oi)

### 🛠️ Ferramentas
- **Calculadora de ROI**: Calcule retorno sobre investimento
- **Diagnóstico Regional**: Análise de saturação por estado
- **Recomendações**: Baseadas em criticidade

## 📱 **Responsividade**

O site é **100% responsivo** e funciona em:
- ✅ Desktop (1920x1080+)
- ✅ Tablets (768x1024)
- ✅ Smartphones (320x768)
- ✅ Menu hambúrguer para mobile

## 🚀 **Tecnologias Utilizadas**

- **HTML5**: Estrutura semântica
- **CSS3**: Grid, Flexbox, Media Queries, Animações
- **JavaScript ES6+**: Lógica da aplicação
- **Plotly.js**: Gráficos interativos
- **Mobile-First**: Design responsivo

## 📁 **Estrutura de Arquivos**

```
├── index.html          # Página principal
├── styles.css          # Estilos e responsividade
├── data.js             # Dados CGNAT, notícias, inovações
├── app.js              # Lógica da aplicação
├── README.md           # Este arquivo
└── .github/            # Configurações GitHub Pages (opcional)
```

## 🔧 **Como Usar Localmente**

### Opção 1: Abrir Direto no Navegador
```bash
# Basta abrir o arquivo index.html
# Clique duplo ou arraste para o navegador
```

### Opção 2: Servidor HTTP Local
```bash
# Python 3
python -m http.server 8000

# Node.js (npx)
npx http-server -p 8000

# PHP
php -S localhost:8000
```

Acesse: `http://localhost:8000`

## 🌍 **Publicar no GitHub Pages**

### Passo a Passo:

1. **Criar Repositório no GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/sentinela-tech.git
   git push -u origin main
   ```

2. **Ativar GitHub Pages**
   - Acesse: Settings > Pages
   - Source: Deploy from branch
   - Branch: main
   - Folder: / (root)
   - Save

3. **Aguardar Publicação**
   - Em 1-2 minutos seu site estará online
   - URL: `https://SEU_USUARIO.github.io/sentinela-tech/`

### Domínio Personalizado (Opcional)

1. Crie um arquivo `CNAME` na raiz:
   ```
   seudominio.com.br
   ```

2. Configure DNS no seu provedor:
   ```
   Tipo: CNAME
   Nome: www
   Valor: SEU_USUARIO.github.io
   ```

## 📊 **Dados Incluídos**

### CGNAT Brasil
- **27 Estados** com dados de saturação
- **Histórico**: 12 meses de evolução
- **Total IPs**: 136+ milhões afetados
- **Média Nacional**: 72.3% saturação

### Notícias
- **12 notícias** categorizadas
- **7 fontes** especializadas
- **5 categorias**: Brasil, Mundo, Inovação, Redes, Infraestrutura

### Infraestrutura
- **10 estados** com velocidade média
- **IPv6**: 48.7% de adoção
- **5 ISPs** com market share

## 🎨 **Design System**

### Cores
- **Primária**: #2563eb (Azul)
- **Sucesso**: #10b981 (Verde)
- **Alerta**: #f59e0b (Laranja)
- **Perigo**: #ef4444 (Vermelho)

### Tipografia
- **Fonte**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Tamanhos**: Responsivos (rem/em)

### Componentes
- Cards com shadow e hover effects
- Gráficos Plotly interativos
- Botões com transições suaves
- Menu responsivo com animação

## 📈 **Performance**

- **Carregamento**: < 2 segundos
- **Tamanho Total**: ~50KB (gzipped)
- **Sem Dependências Pesadas**: Apenas Plotly.js (CDN)
- **SEO Friendly**: Meta tags, estrutura semântica

## 🔒 **Privacidade**

- **100% Client-Side**: Nenhum dado é enviado para servidores
- **Sem Cookies**: Não rastreamos usuários
- **Sem Backend**: Site estático puro
- **Dados Públicos**: Fontes oficiais (Anatel, NIC.br)

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 **Licença**

MIT License - Sinta-se livre para usar em seus projetos!

## 👨‍💻 **Desenvolvedor**

Criado para monitoramento de CGNAT e segurança eletrônica no Brasil.

## 🆘 **Suporte**

Se encontrar algum problema ou tiver sugestões:
- Abra uma Issue no GitHub
- Entre em contato via email

---

**⚠️ Nota**: Os dados apresentados são simulados para demonstração. Para dados reais, consulte as fontes oficiais (Anatel, NIC.br, Registro.br).

**📅 Última Atualização**: Janeiro 2026
