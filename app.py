import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configuração da Página (Estilo Terminal)
st.set_page_config(page_title="Terminal Solar", layout="wide", initial_sidebar_state="expanded")

# --- WIDGET DA BOLSA DE VALORES ---
ticker_html = """
<div class="tradingview-widget-container" style="background-color: #0b0e14;">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "IBOVESPA:IBOV", "title": "Ibovespa"},
    {"description": "Dólar", "proName": "FX_IDC:USDBRL"},
    {"description": "Bitcoin", "proName": "BINANCE:BTCUSDT"},
    {"description": "Índice de Energia", "proName": "BMFBOVESPA:IEE"}
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
components.html(ticker_html, height=45)

# --- CSS: ESTILO NEON / TRADINGVIEW ---
st.markdown("""
    <style>
    /* Fundo super escuro (espaço profundo) */
    .stApp { background-color: #080a0f; color: #e0e0e0; font-family: 'Consolas', monospace; }
    
    /* Efeito de Borda Neon nos blocos principais */
    .neon-container {
        background-color: #121620;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1), inset 0 0 10px rgba(0, 0, 0, 0.8);
        border: 1px solid #1e2532;
        margin-bottom: 20px;
    }
    
    /* Cards de métricas superiores */
    .metric-card {
        background: linear-gradient(145deg, #131722, #0d1017);
        padding: 15px; 
        border-radius: 6px; 
        text-align: center; 
        border: 1px solid #2a2e39;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    
    .metric-value { font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px currentColor; margin: 5px 0; }
    .metric-label { font-size: 0.85rem; color: #787b86; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Títulos neon */
    h1, h2, h3 { color: #d1d4dc; font-weight: 300; }
    
    /* Header (Sala de comando) */
    .top-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2a2e39; padding-bottom: 5px; margin-bottom: 15px;}
    .status-online {color: #00ffcc; font-size: 0.8rem; font-weight: bold; animation: blinker 2s linear infinite; text-shadow: 0 0 8px #00ffcc;}
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
fuso_brasil = timezone(timedelta(hours=-3))
agora = datetime.now(fuso_brasil)
st.markdown(f"""
    <div class="top-header">
        <div style="font-size: 0.8rem; color: #787b86;">SISTEMA OPERACIONAL SOLAR • <b>{agora.strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div class="status-online">● CONECTADO AOS SERVIDORES</div>
    </div>
""", unsafe_allow_html=True)

# 2. Barra Lateral
st.sidebar.markdown("<h2 style='color:#00ffcc; text-align:center;'>⚙️ SETUP</h2>", unsafe_allow_html=True)
investimento_inicial = st.sidebar.number_input("APORTE INICIAL (R$)", min_value=100000, value=300000, step=50000)
retorno_realista = st.sidebar.number_input("RECEITA/MÊS (R$)", min_value=1000, value=7000, step=500)
anos_projecao = st.sidebar.slider("TIMEFRAME (ANOS)", min_value=5, max_value=25, value=10)

meses_totais = anos_projecao * 12
meses_array = np.arange(0, meses_totais + 1)

# Matemática
rentabilidade_mensal = (retorno_realista / investimento_inicial) * 100
payback_meses = investimento_inicial / retorno_realista
lucro_total = (retorno_realista * meses_totais) - investimento_inicial
caixa_realista = -investimento_inicial + (retorno_realista * meses_array)
taxa_decimal = rentabilidade_mensal / 100
caixa_composto = investimento_inicial * (1 + taxa_decimal)**meses_array

# --- MÉTRICAS SUPERIORES ---
st.markdown("<div class='neon-container'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-card"><div class="metric-label">Rentabilidade Mensal</div><div class="metric-value" style="color:#00ffcc;">{rentabilidade_mensal:.2f}%</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><div class="metric-label">Payback Period</div><div class="metric-value" style="color:#ff2a7a;">{int(payback_meses)} M</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><div class="metric-label">Lucro ({anos_projecao} Anos)</div><div class="metric-value" style="color:#00ffcc;">R$ {lucro_total/1000:.0f}K</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><div class="metric-label">Alavancagem Máx.</div><div class="metric-value" style="color:#b200ff;">R$ {caixa_composto[-1]/1000000:.1f}M</div></div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- LAYOUT EM GRADE (Os dois gráficos lado a lado) ---
st.markdown("<div style='margin-bottom: 10px; color:#787b86; font-size:0.9rem;'>❖ ANÁLISE GRÁFICA DE PERFORMANCE</div>", unsafe_allow_html=True)

col_grafico1, col_grafico2 = st.columns(2)

# Configuração de Tema Padrão para os gráficos Plotly (Fundo escuro, sem grid lines fortes)
layout_dark = dict(
    paper_bgcolor='#131722',
    plot_bgcolor='#131722',
    font=dict(color='#d1d4dc'),
    xaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=True, zerolinecolor='#434651'),
    margin=dict(l=40, r=20, t=40, b=30),
    hovermode='x unified'
)

with col_grafico1:
    st.markdown("<div class='neon-container'>", unsafe_allow_html=True)
    # Gráfico 1: Payback (Estilo Ciano/Azul)
    fig1 = go.Figure()
    
    # Linha zero (Break even)
    fig1.add_hline(y=0, line_dash="solid", line_color="#434651", line_width=2)
    
    # Curva de saldo com preenchimento gradiente simulado
    fig1.add_trace(go.Scatter(
        x=meses_array, y=caixa_realista, 
        mode='lines', name='Saldo Acumulado', 
        line=dict(color='#00ffcc', width=3),
        fill='tonexty', fillcolor='rgba(0, 255, 204, 0.1)'
    ))
    
    fig1.update_layout(**layout_dark, title=dict(text="CASHFLOW & PAYBACK", font=dict(size=14, color='#787b86')), height=400)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_grafico2:
    st.markdown("<div class='neon-container'>", unsafe_allow_html=True)
    # Gráfico 2: Alavancagem (Estilo Rosa/Roxo Neon)
    fig2 = go.Figure()
    
    # Crescimento Linear (Saque mensal)
    fig2.add_trace(go.Scatter(
        x=meses_array, y=(caixa_realista + investimento_inicial), 
        mode='lines', name='Saque (Linear)', 
        line=dict(color='#ff2a7a', width=2, dash='dash')
    ))
    
    # Crescimento Exponencial (Reinvestimento)
    fig2.add_trace(go.Scatter(
        x=meses_array, y=caixa_composto, 
        mode='lines', name='Reinvestimento (Exp.)', 
        line=dict(color='#b200ff', width=4),
        fill='tozeroy', fillcolor='rgba(178, 0, 255, 0.1)'
    ))
    
    fig2.update_layout(**layout_dark, title=dict(text="PROJEÇÃO DE ALAVANCAGEM", font=dict(size=14, color='#787b86')), height=400)
    # Ajustando eixo Y para escala logarítmica para dar aquele visual "pro" de trading
    fig2.update_yaxes(type="log") 
    
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
