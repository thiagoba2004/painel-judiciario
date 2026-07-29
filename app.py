import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard do Poder Judiciário",
    page_icon="⚖️",
    layout="wide"
)


@st.cache_data
def carregar_dados():
    varas = pd.read_csv("dados/varas.csv")
    municipios = pd.read_csv("dados/municipios.csv")

    # Padroniza textos
    for coluna in ["tribunal", "comarca", "vara"]:
        varas[coluna] = varas[coluna].astype(str).str.strip()

    for coluna in ["tribunal", "comarca", "municipio"]:
        municipios[coluna] = municipios[coluna].astype(str).str.strip()

    # Converte números
    colunas_numericas_varas = [
        "processos",
        "conclusos",
        "serventuarios"
    ]

    for coluna in colunas_numericas_varas:
        varas[coluna] = pd.to_numeric(
            varas[coluna],
            errors="coerce"
        ).fillna(0)

    municipios["habitantes"] = pd.to_numeric(
        municipios["habitantes"],
        errors="coerce"
    ).fillna(0)

    # Soma os habitantes de todos os municípios de cada comarca
    populacao_comarcas = (
        municipios
        .groupby(["tribunal", "comarca"], as_index=False)
        ["habitantes"]
        .sum()
    )

    # Junta a população da comarca às informações das varas
    dados = varas.merge(
        populacao_comarcas,
        on=["tribunal", "comarca"],
        how="left"
    )

    dados["habitantes"] = dados["habitantes"].fillna(0)

        # Indicadores calculados
    dados["processos_por_1000_habitantes"] = (
        dados["processos"]
        .div(dados["habitantes"])
        .mul(1000)
        .where(dados["habitantes"] > 0)
    )

    dados["percentual_conclusos"] = (
        dados["conclusos"]
        .div(dados["processos"])
        .mul(100)
        .where(dados["processos"] > 0)
    )

    dados["processos_por_serventuario"] = (
        dados["processos"]
        .div(dados["serventuarios"])
        .where(dados["serventuarios"] > 0)
    )

    dados["taxa_congestionamento"] = (
        dados["conclusos"]
        .div(dados["processos"])
        .mul(100)
        .where(dados["processos"] > 0)
    )

    dados["conclusos_por_serventuario"] = (
        dados["conclusos"]
        .div(dados["serventuarios"])
        .where(dados["serventuarios"] > 0)
    )

    return dados, municipios


try:
    df, municipios = carregar_dados()

except FileNotFoundError:
    st.error(
        "Não foi possível encontrar os arquivos "
        "'dados/varas.csv' e 'dados/municipios.csv'."
    )
    st.stop()


st.title("Dashboard de Indicadores do Poder Judiciário")
st.caption(
    "Análise de processos, conclusos, serventuários e população das comarcas"
)

# -----------------------------
# Filtros
# -----------------------------

st.sidebar.header("Filtros")

periodos = sorted(df["periodo"].dropna().unique())

periodo_selecionado = st.sidebar.selectbox(
    "Período",
    periodos
)

df_filtrado = df[df["periodo"] == periodo_selecionado].copy()

tribunais = sorted(df_filtrado["tribunal"].unique())

tribunal_selecionado = st.sidebar.multiselect(
    "Tribunal",
    tribunais,
    default=tribunais
)

if tribunal_selecionado:
    df_filtrado = df_filtrado[
        df_filtrado["tribunal"].isin(tribunal_selecionado)
    ]

comarcas = sorted(df_filtrado["comarca"].unique())

comarca_selecionada = st.sidebar.multiselect(
    "Comarca",
    comarcas,
    default=comarcas
)

if comarca_selecionada:
    df_filtrado = df_filtrado[
        df_filtrado["comarca"].isin(comarca_selecionada)
    ]

# -----------------------------
# Cálculos gerais
# -----------------------------

processos_total = df_filtrado["processos"].sum()
conclusos_total = df_filtrado["conclusos"].sum()
serventuarios_total = df_filtrado["serventuarios"].sum()

# A população não pode ser somada diretamente por vara,
# pois a mesma população aparece em várias varas da comarca.
comarcas_filtradas = (
    df_filtrado[["tribunal", "comarca"]]
    .drop_duplicates()
)

populacao_total = (
    comarcas_filtradas
    .merge(
        municipios.groupby(
            ["tribunal", "comarca"],
            as_index=False
        )["habitantes"].sum(),
        on=["tribunal", "comarca"],
        how="left"
    )["habitantes"]
    .sum()
)

percentual_conclusos = (
    conclusos_total / processos_total * 100
    if processos_total > 0 else 0
)

processos_por_serventuario = (
    processos_total / serventuarios_total
    if serventuarios_total > 0 else 0
)

processos_por_1000_habitantes = (
    processos_total / populacao_total * 1000
    if populacao_total > 0 else 0
)

