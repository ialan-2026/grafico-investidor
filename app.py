import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configuração da Página (Estilo Startup)
st.set_page_config(page_title="Usina Solar | Dashboard Premium", layout="wide", initial_sidebar_state="expanded")

# --- WIDGET DA BOLSA DE VALORES (TRADINGVIEW) ---
# Colocamos logo no topo para dar o impacto de plataforma financeira
ticker_html = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "IBOVESPA:IBOV", "title": "Ibovespa"},
    {"description": "Dólar Comercial", "proName": "FX_IDC:USDBRL"},
    {"description": "Bitcoin", "proName": "BINANCE:BTCUSDT"},
    {"description": "Petrobras", "proName": "BMFBOVESPA:PETR4"},
    {"description": "Vale", "proName": "BMFBOVESPA:VALE3"},
    {"description": "S&P 500", "proName": "FOREXCOM:SPXUSD"},
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
components.html(ticker_html, height=50)

# Custom CSS para deixar a interface ainda mais "sexy"
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1, h2, h3 {color: #fca311;}
    .metric-card {
        background-color: #1f2633; padding: 20px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); text-align: center; border-left: 5px solid #fca311;
    }
    .insight-text {font-size: 1.2rem; color: #e5e5e5; font-style: italic;}
    .highlight {color: #2ca02c; font-weight: bold; font-size: 1.4rem;}
    .top-header {display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px;}
    .status-online {color: #00ff00; font-weight: bold; font-size: 0.9rem; animation: blinker 1.5s linear infinite;}
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO COM DATA, HORA E STATUS ---
# Configurando fuso horário para Brasília (UTC-3)
fuso_brasil = timezone(timedelta(hours=-3))
agora = datetime.now(fuso_brasil)
data_hora_formatada = agora.strftime("%d/%m/%Y • %H:%M:%S")

st.markdown(f"""
    <div class="top-header">
        <div style="font-size: 0.9rem; color: #888;">📊 TERMINAL DE RENDIMENTO ENERGÉTICO | <b>{data_hora_formatada}</b></div>
        <div class="status-online">● SISTEMA ONLINE E OPERACIONAL</div>
    </div>
""", unsafe_allow_html=True)

# Título Principal
st.title("☀️ Usina Solar: O Futuro do Rendimento Passivo")
st.markdown("Uma visão interativa, transparente e previsível para o seu capital. Esqueça a volatilidade da bolsa; invista na certeza do sol.")

# 2. Barra Lateral - Parâmetros
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3565/3565609.png", width=80)
st.sidebar.header("⚙️ Parâmetros do Investimento")

investimento_inicial = st.sidebar.number_input("Capital Investido (R$)", min_value=100000, value=300000, step=50000)
retorno_realista = st.sidebar.number_input("Receita Mensal Esperada (R$)", min_value=1000, value=7000, step=500)
anos_projecao = st.sidebar.slider("Anos de Projeção", min_value=5, max_value=25, value=10)

meses_totais = anos_projecao * 12

# Cálculos Base
rentabilidade_mensal = (retorno_realista / investimento_inicial) * 100
payback_meses = investimento_inicial / retorno_realista
lucro_total = (retorno_realista * meses_totais) - investimento_inicial

# 3. Criação de Abas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral do Investimento", "🚀 Alavancagem (Reinvestimento)", "📅 Histórico Mês a Mês", "🌐 Simulador 3D (Planta)"])

with tab1:
    # --- MÉTRICAS DE TOPO ---
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="metric-card"><h4>Rentabilidade ao Mês</h4><h2 style="color:#2ca02c;">{rentabilidade_mensal:.2f}%</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card"><h4>Payback (Retorno)</h4><h2 style="color:#fca311;">{int(payback_meses)} meses</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card"><h4>Lucro Livre ({anos_projecao} anos)</h4><h2 style="color:#2ca02c;">R$ {lucro_total:,.0f}</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-card"><h4>Retorno Total</h4><h2 style="color:#1f77b4;">{((lucro_total+investimento_inicial)/investimento_inicial):.1f}x</h2></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- FRASES DE IMPACTO ---
    st.markdown("### 💡 Inteligência de Mercado")
    cdi_mensal = 0.85 # Estimativa CDI
    multiplicador_cdi = rentabilidade_mensal / cdi_mensal
    
    st.markdown(f"""
    <div class="insight-text">
        Enquanto o mercado tradicional (CDI/Tesouro) briga para entregar 0,85% ao mês, a sua usina atua como uma máquina de infraestrutura, entregando <span class="highlight">{rentabilidade_mensal:.2f}%</span>. <br>
        Isso significa que o seu dinheiro está trabalhando <b>{multiplicador_cdi:.1f} vezes mais rápido</b> do que no banco. A cada R$ 1 investido hoje, o sol devolve R$ {((lucro_total+investimento_inicial)/investimento_inicial):.2f} em {anos_projecao} anos, imune às oscilações da bolsa.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRÁFICO PRINCIPAL COM PLOTLY ---
    meses_array = np.arange(0, meses_totais + 1)
    caixa_realista = -investimento_inicial + (retorno_realista * meses_array)
    caixa_otimista = -investimento_inicial + ((retorno_realista * 1.2) * meses_array)
    caixa_pessimista = -investimento_inicial + ((retorno_realista * 0.8) * meses_array)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=meses_array, y=caixa_otimista, mode='lines', name='+20% Otimista', line=dict(color='#00ff00', width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=meses_array, y=caixa_realista, mode='lines', name='Realista (Base)', line=dict(color='#1f77b4', width=4), fill='tonexty', fillcolor='rgba(31, 119, 180, 0.1)'))
    fig.add_trace(go.Scatter(x=meses_array, y=caixa_pessimista, mode='lines', name='-20% Pessimista', line=dict(color='#ff4b4b', width=2, dash='dot')))
    
    fig.add_hline(y=0, line_dash="solid", line_color="white", line_width=1)
    
    fig.update_layout(
        title='Projeção de Saldo Financeiro Acumulado',
        xaxis_title='Meses de Operação',
        yaxis_title='Saldo (R$)',
        template='plotly_dark',
        hovermode='x unified',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # --- ALAVANCAGEM / JUROS COMPOSTOS ---
    st.markdown("### 🚀 O Poder do Reinvestimento (Alavancagem)")
    st.markdown("E se você não sacar os rendimentos? E se você usar a própria receita da usina para comprar mais painéis e expandir sua capacidade mensalmente? Veja a diferença entre o **Crescimento Linear** e o **Crescimento Exponencial**.")
    
    taxa_decimal = rentabilidade_mensal / 100
    caixa_composto = investimento_inicial * (1 + taxa_decimal)**meses_array
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=meses_array, y=caixa_composto, mode='lines', name='Reinvestimento (Juros Compostos)', line=dict(color='#fca311', width=4)))
    fig_comp.add_trace(go.Scatter(x=meses_array, y=(caixa_realista + investimento_inicial), mode='lines', name='Saque Mensal (Linear)', line=dict(color='#1f77b4', width=2, dash='dash')))
    
    fig_comp.update_layout(title='Linear vs Exponencial (Reinvestindo o Lucro)', xaxis_title='Meses', yaxis_title='Patrimônio Acumulado (R$)', template='plotly_dark', hovermode='x unified', height=450)
    st.plotly_chart(fig_comp, use_container_width=True)

    montante_final = caixa_composto[-1]
    st.success(f"🔥 Se você reinvestir 100% da receita, seus R$ {investimento_inicial:,.0f} se transformam em um patrimônio de **R$ {montante_final:,.0f}** ao final de {anos_projecao} anos!")

with tab3:
    # --- HISTÓRICO MÊS A MÊS ---
    st.markdown("### 📅 Tabela de Fluxo de Caixa")
    df = pd.DataFrame({
        "Mês": meses_array,
        "Aporte/Retorno": [f"R$ {-investimento_inicial:,.2f}" if i == 0 else f"R$ {retorno_realista:,.2f}" for i in meses_array],
        "Saldo Acumulado (R$)": caixa_realista
    })
    df["Saldo Acumulado (R$)"] = df["Saldo Acumulado (R$)"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "_").replace(".", ",").replace("_", "."))
    st.dataframe(df, use_container_width=True, height=400)

with tab4:
    # --- SIMULADOR 3D ---
    st.markdown("### 🌐 Visualização da Planta (Digital Twin)")
    st.markdown("Visualize o seu ativo físico operando em tempo real no espaço digital.")
    
    html_3d = """
    <div style="width: 100%; height: 500px; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
        <iframe src="https://my.spline.design/solarpanel-0a1b2c3d4e5f/" frameborder="0" width="100%" height="100%" style="background-color: #1e1e1e;">
            <h3 style="color: white; text-align: center; margin-top: 20%;">Área reservada para Embed de Modelo 3D da Usina Solar</h3>
        </iframe>
    </div>
    """
    st.components.v1.html(html_3d, height=550)
