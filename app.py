import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configuração da Página (Estilo Terminal em Tela Cheia)
st.set_page_config(page_title="Solar Leverage Terminal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Avançado (Visual Dark Mode Faria Lima / TradingView)
st.markdown("""
    <style>
    .block-container { padding: 0px 15px !important; max-width: 99% !important; margin: 0 auto !important; }
    header { visibility: hidden !important; } 
    footer { visibility: hidden !important; }
    .stApp { background-color: #0c0f16; font-family: 'Consolas', monospace; }
    
    /* Customização dos blocos para parecerem painéis do TradingView */
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
    
    /* Estilo dos blocos de métricas */
    .tv-metric-box { text-align: center; padding: 5px 0; }
    .tv-label { color: #787b86; font-size: 0.8rem; text-transform: uppercase; }
    .tv-value { font-size: 2rem; font-weight: bold; margin-top: 2px; }
    
    .neon-green { color: #10b981; text-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
    .neon-blue { color: #3b82f6; text-shadow: 0 0 10px rgba(59, 130, 246, 0.2); }
    .neon-purple { color: #a78bfa; text-shadow: 0 0 10px rgba(167, 139, 250, 0.2); }
    </style>
""", unsafe_allow_html=True)

# 3. Faixa Superior (Ticker de Ações do TradingView)
ticker_html = """
<div class="tradingview-widget-container" style="background-color: #0c0f16;">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "IBOVESPA:IBOV", "title": "Ibovespa"},
    {"description": "Dólar", "proName": "FX_IDC:USDBRL"},
    {"description": "Índice de Energia", "proName": "BMFBOVESPA:IEE"}
  ],
  "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "br"
}
  </script>
</div>
"""
components.html(ticker_html, height=40)

# --- INFO HEADER ---
fuso_brasil = timezone(timedelta(hours=-3))
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #434651; padding: 0 5px 10px 5px;">
        <div>❖ SOLAR WEALTH & LEVERAGE TERMINAL v3.0 • <b>{datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div style="color: #10b981; font-weight: bold;">● DATA FEED CONECTADO</div>
    </div>
""", unsafe_allow_html=True)

# 4. Painel Lateral (Inputs Ajustados)
st.sidebar.markdown("<h3 style='color:#3b82f6;'>⚙️ MODELAGEM FINANCEIRA</h3>", unsafe_allow_html=True)
perfil = st.sidebar.selectbox("Perfil do Investidor", ["Conservador Escalável", "Agressivo Bimestral", "Customizado"])
aporte_inicial = st.sidebar.number_input("Aporte Inicial Quitado (R$)", value=300000, step=50000)
faturamento_por_usina = st.sidebar.number_input("Faturamento Mensal por Usina (R$)", value=7000, step=500)
custo_parcela_banco = st.sidebar.number_input("Parcela do Financiamento Solar (R$)", value=5000, step=500)
months_projection = st.sidebar.slider("Prazo da Projeção (Meses)", 12, 120, 120, step=12)
pct_retirada = st.sidebar.slider("% de Retirada do Lucro Líquido (Bolso)", 0, 100, 30, step=5) / 100.0

if perfil == "Conservador Escalável":
    meses_para_nova_usina = 12
elif perfil == "Agressivo Bimestral":
    meses_para_nova_usina = 2
else:
    meses_para_nova_usina = st.sidebar.slider("Frequência de Nova Usina (A cada X meses)", 1, 24, 2)

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

# =========================================================
# LINHA 1: MÉTRICAS MAJESTOSAS DE DESEMPENHO DO IMPÉRIO
# =========================================================
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f'<div class="tv-metric-box"><div class="tv-label">Valor Total do Negócio (Holding)</div><div class="tv-value neon-green">R$ {retorno_solar_total:,.2f}</div></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="tv-metric-box"><div class="tv-label">Dinheiro Sacado para o Bolso</div><div class="tv-value neon-blue">R$ {total_sacado_investidor:,.2f}</div></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="tv-metric-box"><div class="tv-label">Total de Usinas Operando</div><div class="tv-value neon-purple">{int(df["Usinas"].iloc[-1])} Usinas</div></div>', unsafe_allow_html=True)

# =========================================================
# LINHA 2: DOIS GRÁFICOS FINANCEIROS EM PARALELO
# =========================================================
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="panel-header">📈 PAINEL 1: ESCALA PATRIMONIAL (ATIVOS VS LIQUIDEZ)</div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Patrimônio Usinas"], name="Patrimônio Real", line=dict(color="#10B981", width=3), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.03)'))
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Caixa Acumulado"], name="Dinheiro Vivo", line=dict(color="#3B82F6", width=2, dash='dot')))
    fig1.update_layout(**layout_charts, height=260)
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with row2_col2:
    st.markdown('<div class="panel-header">💸 PAINEL 2: FLUXO DE CAIXA MENSAL EM CASCATA</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Faturamento Bruto"], name="Fat. Bruto", line=dict(color="#FBBF24", width=2)))
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Lucro Líquido"], name="Lucro Líq.", line=dict(color="#A78BFA", width=2), fill='tozeroy', fillcolor='rgba(167, 139, 250, 0.03)'))
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Saque Mensal"], name="Seu Saque", line=dict(color="#F43F5E", width=1.5, dash='dash')))
    fig2.update_layout(**layout_charts, height=260)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

# =========================================================
# LINHA 3: DESTRUIÇÃO DE ALTERNATIVAS (MARKETING) + DATA
# =========================================================
row3_col1, row3_col2 = st.columns([1.2, 1])

with row3_col1:
    st.markdown('<div class="panel-header">🏛️ PAINEL 3: DESTRUIÇÃO DE ALTERNATIVAS DO MERCADO</div>', unsafe_allow_html=True)
    anos = months_projection / 12.0
    retorno_cdi = aporte_inicial * ((1 + 0.105) ** anos)
    retorno_imovel = aporte_inicial + (aporte_inicial * 0.05 * anos)
    
    fig3 = go.Figure(go.Bar(
        x=[retorno_solar_total, retorno_cdi, retorno_imovel],
        y=["Império Solar", "Renda Fixa (CDI)", "Imóvel Físico"],
        orientation='h',
        marker_color=['#10B981', '#334155', '#1e293b']
    ))
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#787b86', size=10),
        xaxis=dict(showgrid=True, gridcolor='#2a2e39'),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=10, t=10, b=10), height=160
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

with row3_col2:
    st.markdown('<div class="panel-header">📝 INSIGHT ESTRATÉGICO PARA O PITCH</div>', unsafe_allow_html=True)
    multiplicador = retorno_solar_total / retorno_cdi
    st.markdown(f"""
    <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.4; padding: 5px;">
        Ao adotar o perfil <b style="color:#3b82f6;">{perfil}</b>, o capital injetado se multiplica de forma geométrica. 
        Enquanto o banco transforma o dinheiro do investidor em uma linha reta previsível e corroída pela inflação, 
        a engenharia em cascata solar gera um retorno total estimado de <b style="color:#10b981;">{multiplicador:.1f}x maior que o CDI</b> no mesmo período.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# LINHA 4: TABELA DE AUDITORIA DO TERMINAL
# =========================================================
st.markdown('<div class="panel-header">📋 TABELA DE AUDITORIA DO TERMINAL (MÊS A MÊS)</div>', unsafe_allow_html=True)
st.dataframe(df.style.format({
    "Faturamento Bruto": "R$ {:,.2f}",
    "Parcelas Banco": "R$ {:,.2f}",
    "Lucro Líquido": "R$ {:,.2f}",
    "Saque Mensal": "R$ {:,.2f}",
    "Caixa Acumulado": "R$ {:,.2f}",
    "Patrimônio Usinas": "R$ {:,.2f}",
    "Valor Total Negócio": "R$ {:,.2f}"
}), use_container_width=True, height=250)
