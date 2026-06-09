import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

# 1. Configurar página em modo super-largo (Fullscreen)
st.set_page_config(page_title="Terminal Solar PRO", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Avançado e Seguro (Garante visual escuro e o recuo correto para os cards)
st.markdown("""
    <style>
    .block-container { padding: 80px 15px 0px 15px !important; max-width: 99% !important; margin: 0 auto !important; }
    
    /* Ajusta o cabeçalho nativo para o tom exato do fundo sem quebrar os botões da barra lateral */
    header[data-testid="stHeader"] { 
        background-color: #0c0f16 !important; 
        height: 50px !important;
    } 
    footer { visibility: hidden !important; }
    .stApp { background-color: #0c0f16; font-family: 'Consolas', monospace; }
    
    /* Design do Cabeçalho Financeiro Proprietário */
    .market-header-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 12px;
        width: 100%;
    }
    .market-card {
        flex: 1;
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 4px;
        padding: 10px 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .market-label {
        color: #787b86;
        font-size: 0.72rem;
        font-weight: bold;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .market-value {
        color: #cbd5e1;
        font-size: 0.9rem;
        font-weight: bold;
    }
    
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

# 3. CABEÇALHO PROPRIETÁRIO SANTO HOUSE
st.markdown("""
    <div class="market-header-container">
        <div class="market-card">
            <div class="market-label">💵 DÓLAR COMERCIAL</div>
            <div class="market-value">5,1783 <span style="color: #f43f5e; font-size: 0.75rem; margin-left: 5px;">-0,28% ▼</span></div>
        </div>
        <div class="market-card">
            <div class="market-label">☀️ SOLAR INDEX GLOBAL (TAN)</div>
            <div class="market-value">61,02 USD <span style="color: #f43f5e; font-size: 0.75rem; margin-left: 5px;">-4,03% ▼</span></div>
        </div>
        <div class="market-card">
            <div class="market-label">⚡ NEXTERA ENERGY (NEE)</div>
            <div class="market-value">84,42 USD <span style="color: #10b981; font-size: 0.75rem; margin-left: 5px;">+0,49% ▲</span></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- BARRA DE COMANDO INTEGRADA ---
fuso_brasil = timezone(timedelta(hours=-3))
st.markdown(f"""
    <div class="command-bar">
        <div>❖ SANTO HOUSE SOLAR TERMINAL v4.1 // SEASONAL PERFORMANCE ENGINE</div>
        <div>SYS TIME: <b>{datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")}</b></div>
        <div style="color: #10b981; font-weight: bold; letter-spacing: 1px;">● CORE SYSTEM ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# 4. Painel Lateral (Configuração de Inputs e Estratégia de Caixa)
try:
    side_col1, side_col2, side_col3 = st.sidebar.columns([1, 4, 1])
    with side_col2:
        st.image("logo.jpg", use_container_width=True)
except:
    st.sidebar.markdown("<div style='text-align:center; color:#ff4b4b; font-size:0.8rem; margin-bottom:10px;'>⚠️ Faça upload do arquivo logo.jpg no GitHub</div>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color:#3b82f6; text-align:center; margin-top:5px;'>⚙️ MODELAGEM FINANCEIRA</h3>", unsafe_allow_html=True)

perfil = st.sidebar.selectbox(
    "Perfil do Investidor", 
    ["Conservador Escalável", "Agressivo Bimestral", "Customizado"]
)

aporte_inicial = st.sidebar.number_input("Aporte Inicial Quitado (R$)", value=240000, step=10000)
faturamento_por_usina = st.sidebar.number_input("Faturamento Mensal Inicial por Usina (R$)", value=6000, step=500)
custo_parcela_banco = st.sidebar.number_input("Parcela do Financiamento Solar (R$)", value=5000, step=500)

st.sidebar.markdown("---")
st.sidebar.metric(label="📈 Rendimento Base Combinado", value="2,33% ao mês", delta="Garantido no Repasse")

months_projection = st.sidebar.slider("Prazo da Projeção (Meses)", 12, 300, 60, step=12)
pct_retirada = st.sidebar.slider("% de Retirada do Lucro Líquido (Bolso)", 0, 100, 30, step=5) / 100.0
taxa_admin_pct = st.sidebar.slider("Taxa de O&M / Adm Santo House (%)", 0, 20, 0, step=1) / 100.0

# Seletor de Estratégia Reativa
st.sidebar.markdown("---")
st.sidebar.markdown("<h4 style='color:#cbd5e1; margin-bottom: 2px;'>🎯 Alocação do Caixa</h4>", unsafe_allow_html=True)
estrategia_caixa = st.sidebar.radio(
    "O que fazer com os 70% retidos?",
    ["Acumular em Caixa Vivo (CDI)", "Quitação Acelerada (Abater Bancos)"]
)

# Mapeamento do ritmo com a Chave de Seleção (Toggle)
expandir_usinas = True
if "Conservador" in perfil:
    meses_para_nova_usina = 12
    max_usinas = 999
elif "Agressivo" in perfil:
    meses_para_nova_usina = 2
    max_usinas = 999
else:
    st.sidebar.markdown("---")
    ativar_expansao = st.sidebar.toggle("Ativar Novas Expansões", value=True)
    if ativar_expansao:
        meses_para_nova_usina = st.sidebar.slider("Frequência de Nova Usina (A cada X meses)", 1, 24, 6)
        max_usinas = st.sidebar.slider("Quantidade Máxima Total de Usinas", 1, 30, 5)
    else:
        expandir_usinas = False
        meses_para_nova_usina = 999
        max_usinas = 1

# --- DEFINIÇÃO DA SAZONALIDADE SOLAR DO BRASIL ---
sazonalidade_mes = {
    1: 1.00, 2: 0.95, 3: 0.98, 4: 0.90, 
    5: 0.85, 6: 0.80, 7: 0.88, 
    8: 1.20, 9: 1.25, 10: 1.15, 
    11: 1.05, 12: 1.02
}

# 5. MOTOR DE CÁLCULO CORE REVISADO (CONTRATOS DE CICLO FECHADO SEM INFLAÇÃO INTERNA)
data = []
caixa_acumulado = 0.0
total_sacado_investidor = 0.0
usinas_ativas = 1
financiamentos = {}
id_usina_atual = 1
faturamento_dinamico_base = faturamento_por_usina

for m in range(1, months_projection + 1):
    
    # Identifica o mês do ano corrente (1 a 12) para aplicar o fator de irradiação
    mes_do_ano = ((m - 1) % 12) + 1
    fator_solar = sazonalidade_mes[mes_do_ano]
    
    # Aplica o fator de sazonalidade sobre o valor fixado em contrato
    faturamento_reajustado_usina = faturamento_dinamico_base * fator_solar

    # Gatilho condicional de expansão patrimonial
    if expandir_usinas and m > 1 and m <= 60 and (m - 1) % meses_para_nova_usina == 0:
        if usinas_ativas < max_usinas:
            usinas_ativas += 1
            id_usina_atual += 1
            financiamentos[id_usina_atual] = {
                "parcelas_restantes": 60,
                "primeiras_12_pagas": False,
                "meses_sem_pagar": 0
            }

    # SISTEMA DE AMORTIZAÇÃO ANTECIPADA POR LOTES MENSAL (FLEXÍVEL)
    if estrategia_caixa == "Quitação Acelerada (Abater Bancos)":
        for id_u in sorted(financiamentos.keys()):
            if not financiamentos[id_u]["primeiras_12_pagas"] and financiamentos[id_u]["parcelas_restantes"] >= 12:
                custo_12_parcelas_antecipadas = 12 * (custo_parcela_banco * 0.85)
                
                if caixa_acumulado >= custo_12_parcelas_antecipadas:
                    caixa_acumulado -= custo_12_parcelas_antecipadas
                    financiamentos[id_u]["primeiras_12_pagas"] = True
                    financiamentos[id_u]["parcelas_restantes"] -= 12
                    financiamentos[id_u]["meses_sem_pagar"] = 12 
                    break 

    # Varredura do custo real de boletos bancários ativos no mês
    parcelas_ativas_no_mes = 0
    for id_u in financiamentos.keys():
        if financiamentos[id_u]["parcelas_restantes"] > 0:
            if financiamentos[id_u]["primeiras_12_pagas"] and financiamentos[id_u]["meses_sem_pagar"] > 0:
                parcelas_ativas_no_mes += 0 
            else:
                parcelas_ativas_no_mes += 1

    # MATEMÁTICA OPERACIONAL AJUSTADA COM SAZONALIDADE E TAXA ADM
    faturamento_bruto_visivel = usinas_ativas * faturamento_reajustado_usina
    faturamento_santo_house = faturamento_bruto_visivel * taxa_admin_pct
    faturamento_liquido_holding = faturamento_bruto_visivel - faturamento_santo_house
    custo_parcelas = parcelas_ativas_no_mes * custo_parcela_banco
    lucro_liquido_empresa = faturamento_liquido_holding - custo_parcelas
    
    saque_investidor = lucro_liquido_empresa * pct_retirada
    retencao_caixa = lucro_liquido_empresa - saque_investidor
    
    caixa_acumulado += retencao_caixa
    total_sacado_investidor += saque_investidor

    # CÁLCULO DA TAXA DE RENDIMENTO REAL DINÂMICA
    capital_proporcional = usinas_ativas * aporte_inicial
    taxa_rendimento_mes = (lucro_liquido_empresa / capital_proporcional) * 100 if capital_proporcional > 0 else 0

    # Consumo do tempo de carência e dos contratos paralelos
    for id_u in financiamentos.keys():
        if financiamentos[id_u]["primeiras_12_pagas"] and financiamentos[id_u]["meses_sem_pagar"] > 0:
            financiamentos[id_u]["meses_sem_pagar"] -= 1 
        elif financiamentos[id_u]["parcelas_restantes"] > 0:
            financiamentos[id_u]["parcelas_restantes"] -= 1 

    patrimonio_ativos = usinas_ativas * aporte_inicial
    valor_total_holding = caixa_acumulado + patrimonio_ativos

    # Alimentação da matriz com a nova coluna tratada como string
    data.append({
        "Mês": m,
        "Usinas": usinas_ativas,
        "Faturamento Bruto": faturamento_bruto_visivel,
        "Parcelas Banco": custo_parcelas,
        "Lucro Líquido": lucro_liquido_empresa,
        "Rendimento Mensal (%)": f"{taxa_rendimento_mes:.2f}%",
        "Saque Mensal": saque_investidor,
        "Caixa Acumulado": caixa_acumulado,
        "Patrimônio Usinas": patrimonio_ativos,
        "Valor Total Negócio": valor_total_holding
    })

df = pd.DataFrame(data)
retorno_solar_total = df["Valor Total Negócio"].iloc[-1]

# CÁLCULO DE ROI DO PAINEL 3 REALISTA (JUROS COMPOSTOS DE MERCADO LONGO PRAZO)
anos_totais = months_projection / 12.0
taxa_cdi_anual = 0.095
retorno_cdi_final = aporte_inicial * ((1 + taxa_cdi_anual) ** anos_totais)
retorno_imovel_final = aporte_inicial * ((1 + 0.08) ** anos_totais)

# Configuração Padrão de Design Gráfico (Estilo TradingView)
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

# --- LINHA 1: METRICAS PRINCIPAIS ---
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    render_metric_card("Valor Total do Negócio (Holding)", f"R$ {retorno_solar_total:,.2f}", "neon-green")
with col_m2:
    render_metric_card("Dinheiro Sacado para o Bolso", f"R$ {total_sacado_investidor:,.2f}", "neon-blue")
with col_m3:
    render_metric_card("Total de Usinas Operando", f"{int(df['Usinas'].iloc[-1])} Usinas", "neon-purple")

st.markdown("<br>", unsafe_allow_html=True)

# --- LINHA 2: RENDIMENTOS GRÁFICOS ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("""<div class="panel-title-bar">📈 PAINEL 1: ESCALA PATRIMONIAL (ATIVOS VS LIQUIDEZ VS HOLDING)</div>""", unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Patrimônio Usinas"], name="Patrimônio Real", line=dict(color="#10B981", width=3), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.03)'))
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Caixa Acumulado"], name="Dinheiro Vivo", line=dict(color="#3B82F6", width=2, dash='dot')))
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Valor Total Negócio"], name="Valor da Holding", line=dict(color="#FF9F43", width=3)))
    fig1.update_layout(**layout_charts, height=260)
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with row2_col2:
    st.markdown("""<div class="panel-title-bar">💸 PAINEL 2: FLUXO DE CAIXA MENSAL EM CASCATA</div>""", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Faturamento Bruto"], name="Fat. Bruto", line=dict(color="#FBBF24", width=2)))
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Lucro Líquido"], name="Lucro Líq.", line=dict(color="#A78BFA", width=2), fill='tozeroy', fillcolor='rgba(167, 139, 250, 0.03)'))
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Saque Mensal"], name="Seu Saque", line=dict(color="#F43F5E", width=1.5, dash='dash')))
    fig2.update_layout(**layout_charts, height=260)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br>", unsafe_allow_html=True)

# --- LINHA 3: COMPARATIVO EM JUROS COMPOSTOS E INSIGHTS ---
row3_col1, row3_col2 = st.columns([1.2, 1])

with row3_col1:
    st.markdown("""<div class="panel-title-bar">🏛️ PAINEL 3: DESTRUIÇÃO DE ALTERNATIVAS DO MERCADO</div>""", unsafe_allow_html=True)
    fig3 = go.Figure(go.Bar(
        x=[retorno_solar_total, retorno_cdi_final, retorno_imovel_final],
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
    st.markdown("""<div class="panel-title-bar">📝 INSIGHT ESTRATÉGICO PARA O PITCH</div>""", unsafe_allow_html=True)
    multiplicador = retorno_solar_total / (retorno_cdi_final if retorno_cdi_final > 0 else 1)
    st.markdown(f"""
        <div style="background-color: #131722; border: 1px solid #2a2e39; border-radius: 0 0 4px 4px; padding: 20px; height: 160px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
            Ao adotar a estratégia selecionada, o capital injetado se multiplica de forma geométrica através do efeito cascata. 
            Enquanto as aplicações tradicionais prendem o investidor em uma linha reta corroída pela inflação, o modelo operacional 
            solar entrega um retorno total estimado de <b style="color:#10b981;">{multiplicador:.1f}x maior que o CDI</b>, transformando receita operacional em patrimônio líquido consolidado.
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- LINHA 4: TABELA MÊS A MÊS ---
st.markdown("""<div class="panel-title-bar">📋 TABELA DE AUDITORIA DO TERMINAL (MÊS A MÊS)</div>""", unsafe_allow_html=True)
st.dataframe(df.style.format({
    "Faturamento Bruto": "R$ {:,.2f}",
    "Parcelas Banco": "R$ {:,.2f}",
    "Lucro Líquido": "R$ {:,.2f}",
    "Saque Mensal": "R$ {:,.2f}",
    "Caixa Acumulado": "R$ {:,.2f}",
    "Patrimônio Usinas": "R$ {:,.2f}",
    "Valor Total Negócio": "R$ {:,.2f}"
}), use_container_width=True, height=250)
