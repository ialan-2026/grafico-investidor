import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import streamlit.components.v1 as components

# 1. Configurar página em modo super-largo (Fullscreen)
st.set_page_config(page_title="Terminal Solar PRO", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Avançado e Seguro (Garante visual escuro e mantém a seta de abrir/fechar o menu ativa)
st.markdown("""
    <style>
    .block-container { padding: 50px 15px 0px 15px !important; max-width: 99% !important; margin: 0 auto !important; }
    
    /* Ajusta o cabeçalho nativo para o tom exato do fundo sem quebrar os botões da barra lateral */
    header[data-testid="stHeader"] { 
        background-color: #0c0f16 !important; 
        height: 50px !important;
    } 
    footer { visibility: hidden !important; }
    .stApp { background-color: #0c0f16; font-family: 'Consolas', monospace; }
    
    /* Estilos das faixas e textos neon */
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
        margin-bottom: 15px;
    }
    .panel-title-bar {
        background-color: #131722;
        color: #787b86;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #2a2e39;
        border-bottom: none;
        border-radius: 4px 4px 0 0;
        padding: 6px 12px;
    }
    .neon-green { color: #10b981; text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
    .neon-blue { color: #3b82f6; text-shadow: 0 0 10px rgba(59, 130, 246, 0.3); }
    .neon-purple { color: #a78bfa; text-shadow: 0 0 10px rgba(167, 139, 250, 0.3); }
    </style>
""", unsafe_allow_html=True)

# 3. Faixa Superior (Letreiro com códigos atualizados em modo REGULAR para Auto Scroll Infinito)
ticker_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0c0f16; overflow: hidden; width: 100vw; }
        .tradingview-widget-container { width: 100% !important; }
    </style>
</head>
<body>
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "FX_IDC:USDBRL", "title": "DÓLAR COMERCIAL"},
    {"proName": "AMEX:TAN", "title": "SOLAR ETF GLOBAL (TAN)"},
    {"proName": "NYSE:NEE", "title": "NEXTERA ENERGY (NEE)"},
    {"proName": "BINANCE:BTCUSDT", "title": "BITCOIN (BTC)"},
    {"proName": "BINANCE:ETHUSDT", "title": "ETHEREUM (ETH)"},
    {"proName": "NASDAQ:TSLA", "title": "TESLA ENERGY (TSLA)"},
    {"proName": "FX:EURUSD", "title": "EURO / DÓLAR"},
    {"proName": "OANDA:XAUUSD", "title": "OURO COMERCIAL"}
  ],
  "showSymbolLogo": true, 
  "colorTheme": "dark", 
  "isTransparent": true, 
  "displayMode": "regular",
  "locale": "br"
}
  </script>
</div>
</body>
</html>
"""
components.html(ticker_html, height=48)

# --- BARRA DE COMANDO INTEGRADA ---
fuso_brasil = timezone(timedelta(hours=-3))
st.markdown(f"""
    <div class="command-bar">
        <div>❖ SANTO HOUSE SOLAR TERMINAL v3.6 // LIVE BENCHMARK ROTATION SYSTEM</div>
        <div>SYS TIME: <b>{datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div style="color: #10b981; font-weight: bold; letter-spacing: 1px;">● CORE SYSTEM ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# 4. Painel Lateral (Configuração com redução e centralização da Logo)
try:
    side_col1, side_col2, side_col3 = st.sidebar.columns([1, 4, 1])
    with side_col2:
        st.image("logo.jpg", use_container_width=True)
except:
    st.sidebar.markdown("<div style='text-align:center; color:#ff4b4b; font-size:0.8rem; margin-bottom:10px;'>⚠️ Faça upload do arquivo logo.jpg no GitHub</div>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color:#3b82f6; text-align:center; margin-top:5px;'>⚙️ MODELAGEM FINANCEIRA</h3>", unsafe_allow_html=True)
perfil = st.sidebar.selectbox("Perfil do Investidor", ["Conservador Escalável", "Agressivo Bimestral", "Customizado"])
aporte_inicial = st.sidebar.number_input("Aporte Inicial Quitado (R$)", value=300000, step=50000)
faturamento_por_usina = st.sidebar.number_input("Faturamento Mensal por Usina (R$)", value=7000, step=500)
custo_parcela_banco = st.sidebar.number_input("Parcela do Financiamento Solar (R$)", value=5000, step=500)
months_projection = st.sidebar.slider("Prazo da Projeção (Meses)", 12, 120, 60, step=12)
pct_retirada = st.sidebar.slider("% de Retirada do Lucro Líquido (Bolso)", 0, 100, 30, step=5) / 100.0

if perfil == "Conservador Escalável":
    meses_para_nova_usina = 12
    st.sidebar.info("ℹ️ Frequência travada em 12 meses para o perfil Conservador.")
elif perfil == "Agressivo Bimestral":
    meses_para_nova_usina = 2
    st.sidebar.info("ℹ️ Frequência travada em 2 meses para o perfil Agressivo.")
else:
    meses_para_nova_usina = st.sidebar.slider("Frequência de Nova Usina (A cada X meses)", 1, 24, 6)

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

# Configuração Padrão das Telas do TradingView (Gráficos)
layout_charts = dict(
    paper_bgcolor='#131722', plot_bgcolor='#131722',
    font=dict(color='#787b86', size=10),
    xaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='#2a2e39', zeroline=False),
    margin=dict(l=45, r=15, t=15, b=25), hovermode='x unified'
)

