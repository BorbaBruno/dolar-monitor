import streamlit as st
import pandas as pd
import psycopg2
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60000, key="datarefresh")  # atualiza a cada 60s

# ---------- Configuração do banco ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "dolar_db",
    "user": "postgres",
    "password": "admin",
}

st.set_page_config(page_title="Dashboard Cotação Dólar", layout="wide")


@st.cache_data(ttl=60)  # cache por 60s, evita bater no banco a cada interação
def carregar_dados():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT data_hora, valor_compra, valor_venda, fonte FROM cotacoes ORDER BY data_hora ASC", conn)
    conn.close()
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df["spread"] = df["valor_venda"] - df["valor_compra"]
    return df


st.title("💵 Dashboard Executivo — Cotação USD/BRL")

df_completo = carregar_dados()

if df_completo.empty:
    st.warning("Nenhum dado encontrado na tabela.")
    st.stop()

# ---------- Filtros na barra lateral ----------
st.sidebar.header("Filtros")

data_min = df_completo["data_hora"].min().date()
data_max = df_completo["data_hora"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_max - timedelta(days=3), data_max),
    min_value=data_min,
    max_value=data_max,
)

fontes_disponiveis = df_completo["fonte"].unique().tolist()
fontes_selecionadas = st.sidebar.multiselect(
    "Fonte", options=fontes_disponiveis, default=fontes_disponiveis
)

atualizar = st.sidebar.button("🔄 Atualizar dados agora")
if atualizar:
    st.cache_data.clear()
    st.rerun()

# ---------- Aplicar filtros ----------
if len(periodo) == 2:
    inicio, fim = periodo
    df = df_completo[
        (df_completo["data_hora"].dt.date >= inicio) &
        (df_completo["data_hora"].dt.date <= fim) &
        (df_completo["fonte"].isin(fontes_selecionadas))
    ]
else:
    df = df_completo[df_completo["fonte"].isin(fontes_selecionadas)]

if df.empty:
    st.warning("Nenhum dado no período/filtro selecionado.")
    st.stop()

# ---------- KPIs ----------
ultima = df.iloc[-1]
primeira = df.iloc[0]
variacao_pct = (ultima["valor_venda"] - primeira["valor_venda"]) / primeira["valor_venda"] * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Cotação Atual (Venda)", f"R$ {ultima['valor_venda']:.4f}")
col2.metric("Variação no Período", f"{variacao_pct:+.2f}%")
col3.metric("Mínima", f"R$ {df['valor_venda'].min():.4f}")
col4.metric("Máxima", f"R$ {df['valor_venda'].max():.4f}")
col5.metric("Média", f"R$ {df['valor_venda'].mean():.4f}")

st.markdown("---")

# ---------- Gráfico principal (linha) ----------
fig_linha = go.Figure()
fig_linha.add_trace(go.Scatter(x=df["data_hora"], y=df["valor_compra"], name="Compra",
                                mode="lines", line=dict(color="#4361ee")))
fig_linha.add_trace(go.Scatter(x=df["data_hora"], y=df["valor_venda"], name="Venda",
                                mode="lines", line=dict(color="#e63946")))
fig_linha.update_layout(
    title="Evolução da Cotação",
    xaxis_title="Data/Hora",
    yaxis_title="R$",
    hovermode="x unified",
    height=450,
)
st.plotly_chart(fig_linha, use_container_width=True)

# ---------- Gráficos secundários ----------
col_a, col_b = st.columns(2)

with col_a:
    fig_spread = px.bar(df, x="data_hora", y="spread", title="Spread (Venda - Compra)",
                         color_discrete_sequence=["#7209b7"])
    st.plotly_chart(fig_spread, use_container_width=True)

with col_b:
    fig_hist = px.histogram(df, x="valor_venda", nbins=20, title="Distribuição da Cotação (Venda)",
                             color_discrete_sequence=["#2a9d8f"])
    fig_hist.add_vline(x=df["valor_venda"].mean(), line_dash="dash", line_color="#e63946",
                        annotation_text="Média")
    st.plotly_chart(fig_hist, use_container_width=True)

# ---------- Tabela de dados ----------
with st.expander("📋 Ver dados brutos"):
    st.dataframe(df.sort_values("data_hora", ascending=False), use_container_width=True)

st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
