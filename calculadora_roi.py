"""
Calculadora de ROI para CGNAT
Transforma dados técnicos em impacto financeiro e proposta de venda
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalculadoraROI:
    """Calcula impacto financeiro do CGNAT e ROI da solução"""
    
    # Tabela de impactos por tipo de cliente
    IMPACTOS_POR_TIPO = {
        'residencial': {
            'downtime_horas_ano': 24,
            'custo_hora': 50,
            'bloqueios_servicos': 3,
            'custo_bloqueio': 400,
            'perda_produtividade_pct': 5,
        },
        'pme': {
            'downtime_horas_ano': 120,
            'custo_hora': 500,
            'bloqueios_servicos': 8,
            'custo_bloqueio': 800,
            'perda_produtividade_pct': 15,
        },
        'empresa': {
            'downtime_horas_ano': 240,
            'custo_hora': 2000,
            'bloqueios_servicos': 15,
            'custo_bloqueio': 1500,
            'perda_produtividade_pct': 25,
        },
        'startup': {
            'downtime_horas_ano': 180,
            'custo_hora': 1200,
            'bloqueios_servicos': 12,
            'custo_bloqueio': 1200,
            'perda_produtividade_pct': 20,
        },
    }
    
    # Tabela de custos de solução por tipo
    CUSTOS_SOLUCAO = {
        'residencial': 150,      # R$/mês
        'pme': 300,              # R$/mês
        'empresa': 800,          # R$/mês
        'startup': 500,          # R$/mês
    }
    
    def __init__(self, estado, cidade, tipo_cliente, receita_anual=None):
        """
        Inicializa a calculadora
        
        Args:
            estado: UF (ex: 'SP')
            cidade: Nome da cidade
            tipo_cliente: 'residencial', 'pme', 'empresa', 'startup'
            receita_anual: Receita anual do cliente (para cálculo de % de perda)
        """
        self.estado = estado
        self.cidade = cidade
        self.tipo_cliente = tipo_cliente
        self.receita_anual = receita_anual or self._receita_padrao(tipo_cliente)
        
        if tipo_cliente not in self.IMPACTOS_POR_TIPO:
            raise ValueError(f"Tipo de cliente inválido: {tipo_cliente}")
    
    def _receita_padrao(self, tipo_cliente):
        """Define receita padrão por tipo de cliente"""
        receitas = {
            'residencial': 3000,
            'pme': 500000,
            'empresa': 5000000,
            'startup': 1000000,
        }
        return receitas.get(tipo_cliente, 0)
    
    def calcular_perda_anual(self):
        """Calcula perda financeira anual causada por CGNAT"""
        impacto = self.IMPACTOS_POR_TIPO[self.tipo_cliente]
        
        # Perda por downtime
        perda_downtime = impacto['downtime_horas_ano'] * impacto['custo_hora']
        
        # Perda por bloqueios de serviço
        perda_bloqueios = impacto['bloqueios_servicos'] * impacto['custo_bloqueio']
        
        # Perda por redução de produtividade
        perda_produtividade = (self.receita_anual * impacto['perda_produtividade_pct']) / 100
        
        perda_total = perda_downtime + perda_bloqueios + perda_produtividade
        
        return {
            'perda_downtime': perda_downtime,
            'perda_bloqueios': perda_bloqueios,
            'perda_produtividade': perda_produtividade,
            'perda_total': perda_total,
            'perda_mensal': perda_total / 12,
        }
    
    def calcular_roi_solucao(self):
        """Calcula ROI da solução (IP Fixo ou IPv6)"""
        perda = self.calcular_perda_anual()
        custo_solucao_mensal = self.CUSTOS_SOLUCAO[self.tipo_cliente]
        custo_solucao_anual = custo_solucao_mensal * 12
        
        # Assumindo que a solução elimina 80% das perdas
        economia_anual = perda['perda_total'] * 0.80
        
        roi = ((economia_anual - custo_solucao_anual) / custo_solucao_anual) * 100
        payback_meses = (custo_solucao_anual / economia_anual) * 12
        
        return {
            'economia_anual': economia_anual,
            'custo_anual': custo_solucao_anual,
            'custo_mensal': custo_solucao_mensal,
            'lucro_anual': economia_anual - custo_solucao_anual,
            'roi_percentual': roi,
            'payback_meses': payback_meses,
        }
    
    def gerar_relatorio_executivo(self):
        """Gera relatório executivo para apresentação ao cliente"""
        perda = self.calcular_perda_anual()
        roi = self.calcular_roi_solucao()
        
        relatorio = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ANÁLISE DE IMPACTO CGNAT - RELATÓRIO EXECUTIVO            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📍 LOCALIZAÇÃO
   Cidade: {self.cidade}, {self.estado}
   Tipo de Cliente: {self.tipo_cliente.upper()}
   Data: {datetime.now().strftime('%d/%m/%Y')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 IMPACTO FINANCEIRO ATUAL (SEM SOLUÇÃO)

   Perda por Downtime:           R$ {perda['perda_downtime']:>12,.2f}
   Perda por Bloqueios:          R$ {perda['perda_bloqueios']:>12,.2f}
   Perda de Produtividade:       R$ {perda['perda_produtividade']:>12,.2f}
   ─────────────────────────────────────────────
   PERDA TOTAL ANUAL:            R$ {perda['perda_total']:>12,.2f}
   
   Média Mensal:                 R$ {perda['perda_mensal']:>12,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 SOLUÇÃO PROPOSTA: IP FIXO / IPv6

   Custo Mensal:                 R$ {roi['custo_mensal']:>12,.2f}
   Custo Anual:                  R$ {roi['custo_anual']:>12,.2f}
   
   Economia Anual (80% redução): R$ {roi['economia_anual']:>12,.2f}
   Lucro Anual Líquido:          R$ {roi['lucro_anual']:>12,.2f}
   
   ✅ ROI: {roi['roi_percentual']:>6.1f}%
   ⏱️  Payback: {roi['payback_meses']:>5.1f} meses

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ANÁLISE COMPARATIVA

   Cenário 1: Manter CGNAT
   • Custo: R$ 0,00/mês
   • Perda: R$ {perda['perda_mensal']:>,.2f}/mês
   • Resultado: -R$ {perda['perda_mensal']:>,.2f}/mês

   Cenário 2: Implementar Solução
   • Custo: R$ {roi['custo_mensal']:>,.2f}/mês
   • Perda: R$ {perda['perda_mensal'] * 0.2:>,.2f}/mês (20% residual)
   • Resultado: +R$ {(roi['economia_anual'] - roi['custo_anual']) / 12:>,.2f}/mês

   💡 Diferença Mensal: R$ {(roi['economia_anual'] - roi['custo_anual']) / 12:>,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 DETALHAMENTO TÉCNICO

   Downtime Estimado: {self.IMPACTOS_POR_TIPO[self.tipo_cliente]['downtime_horas_ano']} horas/ano
   Bloqueios de Serviço: {self.IMPACTOS_POR_TIPO[self.tipo_cliente]['bloqueios_servicos']} ocorrências/ano
   Redução de Produtividade: {self.IMPACTOS_POR_TIPO[self.tipo_cliente]['perda_produtividade_pct']}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RECOMENDAÇÃO

   Com ROI de {roi['roi_percentual']:.1f}% e payback em {roi['payback_meses']:.1f} meses,
   a implementação de IP Fixo/IPv6 é ALTAMENTE RECOMENDADA.
   
   A solução se paga em menos de {int(roi['payback_meses']) + 1} meses e gera economia
   contínua de R$ {roi['lucro_anual']:,.0f} por ano.

╔═══════════════════════════════════════════════════════════════════════════════╗
║                         Próximos Passos: Agende uma Reunião                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        return relatorio
    
    def gerar_relatorio_json(self):
        """Gera relatório em formato JSON para integração com sistemas"""
        perda = self.calcular_perda_anual()
        roi = self.calcular_roi_solucao()
        
        return {
            'cliente': {
                'estado': self.estado,
                'cidade': self.cidade,
                'tipo': self.tipo_cliente,
                'receita_anual': self.receita_anual,
            },
            'impacto_atual': {
                'perda_downtime': perda['perda_downtime'],
                'perda_bloqueios': perda['perda_bloqueios'],
                'perda_produtividade': perda['perda_produtividade'],
                'perda_total_anual': perda['perda_total'],
                'perda_total_mensal': perda['perda_mensal'],
            },
            'solucao': {
                'tipo': 'IP Fixo / IPv6',
                'custo_mensal': roi['custo_mensal'],
                'custo_anual': roi['custo_anual'],
                'economia_anual': roi['economia_anual'],
                'lucro_anual': roi['lucro_anual'],
                'roi_percentual': roi['roi_percentual'],
                'payback_meses': roi['payback_meses'],
            },
            'timestamp': datetime.now().isoformat(),
        }


# Uso
if __name__ == "__main__":
    # Exemplo 1: PME em Bauru
    calc_bauru = CalculadoraROI('SP', 'Bauru', 'pme', receita_anual=600000)
    print(calc_bauru.gerar_relatorio_executivo())
    
    # Exemplo 2: Empresa em São Paulo
    calc_sp = CalculadoraROI('SP', 'São Paulo', 'empresa', receita_anual=10000000)
    print("\n" + "="*80 + "\n")
    print(calc_sp.gerar_relatorio_executivo())
    
    # Exemplo 3: Startup em Rio de Janeiro
    calc_rj = CalculadoraROI('RJ', 'Rio de Janeiro', 'startup', receita_anual=2000000)
    print("\n" + "="*80 + "\n")
    print(calc_rj.gerar_relatorio_executivo())
