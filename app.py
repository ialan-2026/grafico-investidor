import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configurar página em modo super-largo (Fullscreen)
st.set_page_config(page_title="Terminal Solar PRO", layout="wide", initial_sidebar_state="collapsed")

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
    
    .neon-cyan { color: #00ffcc; text-shadow: 0 0 10px rgba(0, 255, 204, 0.2); }
    .neon-pink { color: #ff2a7a; text-shadow: 0 0 10px rgba(255, 42, 122, 0.2); }
    .neon-purple { color: #b200ff; text-shadow: 0 0 10px rgba(178, 0, 255, 0.2); }
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
# Aumentamos o height para 52 para acabar com os cortes de renderização
components.html(ticker_html, height=52)

# --- NOVA BARRA DE COMANDO INTEGRADA ---
fuso_brasil = timezone(timedelta(hours=-3))
st.markdown(f"""
    <div class="command-bar">
        <div>❖ SOLAR WEALTH TERMINAL v3.1 // MARKET DATAFEED</div>
        <div>SYS TIME: <b>{datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div style="color: #00ffcc; font-weight: bold; letter-spacing: 1px;">● CORE SYSTEM ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# 4. Parâmetros na Barra Lateral (Sidebar)
st.sidebar.markdown("<h3 style='color:#00ffcc;'>⚙️ PARÂMETROS</h3>", unsafe_allow_html=True)
# ... O resto do seu código continua igual daqui para baixo ...
