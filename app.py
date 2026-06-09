import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configurar página em modo super-largo (Fullscreen)
st.set_page_config(page_title="Terminal Solar PRO", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Avançado e Seguro (Garante visual escuro e colado estilo TradingView)
st.markdown("""
    <style>
    /* Forçar preenchimento de tela inteira sem margens bobas */
    .block-container { padding: 0px 15px !important; max-width: 99% !important; margin: 0 auto !important; }
    header { visibility: hidden !important; } 
    footer { visibility: hidden !important; }
    .stApp { background-color: #0c0f16; font-family: 'Consolas', monospace; }
    
    /* Customização das colunas nativas para parecerem painéis do TradingView */
    div[data-testid="stColumn"] {
        background-color: #131722 !important;
        border: 1px solid #2a2e39 !important;
        border-radius: 4px !important;
        padding: 15px !important;
        margin-bottom: 5px !important;
    }
    
    .panel-header {
        color: #787b86;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #2a2e39;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    
    /* Faixa de comando do terminal superior */
    .command-bar {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 15px;
        font-size: 0.75rem;
        color: #787b86;
        margin-bottom: 10px;
    }
    
    /* Layout dos Grandes Números */
    .tv-metric-box { text-align: center; padding: 5px 0; }
    .tv-label { color: #787b86; font-size: 0.85rem; text-transform: uppercase; }
    .tv-value { font-size: 2.3rem; font-weight: bold; margin-top: 2px; }
    
    .neon-green { color: #10b981; text-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
    .neon-blue { color: #3b82f6; text-shadow: 0 0 10px rgba(59, 130, 246, 0.2); }
    .neon-purple { color: #a78bfa; text-shadow: 0 0 10px rgba(167, 139, 250, 0.2); }
    </style>
""", unsafe_allow_html=True)

# 3. Faixa Superior (Ticker de Ações do TradingView Otimizado)
ticker_html = """
<div class="tradingview-widget-container" style="background-color: #0c0f16; overflow: hidden;">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "BMFBOVESPA:IBOV", "title": "IBOVESPA"},
    {"proName": "FX_IDC:USDBRL", "title": "DÓLAR COMERCIAL"},
    {"proName": "BMFBOVESPA:IEE", "title": "ÍNDICE ENERGIA (B3)"},
    {"proName": "AMEX:TAN", "title": "SOLAR ETF GLOBAL"}
  ],
  "showSymbolLogo": true, 
  "colorTheme": "dark", 
  "isTransparent": true, 
  "displayMode": "adaptive", 
  "locale": "br"
}
  </script>
</div>
"""
components.html(ticker_html, height=52)

# --- BARRA DE COMANDO INTEGRADA ---
fuso_brasil = timezone(timedelta(hours=-3))
st.markdown(f"""
    <div class="command-bar">
        <div>❖ SOLAR WEALTH TERMINAL v3.1 // MARKET DATAFEED</div>
        <div>SYS TIME: <b>{datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div style="color: #10b981; font-weight: bold; letter-spacing: 1px;">● CORE SYSTEM ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# 4. Painel Lateral (Inputs da Modelagem Financeira)
st.sidebar.markdown("<h3 style='color:#3b82f6;'>⚙️ MODELAGEM FINANCEIRA</h3>", unsafe_allow_html=True)
perfil = st.sidebar.selectbox("Perfil do Investidor", ["Conservador Escalável", "Agressivo Bimestral", "Customizado"])
aporte_inicial = st.sidebar.number_input("Aporte Inicial Quitado (R$)", value=300000, step=50000)
faturamento_por_usina = st.sidebar.number_input("Faturamento Mensal por Usina (R$)", value=7000, step=500)
custo_parcela_banco = st.sidebar.number_input("Parcela do Financiamento Solar (R$)", value=5000, step=500)
months_projection = st.sidebar.slider("Prazo da Projeção (Meses)", 12, 120, 60, step=12)
pct_retirada = st.sidebar.slider("% de Retirada do Lucro Líquido (Bolso)", 0, 100, 30, step=5) / 100.0

# CORREÇÃO AQUI: Define o valor padrão baseado no perfil, mas mantém o slider sempre visível
if perfil == "Conservador Escalável":
    default_meses = 12
elif perfil == "Agressivo Bimestral":
    default_meses = 2
else:
    default_meses = 6

meses_para_nova_usina = st.sidebar.slider(
    "Frequência de Nova Usina (A cada X meses)", 
    min_value=1, 
    max_value=24, 
    value=default_meses,
    key=f"freq_slider_{perfil}"  # Força o Streamlit a atualizar o valor quando o perfil muda
)

# 5. Lógica da Engenharia Financeira
data = []
caixa_acumulado = 0.0
total_sacado_investidor = 0.0
usinas_ativas = 1

for m in range(1, months_projection + 1):
    if m > 1 and m <= 60 and (m - 1) % meses_para_nova_usina == 0:
        usinas_ativas += 1
        
    parcelas_ativas = 0
    for u in range(1, usinas_ativas):
        mes_compra_usina = 1 + (u * meses_para_nova_usina)
        if m >= mes_compra_usina and m < (mes_compra_usina + 60):
            parcelas_ativas += 1

    faturamento_bruto = usinas_ativas * faturamento_por_usina
    custo_parcelas = parcelas_ativas * custo_parcela_banco
    lucro_liquido_empresa = faturamento_bruto - custo_parcelas
    
    saque_investidor = lucro_liquido_empresa * pct_retirada
    retencao_caixa = lucro_liquido_empresa - saque_investidor
    
    caixa_acumulado += retencao_caixa
    total_sacado_investidor += saque_investidor
    patrimonio_ativos = usinas_ativas * 300000
    
    data.append({
        "Mês": m,
        "Usinas": usinas_ativas,
        "Faturamento Bruto": faturamento_bruto,
        "Parcelas Banco": custo_parcelas,
        "Lucro Líquido": lucro_liquido_empresa,
        "Saque Mensal": saque_investidor,
        "Caixa Acumulado": caixa_acumulado,
        "Patrimônio Usinas": patrimonio_ativos,
        "Valor Total Negócio": caixa_acumulado + patrimonio_ativos
    })

df = pd.DataFrame(data)
retorno_solar_total = df["Valor Total Negócio"].iloc[-1]

# Configuração de Layout Comum para os Gráficos
layout_charts = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#787b86', size=10),
    xaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False),
    margin=dict(l=40, r=10, t=10, b=20), hovermode='x unified'
)

# =================