def render_metric_card(label, value, color_class):
    st.markdown(f"""
        <div style="background-color: #131722; border: 1px solid #2a2e39; border-radius: 4px; padding: 15px; text-align: center;">
            <div style="color: #787b86; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
            <div class="{color_class}" style="font-size: 2rem; font-weight: bold; margin-top: 5px;">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# LINHA 1: METRICAS PRINCIPAIS
# =========================================================
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    render_metric_card("Valor Total do Negócio (Holding)", f"R$ {retorno_solar_total:,.2f}", "neon-green")
with col_m2:
    render_metric_card("Dinheiro Sacado para o Bolso", f"R$ {total_sacado_investidor:,.2f}", "neon-blue")
with col_m3:
    render_metric_card("Total de Usinas Operando", f"{int(df['Usinas'].iloc[-1])} Usinas", "neon-purple")

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# LINHA 2: GRÁFICOS LADO A LADO
# =========================================================
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="panel-title-bar">📈 PAINEL 1: ESCALA PATRIMONIAL (ATIVOS VS LIQUIDEZ)</div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Patrimônio Usinas"], name="Patrimônio Real", line=dict(color="#10B981", width=3), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.03)'))
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Caixa Acumulado"], name="Dinheiro Vivo", line=dict(color="#3B82F6", width=2, dash='dot')))
    fig1.update_layout(**layout_charts, height=260)
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with row2_col2:
    st.markdown('<div class="panel-title-bar">💸 PAINEL 2: FLUXO DE CAIXA MENSAL EM CASCATA</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Faturamento Bruto"], name="Fat. Bruto", line=dict(color="#FBBF24", width=2)))
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Lucro Líquido"], name="Lucro Líq.", line=dict(color="#A78BFA", width=2), fill='tozeroy', fillcolor='rgba(167, 139, 250, 0.03)'))
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Saque Mensal"], name="Seu Saque", line=dict(color="#F43F5E", width=1.5, dash='dash')))
    fig2.update_layout(**layout_charts, height=260)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# LINHA 3: COMPARATIVO MERCADO + TEXTO ESTRATÉGICO
# =========================================================
row3_col1, row3_col2 = st.columns([1.2, 1])

with row3_col1:
    st.markdown('<div class="panel-title-bar">🏛️ PAINEL 3: DESTRUIÇÃO DE ALTERNATIVAS DO MERCADO</div>', unsafe_allow_html=True)
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
        paper_bgcolor='#131722', plot_bgcolor='#131722',
        font=dict(color='#787b86', size=10),
        xaxis=dict(showgrid=True, gridcolor='#2a2e39'),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=15, t=15, b=15), height=160
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

with row3_col2:
    st.markdown('<div class="panel-title-bar">📝 INSIGHT ESTRATÉGICO PARA O PITCH</div>', unsafe_allow_html=True)
    multiplicador = retorno_solar_total / retorno_cdi
    st.markdown(f"""
        <div style="background-color: #131722; border: 1px solid #2a2e39; border-radius: 0 0 4px 4px; padding: 20px; height: 160px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
            Ao adotar a estratégia selecionada, o capital injetado se multiplica de forma geométrica através do efeito cascata. 
            Enquanto as aplicações tradicionais prendem o investidor em uma linha reta corroída pela inflação, o modelo operacional 
            solar entrega um retorno total estimado de <b style="color:#10b981;">{multiplicador:.1f}x maior que o CDI</b>, transformando receita operacional em patrimônio líquido consolidado.
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# LINHA 4: TABELA MÊS A MÊS
# =========================================================
st.markdown('<div class="panel-title-bar">📋 TABELA DE AUDITORIA DO TERMINAL (MÊS A MÊS)</div>', unsafe_allow_html=True)
st.dataframe(df.style.format({
    "Faturamento Bruto": "R$ {:,.2f}",
    "Parcelas Banco": "R$ {:,.2f}",
    "Lucro Líquido": "R$ {:,.2f}",
    "Saque Mensal": "R$ {:,.2f}",
    "Caixa Acumulado": "R$ {:,.2f}",
    "Patrimônio Usinas": "R$ {:,.2f}",
    "Valor Total Negócio": "R$ {:,.2f}"
}), use_container_width=True, height=250)