# -----------------------------
# Indicadores principais
# -----------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Processos",
    f"{processos_total:,.0f}".replace(",", ".")
)

col2.metric(
    "Processos conclusos",
    f"{conclusos_total:,.0f}".replace(",", ".")
)

col3.metric(
    "Serventuários",
    f"{serventuarios_total:,.0f}".replace(",", ".")
)

col4.metric(
    "Processos por 1.000 hab.",
    f"{processos_por_1000_habitantes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

col5.metric(
    "Conclusos (%)",
    f"{percentual_conclusos:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
)

st.divider()

# -----------------------------
# Agregação por comarca
# -----------------------------

df_comarcas = (
    df_filtrado
    .groupby(["tribunal", "comarca"], as_index=False)
    .agg(
        processos=("processos", "sum"),
        conclusos=("conclusos", "sum"),
        serventuarios=("serventuarios", "sum")
    )
)

pop_comarcas = (
    municipios
    .groupby(["tribunal", "comarca"], as_index=False)
    .agg(habitantes=("habitantes", "sum"))
)

df_comarcas = df_comarcas.merge(
    pop_comarcas,
    on=["tribunal", "comarca"],
    how="left"
)

df_comarcas["processos_por_1000_habitantes"] = (
    df_comarcas["processos"]
    .div(df_comarcas["habitantes"])
    .mul(1000)
    .where(df_comarcas["habitantes"] > 0)
)

df_comarcas["percentual_conclusos"] = (
    df_comarcas["conclusos"]
    .div(df_comarcas["processos"])
    .mul(100)
    .where(df_comarcas["processos"] > 0)
)

df_comarcas["processos_por_serventuario"] = (
    df_comarcas["processos"]
    .div(df_comarcas["serventuarios"])
    .where(df_comarcas["serventuarios"] > 0)
)

# -----------------------------
# Gráficos
# -----------------------------

grafico_processos = px.bar(
    df_comarcas.sort_values("processos", ascending=False),
    x="comarca",
    y="processos",
    color="tribunal",
    title="Processos por comarca",
    text_auto=True
)

grafico_processos.update_layout(
    xaxis_title="Comarca",
    yaxis_title="Número de processos",
    xaxis_tickangle=-45
)

st.plotly_chart(
    grafico_processos,
    use_container_width=True
)

coluna1, coluna2 = st.columns(2)

with coluna1:
    grafico_judicializacao = px.bar(
        df_comarcas.sort_values(
            "processos_por_1000_habitantes",
            ascending=False
        ),
        x="comarca",
        y="processos_por_1000_habitantes",
        color="tribunal",
        title="Processos por 1.000 habitantes",
        text_auto=".2f"
    )

    grafico_judicializacao.update_layout(
        xaxis_title="Comarca",
        yaxis_title="Processos por 1.000 habitantes",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        grafico_judicializacao,
        use_container_width=True
    )

with coluna2:
    grafico_conclusos = px.bar(
        df_comarcas.sort_values(
            "percentual_conclusos",
            ascending=False
        ),
        x="comarca",
        y="percentual_conclusos",
        color="tribunal",
        title="Percentual de processos conclusos",
        text_auto=".2f"
    )

    grafico_conclusos.update_layout(
        xaxis_title="Comarca",
        yaxis_title="Conclusos (%)",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        grafico_conclusos,
        use_container_width=True
    )

# -----------------------------
# Tabela por comarca
# -----------------------------

st.subheader("Indicadores por comarca")

tabela_comarcas = df_comarcas.copy()

tabela_comarcas["processos"] = tabela_comarcas["processos"].round(0)
tabela_comarcas["conclusos"] = tabela_comarcas["conclusos"].round(0)
tabela_comarcas["serventuarios"] = tabela_comarcas["serventuarios"].round(0)
tabela_comarcas["processos_por_1000_habitantes"] = (
    tabela_comarcas["processos_por_1000_habitantes"].round(2)
)
tabela_comarcas["percentual_conclusos"] = (
    tabela_comarcas["percentual_conclusos"].round(2)
)
tabela_comarcas["processos_por_serventuario"] = (
    tabela_comarcas["processos_por_serventuario"].round(2)
)

st.dataframe(
    tabela_comarcas,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Tabela por vara
# -----------------------------

st.subheader("Indicadores por vara")

colunas_varas = [
    "tribunal",
    "comarca",
    "vara",
    "periodo",
    "processos",
    "conclusos",
    "serventuarios",
    "habitantes",
    "percentual_conclusos",
    "processos_por_serventuario",
    "taxa_congestionamento"
]

st.dataframe(
    df_filtrado[colunas_varas].round(2),
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Download dos dados filtrados
# -----------------------------

csv_download = df_filtrado.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="Baixar dados filtrados",
    data=csv_download,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)