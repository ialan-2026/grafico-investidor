import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configurar página em modo super-largo (Fullscreen)
st.set_page_config(page_title="Terminal Solar PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Global - Forçando a Grade de 4 Quadrantes e removendo margens
st.markdown("""
    <style>
    /* Remove padding padrão do Streamlit para ocupar a tela toda */
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    header {visibility: hidden;} /* Esconde o header padrão do Streamlit */
    footer {visibility: hidden;}
    .stApp { background-color: #0b0e14; overflow: hidden; font-family: 'Consolas', monospace; }
    
    /* Layout CSS Grid 2x2 preenchendo 100vh (altura da tela) */
    .tv-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 50vh 45vh; /* Ajustado para deixar espaço para a faixa no topo */
        gap: 2px; /* Apenas um fio de separação entre os blocos, como no TradingView */
        background-color: #2a2e39; /* Cor das "linhas" entre os blocos */
        height: 95vh;
        width: 100vw;
    }
    
    /* Estilo dos painéis (Fundos dos quadrantes) */
    .tv-panel {
        background-color: #131722;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    /* Títulos dentro de cada painel */
    .panel-header {
        background-color: #131722;
        color: #d1d4dc;
        font-size: 0.8rem;
        padding: 5px 10px;
        border-bottom: 1px solid #2a2e39;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
    }
    
    /* Container para os números do quadrante 2 */
    .metrics-container {
        display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;
    }
    .metric-row { text-align: center; margin-bottom: 20px; }
    .m-label { color: #8a919e; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .m-value { font-size: 3rem; font-weight: bold; text-shadow: 0 0 15px rgba(255,255,255,0.1); }
    .c-cyan { color: #00ffcc; }
    .c-pink { color: #ff2a7a; }
    .c-purple { color: #b200ff; }
    </style>
""", unsafe_allow_html=True)

# 3. Faixa Superior (Ticker e Header)
ticker_html = """
<div style="height: 5vh; background-color: #0b0e14; display: flex; align-items: center; border-bottom: 1px solid #2a2e39;">
    <div class="tradingview-widget-container" style="width: 80%;">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {"symbols": [{"proName": "IBOVESPA:IBOV", "title": "Ibovespa"}, {"description": "Dólar", "proName": "FX_IDC:USDBRL"}], "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "br"}
      </script>
    </div>
    <div style="width: 20%; color: #00ffcc; font-size: 0.8rem; font-family: monospace; text-align: right; padding-right: 15px;">
        ● DATAFEED ONLINE
    </div>
</div>
"""
components.html(ticker_html, height=45, margin=0)

# 4. Parâmetros Ocultos (Barra Lateral)
investimento_inicial = st.sidebar.number_input("APORTE (R$)", min_value=100000, value=300000, step=50000)
retorno_realista = st.sidebar.number_input("RECEITA/MÊS (R$)", min_value=1000, value=7000, step=500)
anos_projecao = 10

# Cálculos
meses_totais = anos_projecao * 12
meses_array = np.arange(0, meses_totais + 1)
rentabilidade_mensal = (retorno_realista / investimento_inicial) * 100
payback_meses = investimento_inicial / retorno_realista
caixa_realista = -investimento_inicial + (retorno_realista * meses_array)
taxa_decimal = rentabilidade_mensal / 100
caixa_composto = investimento_inicial * (1 + taxa_decimal)**meses_array

# 5. Criar os Gráficos Plotly
layout_dark = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#8a919e', size=10),
    xaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False), yaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=True, zerolinecolor='#434651'),
    margin=dict(l=30, r=10, t=10, b=20), hovermode='x unified'
)

# Gráfico 1
fig1 = go.Figure()
fig1.add_hline(y=0, line_dash="solid", line_color="#434651", line_width=1)
fig1.add_trace(go.Scatter(x=meses_array, y=caixa_realista, mode='lines', name='Saldo Líquido', line=dict(color='#00ffcc', width=2), fill='tonexty', fillcolor='rgba(0, 255, 204, 0.05)'))
fig1.update_layout(**layout_dark)

# Gráfico 2
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=meses_array, y=(caixa_realista + investimento_inicial), mode='lines', name='Linear', line=dict(color='#ff2a7a', width=1, dash='dot')))
fig2.add_trace(go.Scatter(x=meses_array, y=caixa_composto, mode='lines', name='Exponencial', line=dict(color='#b200ff', width=3), fill='tozeroy', fillcolor='rgba(178, 0, 255, 0.1)'))
fig2.update_layout(**layout_dark)
fig2.update_yaxes(type="log")

# 6. Montar a Grade 2x2 com HTML/CSS Puros para não quebrar
grid_html = f"""
<div class="tv-grid">
    
    <div class="tv-panel">
        <div class="panel-header"><div>🔴 LIVE: PLANTA SOLAR (DIGITAL TWIN)</div></div>
        <div style="flex-grow: 1; overflow: hidden;">
            <iframe width="100%" height="100%" src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&mute=1&loop=1&controls=0&playlist=dQw4w9WgXcQ" frameborder="0" style="pointer-events: none;"></iframe>
        </div>
    </div>

    <div class="tv-panel">
        <div class="panel-header"><div>📊 FUNDAMENTOS DO ATIVO</div></div>
        <div class="metrics-container">
            <div class="metric-row">
                <div class="m-label">Yield Mensal (Rentabilidade)</div>
                <div class="m-value c-cyan">{rentabilidade_mensal:.2f}%</div>
            </div>
            <div class="metric-row">
                <div class="m-label">Break-Even (Payback)</div>
                <div class="m-value c-pink">{int(payback_meses)} Meses</div>
            </div>
            <div class="metric-row">
                <div class="m-label">Projeção Alavancada (10A)</div>
                <div class="m-value c-purple">R$ {caixa_composto[-1]/1000000:.2f}M</div>
            </div>
        </div>
    </div>

    <div class="tv-panel" id="q3">
        <div class="panel-header"><div>📉 CASHFLOW & AMORTIZAÇÃO (BRL)</div></div>
        </div>

    <div class="tv-panel" id="q4">
        <div class="panel-header"><div>🚀 PROJEÇÃO DE ALAVANCAGEM EXPONENCIAL (LOG)</div></div>
        </div>
</div>
"""
st.markdown(grid_html, unsafe_allow_html=True)

# 7. Injetar os gráficos nos quadrantes 3 e 4 via CSS de posicionamento absoluto
st.markdown("""
<style>
/* Força as divs do streamlit a flutuarem sobre os quadrantes de baixo */
div[data-testid="stMainBlockContainer"] > div > div:nth-child(4) { position: absolute; left: 0; bottom: 0; width: 49.5vw; height: 43vh; padding: 10px; z-index: 50; }
div[data-testid="stMainBlockContainer"] > div > div:nth-child(5) { position: absolute; right: 0; bottom: 0; width: 49.5vw; height: 43vh; padding: 10px; z-index: 50; }
</style>
""", unsafe_allow_html=True)

# Renderiza os gráficos. O CSS acima joga o fig1 pra esquerda e o fig2 pra direita
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
