import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configuração da Página (Estilo Terminal em Tela Cheia)
st.set_page_config(page_title="Terminal Solar PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CSS AVANÇADO (Removendo bordas brancas e forçando o Dark Mode) ---
st.markdown("""
    <style>
    /* Remove o espaço em branco no topo e laterais */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
    
    /* Fundo super escuro */
    .stApp { background-color: #0b0e14; color: #d1d4dc; font-family: 'Consolas', monospace; }
    
    /* Caixas estilo TradingView (Painéis) */
    .tv-panel {
        background-color: #131722;
        border-radius: 4px;
        border: 1px solid #2a2e39;
        padding: 10px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        height: 100%;
    }
    
    /* Títulos dos Painéis */
    .panel-title {
        font-size: 0.85rem; color: #787b86; font-weight: bold; margin-bottom: 10px;
        text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #2a2e39; padding-bottom: 5px;
    }
    
    /* Estilo das Métricas */
    .metric-box { background: #1e222d; padding: 15px; border-radius: 4px; margin-bottom: 10px; text-align: center; border-left: 3px solid #2962ff;}
    .metric-value { font-size: 1.6rem; font-weight: bold; margin: 5px 0; text-shadow: 0 0 10px rgba(255,255,255,0.1); }
    .metric-label { font-size: 0.75rem; color: #8a919e; text-transform: uppercase; }
    
    /* Cabeçalho */
    .top-header {display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;}
    .status-online {color: #00ffcc; font-size: 0.8rem; font-weight: bold; animation: blinker 2s linear infinite;}
    @keyframes blinker { 50% { opacity: 0.2; } }
    </style>
""", unsafe_allow_html=True)

# --- WIDGET DA BOLSA DE VALORES ---
ticker_html = """
<div class="tradingview-widget-container" style="background-color: #0b0e14; margin-bottom: -15px;">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [{"proName": "IBOVESPA:IBOV", "title": "Ibovespa"}, {"description": "Dólar", "proName": "FX_IDC:USDBRL"}, {"description": "Bitcoin", "proName": "BINANCE:BTCUSDT"}, {"description": "Índice de Energia", "proName": "BMFBOVESPA:IEE"}],
  "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "br"
  }
  </script>
</div>
"""
components.html(ticker_html, height=45)

# --- CABEÇALHO DO TERMINAL ---
fuso_brasil = timezone(timedelta(hours=-3))
st.markdown(f"""
    <div class="top-header">
        <div style="font-size: 0.85rem; color: #787b86;">❖ TRADINGVIEW SOLAR TERMINAL | <b>{datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div class="status-online">● DATAFEED ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SETUP ESCONDIDO PARA NÃO SUJAR A TELA) ---
st.sidebar.markdown("<h3 style='color:#2962ff;'>⚙️ SETUP DO ATIVO</h3>", unsafe_allow_html=True)
investimento_inicial = st.sidebar.number_input("APORTE (R$)", min_value=100000, value=300000, step=50000)
retorno_realista = st.sidebar.number_input("RECEITA/MÊS (R$)", min_value=1000, value=7000, step=500)
anos_projecao = st.sidebar.slider("TIMEFRAME (ANOS)", min_value=5, max_value=25, value=10)

# --- CÁLCULOS MATEMÁTICOS ---
meses_totais = anos_projecao * 12
meses_array = np.arange(0, meses_totais + 1)
rentabilidade_mensal = (retorno_realista / investimento_inicial) * 100
payback_meses = investimento_inicial / retorno_realista
lucro_total = (retorno_realista * meses_totais) - investimento_inicial
caixa_realista = -investimento_inicial + (retorno_realista * meses_array)
taxa_decimal = rentabilidade_mensal / 100
caixa_composto = investimento_inicial * (1 + taxa_decimal)**meses_array

# ==========================================
# LAYOUT EM GRADE (GRID) - ESTILO TRADINGVIEW
# ==========================================

# LINHA 1: Digital Twin (3D) + Métricas Principais
col_top1, col_top2 = st.columns([2.5, 1]) # O 3D ocupa 70% da tela, as métricas 30%

with col_top1:
    st.markdown("<div class='tv-panel'><div class='panel-title'>🔴 LIVE: DIGITAL TWIN (PROJEÇÃO 3D DA USINA)</div>", unsafe_allow_html=True)
    
    # Aqui entra o seu modelo 3D. Se você tiver um link do Spline ou Sketchfab, coloque no "src"
    # Por enquanto, coloquei um iframe com uma animação de rede neural/tech para simular o painel carregando
    html_3d = """
    <iframe src="https://my.spline.design/solarpanel-0a1b2c3d4e5f/" 
            frameborder="0" width="100%" height="320px" 
            style="background-color: #0b0e14; border-radius: 4px;">
    </iframe>
    """
    components.html(html_3d, height=330)
    st.markdown("</div>", unsafe_allow_html=True)

with col_top2:
    st.markdown("<div class='tv-panel'><div class='panel-title'>📊 DADOS DO ATIVO</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-box" style="border-left-color: #00ffcc;">
            <div class="metric-label">Yield Mensal (Rentabilidade)</div>
            <div class="metric-value" style="color: #00ffcc;">{rentabilidade_mensal:.2f}%</div>
        </div>
        <div class="metric-box" style="border-left-color: #ff2a7a;">
            <div class="metric-label">Break-Even (Payback)</div>
            <div class="metric-value" style="color: #ff2a7a;">{int(payback_meses)} Meses</div>
        </div>
        <div class="metric-box" style="border-left-color: #b200ff;">
            <div class="metric-label">Projeção Alavancada ({anos_projecao}A)</div>
            <div class="metric-value" style="color: #b200ff;">R$ {caixa_composto[-1]/1000000:.2f}M</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# LINHA 2: Gráficos de Payback e Alavancagem Lado a Lado
col_bot1, col_bot2 = st.columns(2)

# Tema Dark padrão para os dois gráficos
layout_dark = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#8a919e', size=10),
    xaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False), yaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=True, zerolinecolor='#434651'),
    margin=dict(l=10, r=10, t=10, b=10), hovermode='x unified'
)

with col_bot1:
    st.markdown("<div class='tv-panel'><div class='panel-title'>📉 CASHFLOW & AMORTIZAÇÃO (BRL)</div>", unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_hline(y=0, line_dash="solid", line_color="#434651", line_width=1)
    fig1.add_trace(go.Scatter(x=meses_array, y=caixa_realista, mode='lines', name='Saldo Líquido', line=dict(color='#00ffcc', width=2), fill='tonexty', fillcolor='rgba(0, 255, 204, 0.05)'))
    fig1.update_layout(**layout_dark, height=280)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_bot2:
    st.markdown("<div class='tv-panel'><div class='panel-title'>🚀 PROJEÇÃO DE ALAVANCAGEM EXPONENCIAL (LOG)</div>", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=meses_array, y=(caixa_realista + investimento_inicial), mode='lines', name='Linear', line=dict(color='#ff2a7a', width=1, dash='dot')))
    fig2.add_trace(go.Scatter(x=meses_array, y=caixa_composto, mode='lines', name='Exponencial', line=dict(color='#b200ff', width=3), fill='tozeroy', fillcolor='rgba(178, 0, 255, 0.1)'))
    fig2.update_layout(**layout_dark, height=280)
    fig2.update_yaxes(type="log") # Escala logarítmica (Visual de Trader)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
