import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="Impacto das Redes Sociais",
    page_icon="📱",
    layout="wide"
)

# =====================================
# CSS PERSONALIZADO
# =====================================

st.markdown("""
<style>

/* Fundo geral */
.stApp {
    background-color: #050816;
    color: white;
}

/* Container principal */
.block-container {
    padding-top: 9rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Título principal */
.titulo {
    font-size: 120px;
    font-weight: 800;
    color: white;
    text-align: center;
    line-height: 1.1;
    margin-bottom: 35px;
}

/* Subtítulo */
.subtitulo {
    font-size: 28px;
    color: #cfcfcf;
    text-align: center;
    line-height: 1.6;
    margin-bottom: 45px;
}

/* Texto comum */
.texto {
    font-size: 28px;
    line-height: 2.0;
    margin-top: 20px;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background-color: #0d111f;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 0px 18px rgba(0,0,0,0.45);
}

/* Linha divisória */
hr {
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 35px;
    margin-bottom: 35px;
}

/* KPI LABEL */
[data-testid="stMetricLabel"] p {
    font-size: 34px !important;
    font-weight: 800 !important;
    color: white !important;
}

/* KPI VALUE */
[data-testid="stMetricValue"] {
    font-size: 42px !important;
    font-weight: 800 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TÍTULO
# =====================================

st.markdown("""
<h1 class="titulo">
📱 Impacto das Redes Sociais na Saúde Mental
</h1>
""", unsafe_allow_html=True)

st.markdown(
    """
    <p class="subtitulo">
    Dashboard desenvolvido para analisar possíveis relações entre comportamento digital,
    ansiedade, vício digital, sono e desempenho acadêmico.
    </p>
    """,
    unsafe_allow_html=True
)

# =====================================
# TEXTO INTRODUTÓRIO
# =====================================

st.markdown("""
<div class="texto">

• 📱 Uso de redes sociais  
• 😟 Ansiedade  
• 🔗 Vício digital  
• 😴 Sono  
• 📚 Desempenho acadêmico  

</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================
# LER DATASET
# =====================================

df = pd.read_csv("data/Teen_Mental_Health_Dataset.csv")

# =====================================
# TRADUZIR PLATAFORMAS
# =====================================

df["platform_usage"] = df["platform_usage"].replace({
    "Both": "Ambas"
})

# =====================================
# TRADUZIR GÊNERO
# =====================================

df["gender"] = df["gender"].replace({
    "male": "Homem",
    "female": "Mulher"
})

# =====================================
# FILTROS
# =====================================

st.markdown("""
<h2 style='font-size:38px; font-weight:800; color:white;'>
🎛️ Filtros do Dashboard
</h2>
""", unsafe_allow_html=True)

filtro1, filtro2 = st.columns(2)

with filtro1:

    plataforma = st.multiselect(
        "📱 Selecione a Plataforma:",
        options=df["platform_usage"].unique(),
        default=df["platform_usage"].unique()
    )

with filtro2:

    genero = st.multiselect(
        "👥 Selecione o Gênero:",
        options=df["gender"].unique(),
        default=df["gender"].unique()
    )

# =====================================
# APLICAR FILTROS
# =====================================

df_filtrado = df[
    (df["platform_usage"].isin(plataforma)) &
    (df["gender"].isin(genero))
]

# Evitar dashboard vazio
if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# KPIs
# =====================================

total_usuarios = len(df_filtrado)

media_ansiedade_kpi = round(
    df_filtrado["anxiety_level"].mean(), 2
)

media_vicio_kpi = round(
    df_filtrado["addiction_level"].mean(), 2
)

media_sono_kpi = round(
    df_filtrado["sleep_hours"].mean(), 2
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Usuários",
        value=total_usuarios
    )

with col2:
    st.metric(
        label="😟 Média Ansiedade",
        value=media_ansiedade_kpi
    )

with col3:
    st.metric(
        label="🔗 Média Vício",
        value=media_vicio_kpi
    )

with col4:
    st.metric(
        label="😴 Média Sono",
        value=f"{media_sono_kpi}h"
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# GRÁFICO 1 - ANSIEDADE
# =====================================

media_ansiedade = df_filtrado.groupby(
    "platform_usage"
)["anxiety_level"].mean().reset_index()

grafico1 = px.bar(
    media_ansiedade,
    x="platform_usage",
    y="anxiety_level",
    title="📊 Média de Ansiedade por Plataforma",
    color="platform_usage",
    text_auto=".2f",
    template="plotly_dark",
    color_discrete_map={
        "Instagram": "#E1306C",
        "TikTok": "#69C9D0",
        "Ambas": "#A020F0"
    }
)

grafico1.update_layout(
    title_x=0.20,
    showlegend=False,
    title_font_size=30,
    font_size=18,
    plot_bgcolor="#0d111f",
    paper_bgcolor="#0d111f",
    margin=dict(t=80)
)

grafico1.update_xaxes(
    title="Plataformas"
)

grafico1.update_yaxes(
    title="Nível Médio de Ansiedade"
)

# =====================================
# GRÁFICO 2 - VÍCIO DIGITAL
# =====================================

vicio = df_filtrado.groupby(
    "platform_usage"
)["addiction_level"].mean().reset_index()

grafico2 = px.bar(
    vicio,
    x="platform_usage",
    y="addiction_level",
    title="🔗 Nível Médio de Vício Digital",
    color="platform_usage",
    text_auto=".2f",
    template="plotly_dark",
    color_discrete_map={
        "Instagram": "#E1306C",
        "TikTok": "#69C9D0",
        "Ambas": "#A020F0"
    }
)

grafico2.update_layout(
    title_x=0.20,
    showlegend=False,
    title_font_size=30,
    font_size=18,
    plot_bgcolor="#0d111f",
    paper_bgcolor="#0d111f",
    margin=dict(t=80)
)

grafico2.update_xaxes(
    title="Plataformas"
)

grafico2.update_yaxes(
    title="Nível Médio de Vício"
)

# =====================================
# MOSTRAR GRÁFICOS
# =====================================

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(grafico1, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(grafico2, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# SONO X ANSIEDADE
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

sono_ansiedade = df_filtrado.groupby(
    ["sleep_hours", "platform_usage"]
)["anxiety_level"].mean().reset_index()

grafico_sono = px.line(
    sono_ansiedade,
    x="sleep_hours",
    y="anxiety_level",
    color="platform_usage",
    markers=True,
    title="😴 Relação entre Sono e Ansiedade",
    template="plotly_dark",
    color_discrete_map={
        "Instagram": "#E1306C",
        "TikTok": "#69C9D0",
        "Ambas": "#A020F0"
    }
)

grafico_sono.update_traces(
    line=dict(width=5),
    marker=dict(size=9)
)

grafico_sono.update_layout(
    title_x=0.20,
    title_font_size=30,
    paper_bgcolor="#0d111f",
    plot_bgcolor="#0d111f",
    font=dict(size=18),
    xaxis_title="Horas de Sono",
    yaxis_title="Média de Ansiedade",
    height=650,
    legend_title="Plataformas"
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(grafico_sono, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# VÍCIO DIGITAL X DESEMPENHO
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

vicio_desempenho = df_filtrado.groupby(
    ["addiction_level", "platform_usage"]
)["academic_performance"].mean().reset_index()

grafico_desempenho = px.line(
    vicio_desempenho,
    x="addiction_level",
    y="academic_performance",
    color="platform_usage",
    markers=True,
    title="📚 Vício Digital x Desempenho Acadêmico",
    template="plotly_dark",
    color_discrete_map={
        "Instagram": "#E1306C",
        "TikTok": "#69C9D0",
        "Ambas": "#A020F0"
    }
)

grafico_desempenho.update_traces(
    line=dict(width=5),
    marker=dict(size=9)
)

grafico_desempenho.update_layout(
    title_x=0.20,
    title_font_size=30,
    paper_bgcolor="#0d111f",
    plot_bgcolor="#0d111f",
    font=dict(size=18),
    xaxis_title="Nível de Vício Digital",
    yaxis_title="Desempenho Acadêmico Médio",
    height=650,
    legend_title="Plataformas"
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(grafico_desempenho, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# DONUT CHART
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

distribuicao = df_filtrado["platform_usage"].value_counts().reset_index()

distribuicao.columns = ["Plataforma", "Quantidade"]

donut = px.pie(
    distribuicao,
    names="Plataforma",
    values="Quantidade",
    hole=0.65,
    title="📱 Distribuição de Usuários por Plataforma",
    template="plotly_dark",
    color="Plataforma",
    color_discrete_map={
        "Instagram": "#E1306C",
        "TikTok": "#69C9D0",
        "Ambas": "#A020F0"
    }
)

donut.update_traces(
    textinfo='label+percent',
    textfont_size=18
)

donut.update_layout(
    title_x=0.20,
    title_font_size=30,
    paper_bgcolor="#0d111f",
    plot_bgcolor="#0d111f",
    height=650,
    font=dict(size=18),
    showlegend=False
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(donut, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# HEATMAP DE CORRELAÇÃO
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

correlacao = df_filtrado[
    [
        "anxiety_level",
        "addiction_level",
        "sleep_hours",
        "academic_performance"
    ]
].corr()

labels = [
    "Ansiedade",
    "Vício Digital",
    "Sono",
    "Desempenho"
]

heatmap = ff.create_annotated_heatmap(
    z=correlacao.values,
    x=labels,
    y=labels,
    annotation_text=correlacao.round(2).values,
    colorscale="RdBu",
    showscale=True
)

heatmap.update_layout(
    title="🔥 Correlação entre Indicadores",
    title_x=0.20,
    title_font_size=30,
    paper_bgcolor="#0d111f",
    plot_bgcolor="#0d111f",
    font=dict(
        color="white",
        size=18
    ),
    height=700
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(heatmap, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# INSIGHTS AUTOMÁTICOS
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='font-size:42px; font-weight:800; color:white; margin-bottom:25px;'>
📌 Principais Insights
</h2>
""", unsafe_allow_html=True)

# Maior ansiedade
maior_ansiedade = df_filtrado.groupby(
    "platform_usage"
)["anxiety_level"].mean().idxmax()

# Maior vício
maior_vicio = df_filtrado.groupby(
    "platform_usage"
)["addiction_level"].mean().idxmax()

# Média de sono
media_sono = round(df_filtrado["sleep_hours"].mean(), 1)

# Desempenho acadêmico médio
media_desempenho = round(
    df_filtrado["academic_performance"].mean(), 1
)

st.markdown(f"""
<div style="
background-color:#0d111f;
padding:35px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.08);
box-shadow:0px 0px 18px rgba(0,0,0,0.45);
font-size:26px;
line-height:2.2;
">

✅ <b>Plataforma com maior média de ansiedade:</b> {maior_ansiedade}<br>

✅ <b>Plataforma com maior média de vício digital:</b> {maior_vicio}<br>

✅ <b>Média geral de sono dos usuários:</b> {media_sono} horas<br>

✅ <b>Desempenho acadêmico médio:</b> {media_desempenho}<br>

</div>
""", unsafe_allow_html=True)

# =====================================
# RECOMENDAÇÕES E SOLUÇÕES
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='font-size:42px; font-weight:800; color:white; margin-bottom:25px;'>
💡 Recomendações e Possíveis Soluções
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background-color:#0d111f;
padding:35px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.08);
box-shadow:0px 0px 18px rgba(0,0,0,0.45);
font-size:26px;
line-height:2.2;
">

🛌 Dormir mais de 7 horas pode ajudar a reduzir níveis de ansiedade.<br><br>

📵 Reduzir o uso excessivo de redes sociais pode ajudar a diminuir sinais de vício digital.<br><br>

📚 Equilibrar tempo online e estudos pode contribuir para um melhor desempenho acadêmico.<br><br>

🏃 Atividades físicas e pausas digitais podem auxiliar na melhoria da saúde mental.<br>

</div>
""", unsafe_allow_html=True)

# =====================================
# RECOMENDAÇÕES INTELIGENTES
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='font-size:42px; font-weight:800; color:white; margin-bottom:25px;'>
🧠 Recomendações Inteligentes
</h2>
""", unsafe_allow_html=True)

# Recomendações automáticas

recomendacoes = []

# Ansiedade
if media_ansiedade_kpi >= 5:
    recomendacoes.append("""
    <div style="
    background-color:#0d111f;
    padding:30px;
    border-radius:20px;
    margin-bottom:25px;
    border:1px solid rgba(255,255,255,0.08);
    ">
    
    <h3>😟 Ansiedade Elevada</h3>

    <p style='font-size:22px; line-height:1.8;'>
    Os dados mostram níveis elevados de ansiedade entre os usuários analisados.
    </p>

    <p style='font-size:22px; line-height:1.8;'>
    💡 <b>Recomendação:</b> reduzir o tempo excessivo em redes sociais e criar momentos de pausa digital pode ajudar no bem-estar mental.
    </p>

    </div>
    """)

# Sono
if media_sono_kpi < 7:
    recomendacoes.append("""
    <div style="
    background-color:#0d111f;
    padding:30px;
    border-radius:20px;
    margin-bottom:25px;
    border:1px solid rgba(255,255,255,0.08);
    ">
    
    <h3>😴 Qualidade do Sono</h3>

    <p style='font-size:22px; line-height:1.8;'>
    A média de sono identificada ficou abaixo das 7 horas recomendadas.
    </p>

    <p style='font-size:22px; line-height:1.8;'>
    💡 <b>Recomendação:</b> estabelecer uma rotina de descanso mais equilibrada pode contribuir para redução da ansiedade e melhora da saúde mental.
    </p>

    </div>
    """)

# Vício digital
if media_vicio_kpi >= 5:
    recomendacoes.append("""
    <div style="
    background-color:#0d111f;
    padding:30px;
    border-radius:20px;
    margin-bottom:25px;
    border:1px solid rgba(255,255,255,0.08);
    ">
    
    <h3>🔗 Vício Digital</h3>

    <p style='font-size:22px; line-height:1.8;'>
    O nível médio de vício digital apresentou valores elevados no dataset analisado.
    </p>

    <p style='font-size:22px; line-height:1.8;'>
    💡 <b>Recomendação:</b> pausas durante o uso das plataformas e controle do tempo de tela podem ajudar na qualidade de vida.
    </p>

    </div>
    """)

# Mostrar recomendações
for recomendacao in recomendacoes:
    st.markdown(recomendacao, unsafe_allow_html=True)

# =====================================
# RODAPÉ
# =====================================

st.markdown("<br><hr>", unsafe_allow_html=True)

st.info(
    "Os valores representam médias calculadas com base nos dados do dataset analisado."
)